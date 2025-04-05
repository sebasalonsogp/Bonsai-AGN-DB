from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings

# Create async engine for database connection with MariaDB
# The asyncmy driver enables asynchronous I/O with MariaDB
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO_LOG,  # When True, logs all SQL queries for debugging
    pool_size=settings.DB_POOL_SIZE,  # Number of connections to keep open in the pool
    max_overflow=settings.DB_MAX_OVERFLOW,  # Max number of connections beyond pool_size
    pool_pre_ping=True,  # Verify connection is still active before using it
)

# Create session factory for getting async sessions
# This factory creates new session objects that are properly configured
# for use with FastAPI's async endpoints
async_session_factory = sessionmaker(
    engine, 
    class_=AsyncSession,  # Use async session for non-blocking database operations 
    expire_on_commit=False,  # Keep objects usable after a commit operation
    autoflush=False  # Don't automatically flush changes before each query
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an async database session with proper transaction handling.
    
    This function serves as a FastAPI dependency that creates a new database session
    for each request, handles commits and rollbacks automatically, and ensures
    proper cleanup when the request is complete. It uses contextlib's async context
    manager to ensure resources are properly released even if exceptions occur.
    
    The session automatically commits changes if no exceptions are raised,
    or rolls back changes if an exception occurs. This supports the Unit of Work pattern
    where all database operations within a request are treated as a single transaction.
    
    Yields:
        AsyncSession: SQLAlchemy async session that can be used for database operations
        
    Example:
        ```python
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db_session)):
            # Use db session for async database operations
            result = await db.execute(select(Item))
            items = result.scalars().all()
            return items
        ```
        
    Raises:
        Any exceptions from database operations are propagated after rollback
    """
    async with async_session_factory() as session:
        try:
            # Yield the session to the route handler
            yield session
            # If no exception occurs, commit the transaction
            await session.commit()
        except Exception:
            # If an exception occurs, rollback the transaction
            await session.rollback()
            # Re-raise the exception for error handling middleware
            raise
        finally:
            # Always ensure the session is closed
            await session.close() 