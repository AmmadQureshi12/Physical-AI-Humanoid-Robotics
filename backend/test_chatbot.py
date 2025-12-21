"""
Test script for the RAG chatbot functionality.
"""
import pytest
import asyncio
import sys
import os

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.rag_service import rag_service
from src.services.document_processor import document_processor
from src.core.qdrant_initializer import initialize_qdrant_collection
from src.database.init_db import init_db


@pytest.fixture(scope="module", autouse=True)
async def setup_database_and_qdrant():
    """
    Fixture to set up the database and Qdrant collection before running tests.
    This runs once for the entire module.
    """
    print("\nStarting RAG chatbot tests setup...\n")
    print("Initializing database and vector store...")
    await document_processor.clear_collection()
    await init_db()
    initialize_qdrant_collection()
    print("Initialization completed\n")
    yield
    print("\nCleaning up after RAG chatbot tests...")
    await document_processor.clear_collection()
    print("Cleanup completed\n")


@pytest.mark.asyncio
async def test_basic_query():
    """Test basic query functionality."""
    result = await rag_service.process_query(
        question="What is the meaning of life according to this book?",
        selected_text=None
    )
    assert result is not None
    assert "answer" in result
    assert "selected_text_mode" in result
    assert "citations" in result
    assert "retrieved_contexts" in result
    assert result['selected_text_mode'] is False
    assert len(result['citations']) >= 0 # Or some expected value
    assert len(result['retrieved_contexts']) >= 0 # Or some expected value
    assert isinstance(result['answer'], str) and len(result['answer']) > 0


@pytest.mark.asyncio
async def test_selected_text_mode():
    """Test selected text only mode."""
    selected_text = "AI-native development involves building systems from the ground up with AI as a core component rather than an afterthought. This approach ensures that AI capabilities are deeply integrated into the system architecture."
    result = await rag_service.process_query(
        question="What is AI-native development?",
        selected_text=selected_text
    )
    assert result is not None
    assert "answer" in result
    assert "selected_text_mode" in result
    assert result['selected_text_mode'] is True
    assert isinstance(result['answer'], str) and len(result['answer']) > 0


@pytest.mark.asyncio
async def test_document_processing():
    """Test document processing functionality."""
    # Sample book content to index
    book_content = [
        {
            "content": "AI-native development involves building systems from the ground up with AI as a core component rather than an afterthought. This approach ensures that AI capabilities are deeply integrated into the system architecture.",
            "chapter_number": 1,
            "chapter_title": "Introduction to AI-Native Development",
            "section_number": "1.1",
            "section_title": "Defining AI-Native",
            "page_start": 1,
            "page_end": 3
        },
        {
            "content": "The architecture of AI-native systems differs significantly from traditional software. These systems are designed to continuously learn and adapt based on new data inputs.",
            "chapter_number": 2,
            "chapter_title": "Architecture Patterns",
            "section_number": "2.1",
            "section_title": "Designing for Adaptability",
            "page_start": 15,
            "page_end": 18
        }
    ]
    
    # Process and index the content
    success = await document_processor.process_and_index_book_content(book_content)
    assert success is True