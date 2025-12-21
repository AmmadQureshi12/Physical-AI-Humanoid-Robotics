"""
Qdrant client connection module with API key authentication.
"""
import os
from qdrant_client import QdrantClient


# Get configuration from environment variables
QDRANT_URL = os.getenv("QDRANT_URL", "https://6c0a5f3f-0328-496b-adf5-d0bc5613920b.us-east4-0.gcp.cloud.qdrant.io:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.TqzYwK3-fEBd3smRL3WItTijQZB3f_QW21lG1yXkIEo")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_content_chunks")


# Initialize Qdrant client with API key authentication
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    # Set timeout and other options as needed
    timeout=10,
)


def get_qdrant_client():
    """
    Returns the initialized Qdrant client.
    """
    return client


def get_collection_name():
    """
    Returns the collection name to use for book content.
    """
    return QDRANT_COLLECTION_NAME