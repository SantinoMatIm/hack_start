"""Database connection setup using SQLAlchemy."""

import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from sqlalchemy.exc import OperationalError
from typing import Generator

from src.config.settings import get_settings


# Global engine instance
_engine = None

# Retry configuration for transient SSL errors
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 0.5


def get_engine():
    """Create and return SQLAlchemy engine.
    
    Uses NullPool for cloud databases (Supabase) to avoid connection pooling issues.
    Each request gets a fresh connection that is closed after use.
    """
    global _engine
    if _engine is not None:
        return _engine
        
    settings = get_settings()
    
    # Ensure sslmode is set for Supabase
    db_url = settings.database_url
    if "sslmode" not in db_url:
        separator = "&" if "?" in db_url else "?"
        db_url = f"{db_url}{separator}sslmode=require"
    
    # Use NullPool for cloud databases - no connection pooling
    # This is more reliable for Supabase which has limited connections
    _engine = create_engine(
        db_url,
        poolclass=NullPool,  # No pooling - fresh connection each time
        connect_args={
            "connect_timeout": 30,
            # TCP keepalive settings to prevent idle disconnections
            "keepalives": 1,
            "keepalives_idle": 30,  # Seconds before sending keepalive
            "keepalives_interval": 10,  # Seconds between keepalives
            "keepalives_count": 5,  # Failed keepalives before disconnect
        },
    )
    
    return _engine


def get_session_factory():
    """Get or create the session factory."""
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def init_db():
    """Initialize database engine (called at startup)."""
    get_engine()  # Just ensure engine is created
    print("Database ready (NullPool - no connection pooling)")


def dispose_engine():
    """Dispose the current engine and force recreation on next use.
    
    This is useful when SSL connections become stale and need to be reset.
    """
    global _engine
    if _engine is not None:
        try:
            _engine.dispose()
        except Exception:
            pass
        _engine = None


def get_session() -> Generator[Session, None, None]:
    """Get database session dependency for FastAPI.
    
    Creates a new session for each request and ensures it's closed after.
    """
    from sqlalchemy import text
    SessionLocal = get_session_factory()
    
    last_error = None
    for attempt in range(MAX_RETRIES):
        db = SessionLocal()
        try:
            yield db
            return
        except OperationalError as e:
            last_error = e
            error_msg = str(e).lower()
            # Retry on SSL connection errors
            if "ssl" in error_msg or "connection" in error_msg:
                if attempt < MAX_RETRIES - 1:
                    db.close()
                    time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))
                    continue
            raise
        finally:
            db.close()
    
    # If we exhausted retries, raise the last error
    if last_error:
        raise last_error


def get_session_with_retry() -> Session:
    """Get a database session with automatic retry for transient errors.
    
    Use this for non-generator contexts where you need direct session access.
    Caller is responsible for closing the session.
    """
    SessionLocal = get_session_factory()
    
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            db = SessionLocal()
            # Test connection
            from sqlalchemy import text
            db.execute(text("SELECT 1"))
            return db
        except OperationalError as e:
            last_error = e
            error_msg = str(e).lower()
            if "ssl" in error_msg or "connection" in error_msg:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))
                    continue
            raise
    
    if last_error:
        raise last_error
