"""
Database initialization module for the RAG Chatbot.
"""
from sqlalchemy import create_engine
from src.database.models import Base
from src.core.config import settings
from src.core.logging_config import get_logger


logger = get_logger(__name__)


def init_db():
    """
    Initialize the database tables if they don't exist.
    """
    # Create a sync engine for database operations
    engine = create_engine(
        settings.neon_db_url,
        echo=settings.debug,  # Log SQL statements in debug mode
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,  # Recycle connections every 5 minutes
    )

    try:
        logger.info("Initializing database tables...")
        print(settings.neon_db_url)
        # Create all tables defined in models
        Base.metadata.create_all(engine)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
    finally:
        # Dispose the engine to close all connections
        engine.dispose()


if __name__ == "__main__":
    init_db()