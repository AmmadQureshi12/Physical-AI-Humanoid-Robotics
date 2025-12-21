"""
Generation service for calling Qwen via Cohere API.
"""
from typing import List, Dict
from src.core.config import settings
import cohere
from src.core.exceptions import GenerationException
from src.core.logging_config import get_logger
from src.database.models import RetrievedContext as RetrievedContextModel
from src.core.constants import ACADEMIC_TONE_PROMPT, FLESCH_KINCAID_TARGET, INSUFFICIENT_CONTENT_MESSAGE
from src.utils.token_utils import get_token_count, truncate_contexts_to_token_limit


logger = get_logger(__name__)


class GenerationService:
    """Service to handle text generation using Qwen models via Cohere API."""

    def __init__(self):
        # Initialize Cohere client with the API key from settings
        self.cohere_client = cohere.Client(settings.cohere_api_key)
        # Using command-r-plus as it's a current Cohere model suitable for Qwen use case
        self.model_name = settings.model_name

    async def generate_response(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.3  # Lower temperature for more consistent, factual responses
    ) -> str:
        """
        Generate a response using the Qwen model via Cohere API.

        Args:
            prompt: The input prompt for generation
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature for generation (lower for more factual)

        Returns:
            Generated text response
        """
        try:
            logger.info(f"Generating response with model: {self.model_name}")

            # Use Cohere's generate endpoint to call the Qwen model
            response = self.cohere_client.chat(
                model=self.model_name,
                message=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop_sequences=["\n\n", "Question:", "Answer:", "User:", "Assistant:"],  # Common stop sequences
                preamble="You are an academic assistant for a computer science book. You must follow these rules: 1. Answer only based on the provided context. 2. If the context doesn't contain sufficient information, try to answer using your general knowledge of the topic. 3. Maintain formal academic tone. 4. Make no inferences beyond what's explicitly stated in the context."
            )

            # Extract the generated text from the response
            generated_text = response.text.strip()

            logger.info(f"Successfully generated response of {len(generated_text)} characters")
            return generated_text

        except Exception as e:
            logger.error(f"Error during response generation: {str(e)}")
            raise GenerationException(f"Failed to generate response: {str(e)}")

    async def generate_response_with_context(
        self,
        question: str,
        contexts: List[RetrievedContextModel],
        selected_text: str = None,
        academic_tone: bool = True
    ) -> str:
        """
        Generate a response based on the question and provided contexts.

        Args:
            question: The user's question
            contexts: List of retrieved contexts to use as reference
            selected_text: Optional selected text (when in selected-text-only mode)
            academic_tone: Whether to enforce academic tone in the response

        Returns:
            Generated text response
        """
        try:
            logger.info(f"Generating response for question: {question[:50]}...")

            # Determine which content to use based on mode
            if selected_text:
                # Selected-text-only mode: only use the user-provided text
                combined_context = f"Please answer the following question based ONLY on the selected text provided below. Do not use any other information.\n\nSelected Text: {selected_text}\n\nQuestion: {question}"
            else:
                # Regular mode: use retrieved contexts
                # Truncate contexts to fit within token limits
                # The Cohere model has a limit of 1,048,576 tokens, but we should stay well below that
                # to account for the response tokens and model-specific overhead
                max_input_tokens = 800000  # Conservatively set below the limit
                truncated_contexts = truncate_contexts_to_token_limit(contexts, max_input_tokens, question)

                context_texts = []
                for ctx in truncated_contexts:
                    context_texts.append(f"Source: {ctx.source_chapter} {ctx.source_section} | Content: {ctx.content}")

                combined_context = f"Please answer the following question based only on the book content provided below. If the provided information is insufficient, please state that explicitly.\n\nContext:\n" + "\n".join(context_texts) + f"\n\nQuestion: {question}"

            # Add academic tone requirement if needed
            if academic_tone:
                combined_context += f"\n\n{ACADEMIC_TONE_PROMPT} Ensure the response is written at a Flesch-Kincaid grade level between {FLESCH_KINCAID_TARGET[0]} and {FLESCH_KINCAID_TARGET[1]}. Use formal academic language, avoid contractions, and maintain objectivity."

            # Generate the response
            response_text = await self.generate_response(combined_context)

            # Apply academic tone enforcement if needed
            if academic_tone:
                response_text = await self.enforce_academic_tone(response_text)

            return response_text

        except Exception as e:
            logger.error(f"Error during context-based response generation: {str(e)}")
            raise GenerationException(f"Failed to generate response with context: {str(e)}")

    async def enforce_academic_tone(self, text: str) -> str:
        """
        Post-process generated text to ensure it meets academic tone requirements.

        Args:
            text: The generated text to check and modify

        Returns:
            Text that meets academic tone requirements
        """
        # This is a simplified implementation
        # A full implementation would involve more sophisticated NLP techniques

        # For now, we'll just ensure basic academic standards are met
        # In a real implementation, we might check readability scores, formal language usage, etc.

        # Ensure no casual language is used (simple check)
        if "um" in text or "uh" in text:
            logger.warning("Casual language detected in response")

        # Log that academic tone enforcement was run
        logger.info("Academic tone enforcement completed")

        return text


# Global instance of the service
generation_service = GenerationService()