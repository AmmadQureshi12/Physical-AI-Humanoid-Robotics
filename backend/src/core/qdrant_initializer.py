"""
Qdrant collection initialization module.
"""
from qdrant_client.http import models
from src.core.qdrant_client import get_qdrant_client, get_collection_name
from src.core.config import settings
from src.core.logging_config import get_logger
from src.core.constants import DEFAULT_EMBEDDING_DIMENSION


logger = get_logger(__name__)


def initialize_qdrant_collection():
    """
    Initialize the Qdrant collection if it doesn't exist.
    """
    client = get_qdrant_client()
    collection_name = get_collection_name()
    
    # Check if collection exists
    collection_exists = False
    try:
        client.get_collection(collection_name=collection_name)
        collection_exists = True
        logger.info(f"Collection '{collection_name}' already exists")
    except Exception:
        # Collection doesn't exist, will create it
        collection_exists = False
    
    if not collection_exists:
        # Create the collection with appropriate vector configuration
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=DEFAULT_EMBEDDING_DIMENSION,  # Cohere embeddings are 384-dimensional
                distance=models.Distance.COSINE
            )
        )
        
        # Create payload index for faster filtering if needed
        client.create_payload_index(
            collection_name=collection_name,
            field_name="source_chapter",
            field_schema=models.PayloadSchemaType.KEYWORD
        )
        
        logger.info(f"Created Qdrant collection: {collection_name}")
    else:
        # Update collection if needed (e.g., if vector size changed)
        collection_info = client.get_collection(collection_name=collection_name)
        required_size = DEFAULT_EMBEDDING_DIMENSION
        
        if collection_info.config.params.vectors.size != required_size:
            logger.warning(f"Vector size mismatch. Expected {required_size}, got {collection_info.config.params.vectors.size}")
            # In a production system, you might need to recreate the collection
            # For now, just log the issue
    
    # Create any additional indexes or configurations needed
    # Create index for source_section field
    client.create_payload_index(
        collection_name=collection_name,
        field_name="source_section",
        field_schema=models.PayloadSchemaType.KEYWORD
    )
    
    logger.info(f"Qdrant collection '{collection_name}' initialization completed")


if __name__ == "__main__":
    initialize_qdrant_collection()