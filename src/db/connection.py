"""Database connection setup using SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from src.config.settings import get_settings


def get_engine():
    """Create and return SQLAlchemy engine."""
    settings = get_settings()
    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


engine = None
SessionLocal = None


def init_db():
    """Initialize database engine and session factory."""
    global engine, SessionLocal
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session dependency for FastAPI."""
    if SessionLocal is None:
        init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
