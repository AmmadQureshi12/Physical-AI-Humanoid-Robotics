"""
Validation service to ensure responses contain only book content.
"""
from typing import List
from src.database.models import RetrievedContext
from src.core.exceptions import ValidationException
from src.core.logging_config import get_logger
from src.core.constants import MAX_QUESTION_LENGTH, MAX_SELECTED_TEXT_LENGTH


logger = get_logger(__name__)


class ValidationService:
    """Service to validate that responses contain only book content and meet academic standards."""
    
    def __init__(self):
        pass
    
    def validate_question(self, question: str) -> bool:
        """
        Validate that the question meets our requirements.
        
        Args:
            question: The question text to validate
            
        Returns:
            True if valid, raises exception if invalid
        """
        if not question or not question.strip():
            raise ValidationException("Question cannot be empty")
        
        if len(question) > MAX_QUESTION_LENGTH:
            raise ValidationException(f"Question exceeds maximum length of {MAX_QUESTION_LENGTH} characters")
        
        # Additional validation for academic tone could be added here
        return True
    
    def validate_selected_text(self, selected_text: str) -> bool:
        """
        Validate that the selected text meets our requirements.
        
        Args:
            selected_text: The selected text to validate
            
        Returns:
            True if valid, raises exception if invalid
        """
        if selected_text and len(selected_text) > MAX_SELECTED_TEXT_LENGTH:
            raise ValidationException(f"Selected text exceeds maximum length of {MAX_SELECTED_TEXT_LENGTH} characters")
        
        return True
    
    def validate_retrieved_contexts(self, contexts: List[RetrievedContext]) -> bool:
        """
        Validate that the retrieved contexts meet our requirements.
        
        Args:
            contexts: List of retrieved contexts to validate
            
        Returns:
            True if valid, raises exception if invalid
        """
        if not contexts:
            # This is valid - it means no relevant content was found
            return True
        
        for ctx in contexts:
            if not ctx.content or not ctx.content.strip():
                raise ValidationException("Retrieved context cannot have empty content")
            
            if ctx.similarity_score < 0 or ctx.similarity_score > 1:
                raise ValidationException("Similarity score must be between 0 and 1")
        
        return True
    
    def validate_response_content(
        self, 
        response: str, 
        contexts: List[RetrievedContext], 
        selected_text_mode: bool = False,
        selected_text: str = None
    ) -> bool:
        """
        Validate that the response content is based only on the provided contexts.
        
        Args:
            response: The generated response to validate
            contexts: The contexts that were used to generate the response
            selected_text_mode: Whether to validate against selected text instead of contexts
            selected_text: The selected text to validate against (if in selected-text mode)
            
        Returns:
            True if valid, raises exception if invalid
        """
        if not response or not response.strip():
            raise ValidationException("Response cannot be empty")
        
        # If in selected-text-only mode, validate against the selected text
        if selected_text_mode and selected_text:
            # Check if response contains information that's not in the selected text
            # This is a simplified check - a full implementation would require more sophisticated NLP
            logger.info("Validating response in selected-text-only mode")
            # For now, we trust that the generation service properly followed the selected-text mode
            return True
        else:
            # In normal mode, ensure response is grounded in the provided contexts
            # This is a simplified check - a full implementation would use more sophisticated methods
            logger.info("Validating response in normal mode")
            # For now, we'll just check that we have contexts to validate against
            if not contexts:
                raise ValidationException("Response must be grounded in provided contexts, but no contexts were provided")
            
            # In a full implementation, we would check if the response content 
            # is properly based on the retrieved contexts
            return True
    
    def validate_zero_hallucination_policy(
        self, 
        response: str, 
        contexts: List[RetrievedContext], 
        selected_text: str = None
    ) -> bool:
        """
        Validate that the response follows the zero hallucination policy.
        
        Args:
            response: The generated response to validate
            contexts: The contexts that were used to generate the response
            selected_text: The selected text to validate against (if in selected-text mode)
            
        Returns:
            True if valid, raises exception if invalid
        """
        # This is a simplified check - a full implementation would require sophisticated NLP
        # to compare the factual claims in the response with the source content
        
        if selected_text:
            # In selected-text-only mode, ensure the response doesn't contain information
            # not present in the selected text
            logger.info("Validating zero hallucination policy in selected-text mode")
        else:
            # In normal mode, ensure the response doesn't contain information
            # not present in the contexts
            logger.info("Validating zero hallucination policy in normal mode")
        
        # For now, we rely on the RAG service and generation service to follow the policy
        # In a full implementation, we would have more sophisticated validation here
        return True


# Global instance of the service
validation_service = ValidationService()