"""Database connection utilities for read-only operations with AUTOCOMMIT."""

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings


# Lazy-initialized read-only engine and session factory
_read_engine = None
_read_session_factory = None


def _get_read_session_factory():
    """Get or create the read-only session factory with AUTOCOMMIT isolation."""
    global _read_engine, _read_session_factory
    if _read_session_factory is None:
        # Create engine directly with AUTOCOMMIT to eliminate transaction overhead
        _read_engine = create_async_engine(
            url=settings.database_url,
            echo=False,  # Set to True for SQL query logging
            pool_pre_ping=True,  # Verify connections before using
            pool_size=5,  # Connection pool size
            max_overflow=10  # Max overflow connections
        ).execution_options(isolation_level="AUTOCOMMIT")
        
        _read_session_factory = sessionmaker(
            bind=_read_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _read_session_factory


@asynccontextmanager
async def get_readonly_session_context():
    """
    Provide a read-only async database session with AUTOCOMMIT isolation.
    
    Uses AUTOCOMMIT to eliminate transaction overhead (no BEGIN/COMMIT/ROLLBACK)
    for read-only SELECT operations. More efficient for read-heavy workloads.
    
    WARNING: Only for read operations. Do NOT use for INSERT/UPDATE/DELETE.
    
    Usage:
        async with get_readonly_session_context() as session:
            result = await session.execute(select(Model))
            
    Yields:
        AsyncSession: Read-only session with AUTOCOMMIT isolation.
    """
    session_factory = _get_read_session_factory()
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def readonly_db_lifespan(app):
    """
    Lifespan context manager for read-only database engine with AUTOCOMMIT.
    
    Manages the lifecycle of the read-only async database engine:
    - Initializes the engine on startup
    - Properly disposes of the engine on shutdown
    
    Usage:
        app = air.Air(lifespan=readonly_db_lifespan)
    
    Args:
        app: The FastAPI/Air application instance
    """
    # Initialize the engine on startup
    _get_read_session_factory()
    yield
    # Dispose of the engine on shutdown
    global _read_engine
    if _read_engine is not None:
        await _read_engine.dispose()