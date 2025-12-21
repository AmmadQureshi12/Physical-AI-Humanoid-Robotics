"""
Database connection setup and utilities.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.core.logging_config import get_logger


logger = get_logger(__name__)

# Create async engine
engine = create_async_engine(
    settings.neon_db_url,
    echo=settings.debug,  # Log SQL statements in debug mode
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections every 5 minutes
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db_session():
    """
    Dependency to get async database session.
    """
    async with AsyncSessionLocal() as session:
        yield session


def init_db():
    """
    Initialize the database tables if they don't exist.
    """
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy import event
    from src.database.models import Base
    from src.core.config import settings

    # Create a temporary sync engine for table creation
    # We need to use sync methods for table creation
    import sqlalchemy as sa
    from sqlalchemy import create_engine
    from sqlalchemy.pool import StaticPool

    # For async database setup, we'll use alembic in production
    # For now, using the async engine directly

    async def create_tables():
        logger.info("Initializing database tables...")
        async with engine.begin() as conn:
            # Create all tables defined in models
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized successfully")

    # Run the async function
    asyncio.run(create_tables())


if __name__ == "__main__":
    init_db()