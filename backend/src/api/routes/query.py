"""
Query endpoint implementation and API models/schemas matching OpenAPI contract in query-api.yaml
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from src.services.rag_service import rag_service
from src.core.exceptions import AppBaseException
from src.core.logging_config import get_logger


logger = get_logger(__name__)
router = APIRouter()


class QuestionRequest(BaseModel):
    """Request model for the question endpoint."""
    question: str = Field(..., example="What are the main principles of AI-native development?")
    selected_text: Optional[str] = Field(
        None,
        description="Optional text selected by the user for selected-text-only mode",
        example="AI-native development involves building systems from the ground up with AI as a core component rather than an afterthought."
    )
    session_id: str = Field(
        ...,
        description="Unique identifier for the conversation session",
        example="sess-12345-abcde"
    )
    page_metadata: Optional[dict] = Field(
        None,
        description="Metadata about the book page where the question originated",
        example={
            "chapter": "Chapter 3",
            "section": "3.2",
            "url": "https://book.example.com/chapter-3#section-3.2"
        }
    )


class Citation(BaseModel):
    """Model for citations in the response."""
    apa_text: str = Field(..., example="Author, A. (2024). Title of Book. Publisher. Chapter 3.")
    source_chapter: str = Field(..., example="Chapter 3")
    source_section: str = Field(..., example="3.2")
    pages: Optional[List[int]] = Field(None, example=[45, 47])


class RetrievedContext(BaseModel):
    """Model for retrieved context in the response."""
    content: str = Field(
        ...,
        example="The concept of AI-native development involves building systems from the ground up with AI as a core component rather than an afterthought..."
    )
    source: str = Field(..., example="Chapter 3, Section 3.2, Pages 45-47")
    similarity_score: float = Field(..., ge=0.0, le=1.0, example=0.87)


class QuestionResponse(BaseModel):
    """Response model for the question endpoint."""
    answer: str = Field(
        ...,
        example="AI-native development involves building systems from the ground up with AI as a core component rather than an afterthought. This approach ensures that AI capabilities are deeply integrated into the system architecture. [Citation: Author, 2024, Chapter 3]"
    )
    citations: List[Citation]
    retrieved_contexts: List[RetrievedContext]
    selected_text_mode: bool = Field(..., example=False)
    model_used: str = Field(..., example="qwen-7b")
    validation_passed: bool = Field(default=True, example=True)


class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str = Field(..., example="INTERNAL_ERROR")
    message: str = Field(..., example="An internal error occurred while processing the request")


class InsufficientContentResponse(BaseModel):
    """Model for responses when content is insufficient."""
    message: str = Field(
        ...,
        example="The provided sources do not contain sufficient information to answer this question."
    )


class HealthResponse(BaseModel):
    """Model for health check responses."""
    status: str = Field(..., example="healthy")
    timestamp: str = Field(..., example="2023-12-16T10:30:00Z")
    details: Optional[dict] = Field(
        None,
        example={
            "database": "connected",
            "vector_db": "connected",
            "llm_provider": "available"
        }
    )


@router.post("/query",
             summary="Process a user question and return a RAG-enhanced response",
             description="""
             Accepts a user's question about the academic book content and returns a response generated using Retrieval-Augmented Generation.
             The response strictly adheres to the academic constitution, using only retrieved context or user-selected text.
             """,
             response_model=QuestionResponse,
             responses={
                 200: {"description": "Successfully processed query with response"},
                 400: {"model": ErrorResponse, "description": "Bad request - invalid input parameters"},
                 422: {"model": InsufficientContentResponse, "description": "Unprocessable Entity - content insufficient for answer"},
                 429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
async def process_query(request: QuestionRequest):
    """
    Process a user question and return a RAG-enhanced response.

    Args:
        request: QuestionRequest containing the question and optional selected text

    Returns:
        QuestionResponse containing the answer, citations, and other metadata
    """
    try:
        logger.info(f"Received query: {request.question[:50]}...")

        # Process the query through the RAG service
        result = await rag_service.process_query(
            question=request.question,
            selected_text=request.selected_text
        )

        logger.info(f"Successfully processed query for session {request.session_id}")
        return result

    except HTTPException:
        # Re-raise HTTP exceptions (like rate limiting)
        raise
    except AppBaseException as e:
        # Handle application-specific exceptions
        logger.error(f"Application error during query processing: {e.message}")
        raise HTTPException(
            status_code=422 if "insufficient" in e.message.lower() else 500,
            detail={
                "error": e.error_code,
                "message": e.message
            }
        )
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error during query processing: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "INTERNAL_ERROR",
                "message": "An internal error occurred while processing the request"
            }
        )