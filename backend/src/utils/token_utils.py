"""
Utility functions for token counting and management.
"""
import cohere
from src.core.config import settings


def get_token_count(text: str) -> int:
    """
    Get the approximate number of tokens in the text.

    Args:
        text: The text to count tokens for

    Returns:
        The number of tokens in the text
    """
    # Initialize a temporary client just for tokenization
    try:
        client = cohere.Client(settings.cohere_api_key)
        # Use the cohere client's tokenize method to get token count
        response = client.tokenize(text=text, model=settings.model_name)
        return len(response.tokens)
    except Exception as e:
        # If tokenization fails, provide a rough estimate
        # This is a rough approximation (about 4 chars per token)
        # This fallback is conservative to avoid hitting limits
        estimated_tokens = len(text) // 4
        return estimated_tokens


def truncate_text_to_token_limit(text: str, max_tokens: int) -> str:
    """
    Truncate text to fit within a token limit.

    Args:
        text: The text to truncate
        max_tokens: The maximum number of tokens allowed

    Returns:
        The truncated text
    """
    current_tokens = get_token_count(text)

    # If we're already within the limit, return the original text
    if current_tokens <= max_tokens:
        return text

    # Start with a conservative estimate to reduce iterations
    start_ratio = max_tokens / current_tokens
    estimate_length = int(len(text) * start_ratio)

    # Ensure we have at least a small portion of text
    if estimate_length < 100:
        return text[:100]

    # Binary search approach to find the right size
    left, right = 100, estimate_length  # Start with the estimate as upper bound

    best_text = text[:estimate_length]

    while left <= right:
        mid = (left + right) // 2
        truncated_text = text[:mid]
        token_count = get_token_count(truncated_text)

        if token_count <= max_tokens:
            best_text = truncated_text
            left = mid + 1  # Try for a longer text
        else:
            right = mid - 1  # Text is too long, reduce it

    return best_text


def truncate_contexts_to_token_limit(contexts: list, max_total_tokens: int, question: str) -> list:
    """
    Truncate a list of contexts to fit within a total token limit.

    Args:
        contexts: List of context strings
        max_total_tokens: The maximum total tokens allowed for all contexts
        question: The question that will be added to the prompt

    Returns:
        List of truncated context strings
    """
    # Calculate token counts for the question
    question_tokens = get_token_count(question)

    # Calculate token counts for all context content
    context_tokens = []
    for ctx in contexts:
        content = ctx.content if hasattr(ctx, 'content') else str(ctx)
        token_count = get_token_count(content)
        context_tokens.append(token_count)

    total_context_tokens = sum(context_tokens)

    # Check if the total (question + contexts) is within the limit
    if question_tokens + total_context_tokens <= max_total_tokens:
        return contexts

    # Calculate how many tokens we can allocate to contexts
    available_context_tokens = max_total_tokens - question_tokens

    # If we can't even fit the question, return empty contexts
    if available_context_tokens <= 0:
        return []

    # Calculate the reduction factor
    reduction_factor = available_context_tokens / total_context_tokens

    # Ensure we don't reduce below a reasonable minimum
    reduction_factor = min(1.0, max(0.01, reduction_factor))

    truncated_contexts = []
    for i, ctx in enumerate(contexts):
        if hasattr(ctx, 'content'):
            # Calculate the new token count for this context
            new_context_tokens = max(1, int(context_tokens[i] * reduction_factor))

            # Convert token count back to character count (approximation)
            original_content = ctx.content
            original_tokens = context_tokens[i]

            if original_tokens == 0:
                new_content = original_content
            else:
                # Calculate the proportion of characters to keep
                char_ratio = new_context_tokens / original_tokens
                new_length = max(10, int(len(original_content) * char_ratio))
                new_content = original_content[:new_length]

            # Create a new context object with the truncated content
            new_ctx = type(ctx)(
                content=new_content,
                source_chapter=getattr(ctx, 'source_chapter', ''),
                source_section=getattr(ctx, 'source_section', ''),
                source_page=getattr(ctx, 'source_page', None),
                similarity_score=getattr(ctx, 'similarity_score', 0.0),
                chunk_id=getattr(ctx, 'chunk_id', '')
            )
            truncated_contexts.append(new_ctx)
        else:
            # If it's just a string, truncate it based on the reduction factor
            original_content = str(ctx)
            original_tokens = get_token_count(original_content)
            new_tokens = max(1, int(original_tokens * reduction_factor))

            # Convert token count back to character count
            if original_tokens == 0:
                new_content = original_content
            else:
                char_ratio = new_tokens / original_tokens
                new_length = max(10, int(len(original_content) * char_ratio))
                new_content = original_content[:new_length]

            truncated_contexts.append(new_content)

    return truncated_contexts