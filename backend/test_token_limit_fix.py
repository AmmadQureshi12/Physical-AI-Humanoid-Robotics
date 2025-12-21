"""
Test script to verify the token limit fix is working properly.
This creates a long input text to test that token truncation is working.
"""
import asyncio
from src.utils.token_utils import get_token_count, truncate_text_to_token_limit, truncate_contexts_to_token_limit
from src.database.models import RetrievedContext as RetrievedContextModel


def test_token_counting():
    """Test basic token counting functionality"""
    print("Testing token counting...")
    text = "This is a test sentence. " * 10
    tokens = get_token_count(text)
    print(f"Token count for '{text[:50]}...': {tokens}")
    return tokens


def test_text_truncation():
    """Test text truncation based on token limits"""
    print("\nTesting text truncation...")
    long_text = "This is a very long sentence. " * 1000  # This should exceed any reasonable token limit
    print(f"Original text length: {len(long_text)} characters")

    # Count original tokens
    original_tokens = get_token_count(long_text)
    print(f"Original token count: {original_tokens}")

    # Truncate to 800 tokens
    max_tokens = 800
    truncated_text = truncate_text_to_token_limit(long_text, max_tokens)
    truncated_tokens = get_token_count(truncated_text)

    print(f"Truncated text length: {len(truncated_text)} characters")
    print(f"Truncated token count: {truncated_tokens}")
    print(f"Within limit: {truncated_tokens <= max_tokens}")

    return truncated_tokens <= max_tokens


def test_context_truncation():
    """Test context truncation based on token limits"""
    print("\nTesting context truncation...")

    # Create a list of contexts
    contexts = []
    for i in range(5):
        context = RetrievedContextModel(
            content=f"This is context {i} with a lot of content. " * 500,  # Each context is quite long
            source_chapter=f"Chapter {i}",
            source_section=f"Section {i}.{i}",
            source_page=i+1,
            similarity_score=0.8,
            chunk_id=f"chunk_{i}"
        )
        contexts.append(context)

    question = "This is a sample question that will be added to the prompt. " * 5

    # Count total tokens before truncation
    question_tokens = get_token_count(question)
    context_tokens = sum(get_token_count(ctx.content) for ctx in contexts)
    total_before = question_tokens + context_tokens

    print(f"Question tokens: {question_tokens}")
    print(f"Context tokens before: {context_tokens}")
    print(f"Total tokens before: {total_before}")

    # Truncate contexts
    max_total = 1000
    truncated_contexts = truncate_contexts_to_token_limit(contexts, max_total, question)

    # Count tokens after truncation
    new_context_tokens = sum(get_token_count(ctx.content) for ctx in truncated_contexts)
    total_after = question_tokens + new_context_tokens

    print(f"Context tokens after: {new_context_tokens}")
    print(f"Total tokens after: {total_after}")
    print(f"Within limit: {total_after <= max_total}")

    return total_after <= max_total


async def main():
    print("Testing token limit fixes...")

    # Test basic functionality
    test_token_counting()

    # Test text truncation
    text_truncation_ok = test_text_truncation()

    # Test context truncation
    context_truncation_ok = test_context_truncation()

    print(f"\nResults:")
    print(f"Text truncation working: {text_truncation_ok}")
    print(f"Context truncation working: {context_truncation_ok}")

    if text_truncation_ok and context_truncation_ok:
        print("\n[SUCCESS] Token limit fix is working correctly!")
    else:
        print("\n[ERROR] Token limit fix has issues!")


if __name__ == "__main__":
    asyncio.run(main())