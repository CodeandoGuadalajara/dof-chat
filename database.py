"""Database connection utilities using AirSQLModel."""

import os
from contextlib import asynccontextmanager, aclosing
import airsqlmodel as sql
from config import settings

# Ensure DATABASE_URL is set for airsqlmodel
if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = settings.database_url

@asynccontextmanager
async def get_async_session_context():
    """
    Provide an asynchronous database session as an async context manager.
    
    This function wraps the airsqlmodel async generator using `aclosing` 
    to ensure the session is properly closed even if exceptions occur, 
    preventing context leakage or masked errors.
    
    Usage:
        async with get_async_session_context() as session:
            result = await session.exec(statement)
            
    Yields:
        AsyncSession: A managed SQLAlchemy async session.
    """
    # Use aclosing to ensure the generator's aclose() is called upon exit
    async with aclosing(sql.get_async_session()) as session_gen:
        try:
            # Advance the generator to obtain the session instance
            session = await anext(session_gen)
        except StopAsyncIteration:
            raise RuntimeError("Database generator failed to yield a session.") from None
        
        try:
            yield session
        except Exception:
            # Exceptions are re-raised so they can be handled by the caller or middleware.
            # 'aclosing' handles the generator cleanup without suppressing this exception.
            raise

# Re-export dependency for FastAPI routes
async_session_dependency = sql.async_session_dependency