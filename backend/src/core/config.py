"""
Core configuration module with settings validation.
"""
import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation."""

    # Database settings
    neon_db_url: str = Field(
        default="postgresql+psycopg://neondb_owner:npg_am6kr9fbODhv@ep-floral-lake-ahzd486u-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
        description="Neon Postgres database URL"
    )

    # Qdrant settings
    qdrant_url: str = Field(
        default=os.getenv("QDRANT_URL", "https://6c0a5f3f-0328-496b-adf5-d0bc5613920b.us-east4-0.gcp.cloud.qdrant.io:6333"),
        description="Qdrant Cloud URL"
    )
    qdrant_api_key: str = Field(
        default=os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.TqzYwK3-fEBd3smRL3WItTijQZB3f_QW21lG1yXkIEo"),
        description="Qdrant API key"
    )
    qdrant_collection_name: str = Field(
        default=os.getenv("QDRANT_COLLECTION_NAME", "book_content_chunks"),
        description="Name of the Qdrant collection for book content"
    )

    # LLM Provider settings
    cohere_api_key: str = Field(
        default=os.getenv("COHERE_API_KEY", "M8Lh6vHl4fzxOmrQD3F5t4ThbZhLgsQllAZwsUGo"),
        description="Cohere API key for Qwen models"
    )
    model_name: str = Field(
        default=os.getenv("MODEL_NAME", "command-r-08-2024"),
        description="Name of the model to use"
    )

    # Application settings
    secret_key: str = Field(
        default=os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
        description="Secret key for signing"
    )
    debug: bool = Field(
        default=os.getenv("DEBUG", "False").lower() == "true",
        description="Enable debug mode"
    )
    log_level: str = Field(
        default=os.getenv("LOG_LEVEL", "INFO"),
        description="Logging level"
    )

    # Rate limiting
    rate_limit_requests_per_minute: int = Field(
        default=int(os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "60")),
        description="Number of requests allowed per minute per IP"
    )
    rate_limit_window_seconds: int = Field(
        default=int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60")),
        description="Time window for rate limiting in seconds"
    )

    # Book configuration
    book_title: str = Field(
        default=os.getenv("BOOK_TITLE", "AI-Native Software Development"),
        description="Title of the book"
    )
    book_author: str = Field(
        default=os.getenv("BOOK_AUTHOR", "Author Name"),
        description="Author of the book"
    )
    book_publication_year: int = Field(
        default=int(os.getenv("BOOK_PUBLICATION_YEAR", "2024")),
        description="Publication year of the book"
    )

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }


# Create a single instance of settings
settings = Settings()


def get_settings():
    """Get the application settings."""
    return settings