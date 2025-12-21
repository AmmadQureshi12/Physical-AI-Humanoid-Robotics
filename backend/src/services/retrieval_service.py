"""
Retrieval service to get context from Qdrant based on user query.
"""
from typing import List, Optional
from src.core.qdrant_client import get_qdrant_client, get_collection_name
from src.core.exceptions import RetrievalException
from src.core.constants import DEFAULT_TOP_K, DEFAULT_MIN_SIMILARITY
from src.database.models import RetrievedContext as RetrievedContextModel
from qdrant_client.http import models
from src.core.logging_config import get_logger
import cohere


logger = get_logger(__name__)


class RetrievalService:
    """Service to handle retrieval of relevant contexts from Qdrant."""

    def __init__(self):
        self.client = get_qdrant_client()
        self.collection_name = get_collection_name()
        # Initialize Cohere client for embedding generation
        from src.core.config import settings
        self.cohere_client = cohere.Client(settings.cohere_api_key)

    async def retrieve_contexts_by_text(
        self,
        query_text: str,
        top_k: int = DEFAULT_TOP_K,
        min_similarity: float = DEFAULT_MIN_SIMILARITY
    ) -> List[RetrievedContextModel]:
        """
        Retrieve relevant contexts from Qdrant based on the query text.

        Args:
            query_text: The text to search for in the vector database
            top_k: Number of top results to return
            min_similarity: Minimum similarity threshold for results

        Returns:
            List of RetrievedContextModel objects containing relevant content
        """
        try:
            logger.info(f"Retrieving contexts for query: {query_text[:50]}...")

            # Generate embedding for the query text using Cohere
            response = self.cohere_client.embed(
                texts=[query_text],
                model="embed-multilingual-v2.0"  # Cohere embedding model
            )
            query_vector = response.embeddings[0]

            # Use Qdrant's search functionality with the generated vector
            search_result = self.client.search_points(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                score_threshold=min_similarity,
                with_payload=True  # Include payload in results
            )

            # Convert the search results to RetrievedContextModel objects
            retrieved_contexts = []
            for result in search_result:
                if result.score >= min_similarity:
                    # Extract content from payload
                    payload = result.payload or {}
                    retrieved_context = RetrievedContextModel(
                        content=payload.get('content', ''),
                        source_chapter=payload.get('source_chapter', 'Unknown'),
                        source_section=payload.get('source_section', 'Unknown'),
                        source_page=payload.get('source_page'),
                        similarity_score=result.score,
                        chunk_id=result.id
                    )
                    retrieved_contexts.append(retrieved_context)

            logger.info(f"Retrieved {len(retrieved_contexts)} contexts for query")
            return retrieved_contexts

        except Exception as e:
            logger.error(f"Error during context retrieval: {str(e)}")
            raise RetrievalException(f"Failed to retrieve contexts: {str(e)}")

    async def retrieve_contexts_by_vector(
        self,
        query_vector: List[float],
        top_k: int = DEFAULT_TOP_K,
        min_similarity: float = DEFAULT_MIN_SIMILARITY
    ) -> List[RetrievedContextModel]:
        """
        Retrieve relevant contexts from Qdrant using a pre-computed vector.

        Args:
            query_vector: The embedding vector to search for in the vector database
            top_k: Number of top results to return
            min_similarity: Minimum similarity threshold for results

        Returns:
            List of RetrievedContextModel objects containing relevant content
        """
        try:
            logger.info(f"Retrieving contexts using vector query")

            # Use Qdrant's search functionality with the provided vector
            search_result = self.client.search_points(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                score_threshold=min_similarity,
                with_payload=True  # Include payload in results
            )

            # Convert the search results to RetrievedContextModel objects
            retrieved_contexts = []
            for result in search_result:
                if result.score >= min_similarity:
                    # Extract content from payload
                    payload = result.payload or {}
                    retrieved_context = RetrievedContextModel(
                        content=payload.get('content', ''),
                        source_chapter=payload.get('source_chapter', 'Unknown'),
                        source_section=payload.get('source_section', 'Unknown'),
                        source_page=payload.get('source_page'),
                        similarity_score=result.score,
                        chunk_id=result.id
                    )
                    retrieved_contexts.append(retrieved_context)

            logger.info(f"Retrieved {len(retrieved_contexts)} contexts using vector query")
            return retrieved_contexts

        except Exception as e:
            logger.error(f"Error during vector-based context retrieval: {str(e)}")
            raise RetrievalException(f"Failed to retrieve contexts using vector: {str(e)}")


# Global instance of the service
retrieval_service = RetrievalService()