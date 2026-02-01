"""Database retry utilities for handling transient Supabase SSL errors."""

import time
import functools
from typing import TypeVar, Callable, Any
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from src.db.connection import get_session_factory

T = TypeVar('T')

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 0.5


def is_transient_error(error: Exception) -> bool:
    """Check if an error is a transient connection error that can be retried."""
    error_msg = str(error).lower()
    transient_indicators = [
        "ssl connection has been closed unexpectedly",
        "connection refused",
        "connection reset",
        "connection timed out",
        "server closed the connection unexpectedly",
    ]
    return any(indicator in error_msg for indicator in transient_indicators)


def get_session_with_retry() -> Session:
    """Get a database session with automatic retry for transient errors.
    
    Creates a fresh connection for each call.
    Caller is responsible for closing the session.
    """
    SessionLocal = get_session_factory()
    
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            session = SessionLocal()
            # Test the connection immediately
            from sqlalchemy import text
            session.execute(text("SELECT 1"))
            return session
        except OperationalError as e:
            last_error = e
            if is_transient_error(e) and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))
                continue
            raise
    
    if last_error:
        raise last_error


def with_db_retry(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator that wraps a function with database retry logic.
    
    The decorated function should accept a 'session' parameter.
    On transient errors, the function will be retried with a fresh session.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> T:
        last_error = None
        
        for attempt in range(MAX_RETRIES):
            session = None
            try:
                session = get_session_with_retry()
                # Inject session into kwargs
                kwargs['session'] = session
                result = func(*args, **kwargs)
                session.commit()
                return result
            except OperationalError as e:
                last_error = e
                if session:
                    try:
                        session.rollback()
                    except:
                        pass
                    try:
                        session.close()
                    except:
                        pass
                
                if is_transient_error(e) and attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))
                    continue
                raise
            except Exception:
                if session:
                    try:
                        session.rollback()
                    except:
                        pass
                raise
            finally:
                if session:
                    try:
                        session.close()
                    except:
                        pass
        
        if last_error:
            raise last_error
    
    return wrapper


def execute_with_retry(operation: Callable[[Session], T]) -> T:
    """Execute a database operation with automatic retry on transient errors.
    
    Args:
        operation: A callable that takes a Session and returns a result.
        
    Returns:
        The result of the operation.
        
    Example:
        def get_zones(session):
            return session.query(Zone).all()
        
        zones = execute_with_retry(get_zones)
    """
    last_error = None
    
    for attempt in range(MAX_RETRIES):
        session = None
        try:
            session = get_session_with_retry()
            result = operation(session)
            return result
        except OperationalError as e:
            last_error = e
            if is_transient_error(e) and attempt < MAX_RETRIES - 1:
                if session:
                    try:
                        session.close()
                    except:
                        pass
                time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))
                continue
            raise
        finally:
            if session:
                try:
                    session.close()
                except:
                    pass
    
    if last_error:
        raise last_error
