"""
RAG service to orchestrate retrieval and generation.
"""
from typing import List, Optional
from src.services.retrieval_service import retrieval_service
from src.services.generation_service import generation_service
from src.services.citation_service import citation_service
from src.services.validation_service import validation_service
from src.database.models import RetrievedContext as RetrievedContextModel, Citation as CitationModel
from src.core.exceptions import RAGException
from src.core.logging_config import get_logger
from src.core.constants import INSUFFICIENT_CONTENT_MESSAGE
from src.utils.token_utils import truncate_contexts_to_token_limit


logger = get_logger(__name__)


class RAGService:
    """Service to orchestrate retrieval and generation for the RAG system."""

    def __init__(self):
        self.retrieval_service = retrieval_service
        self.generation_service = generation_service
        self.citation_service = citation_service
        self.validation_service = validation_service

    async def process_query(
        self,
        question: str,
        selected_text: Optional[str] = None,
        top_k: int = 5,
        min_similarity: float = 0.3
    ) -> dict:
        """
        Process a user query through the RAG pipeline.

        Args:
            question: The user's question
            selected_text: Optional selected text for selected-text-only mode
            top_k: Number of top contexts to retrieve
            min_similarity: Minimum similarity threshold for retrieval

        Returns:
            Dictionary containing the answer, citations, and other metadata
        """
        try:
            logger.info(f"Processing query: {question[:50]}...")

            # Validate inputs
            self.validation_service.validate_question(question)
            self.validation_service.validate_selected_text(selected_text)

            # Determine if we're in selected-text-only mode
            selected_text_mode = selected_text is not None and selected_text.strip() != ""

            # Retrieve relevant contexts
            contexts = []
            if selected_text_mode:
                # In selected-text-only mode, we don't retrieve from the vector database
                # just use the selected text as context
                logger.info("Using selected-text-only mode")
                # Create a synthetic context from the selected text
                contexts = [
                    RetrievedContextModel(
                        content=selected_text,
                        source_chapter="Selected Text",
                        source_section="User Selection",
                        source_page=None,
                        similarity_score=1.0,  # Perfect match since it's the exact text
                        chunk_id="selected_text"
                    )
                ]
            else:
                # In normal mode, retrieve contexts from the vector database
                logger.info("Using normal retrieval mode")
                contexts = await self.retrieval_service.retrieve_contexts_by_text(
                    query_text=question,
                    top_k=top_k,
                    min_similarity=min_similarity
                )

            # Validate retrieved contexts
            self.validation_service.validate_retrieved_contexts(contexts)

            # If no contexts were found, return the insufficient content message
            if not contexts:
                logger.info("No relevant contexts found, returning insufficient content message")
                return {
                    "answer": INSUFFICIENT_CONTENT_MESSAGE,
                    "citations": [],
                    "retrieved_contexts": [],
                    "selected_text_mode": selected_text_mode,
                    "model_used": generation_service.model_name,
                    "validation_passed": True
                }

            # Truncate contexts to prevent token limit errors before passing to generation service
            if not selected_text_mode and len(contexts) > 0:
                # The Cohere model has a limit of 1,048,576 tokens, but we should stay well below that
                # to account for the response tokens and model-specific overhead
                max_input_tokens = 800000  # Conservatively set below the limit
                contexts = truncate_contexts_to_token_limit(contexts, max_input_tokens, question)

            # Generate the response based on the question and contexts
            answer = await self.generation_service.generate_response_with_context(
                question=question,
                contexts=contexts,
                selected_text=selected_text if selected_text_mode else None
            )

            # Validate the generated response
            self.validation_service.validate_response_content(
                response=answer,
                contexts=contexts,
                selected_text_mode=selected_text_mode,
                selected_text=selected_text
            )

            # Validate zero hallucination policy
            self.validation_service.validate_zero_hallucination_policy(
                response=answer,
                contexts=contexts,
                selected_text=selected_text
            )

            # Generate citations based on the contexts used
            citations = self.citation_service.generate_citations_from_contexts(contexts)

            # Create the response dictionary
            result = {
                "answer": answer,
                "citations": [cit for cit in citations],
                "retrieved_contexts": [
                    {
                        "content": ctx.content,
                        "source": f"{ctx.source_chapter}, {ctx.source_section}" + (f", Page {ctx.source_page}" if ctx.source_page else ""),
                        "similarity_score": ctx.similarity_score
                    }
                    for ctx in contexts
                ],
                "selected_text_mode": selected_text_mode,
                "model_used": generation_service.model_name,
                "validation_passed": True
            }

            logger.info(f"Successfully processed query, generated answer of {len(answer)} characters")
            return result

        except Exception as e:
            logger.error(f"Error during RAG processing: {str(e)}")
            raise RAGException(f"Failed to process query: {str(e)}")


# Global instance of the service
rag_service = RAGService()