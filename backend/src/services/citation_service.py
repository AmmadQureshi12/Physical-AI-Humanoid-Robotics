"""
Citation service to generate APA-formatted citations.
"""
from typing import List
from src.database.models import Citation as CitationModel, RetrievedContext
from src.core.exceptions import CitationException
from src.core.logging_config import get_logger
from src.core.config import settings


logger = get_logger(__name__)


class CitationService:
    """Service to handle citation generation in APA format."""
    
    def __init__(self):
        self.book_title = settings.book_title
        self.book_author = settings.book_author
        self.book_year = settings.book_publication_year
    
    def generate_citation_from_context(
        self, 
        context: RetrievedContext
    ) -> CitationModel:
        """
        Generate an APA-formatted citation from a retrieved context.
        
        Args:
            context: The retrieved context to generate a citation for
            
        Returns:
            CitationModel object with APA-formatted citation
        """
        try:
            # Construct APA citation based on available context information
            if context.source_page:
                apa_text = f"{self.book_author}. ({self.book_year}). {self.book_title}. {context.source_chapter}, {context.source_section}, p. {context.source_page}."
            else:
                apa_text = f"{self.book_author}. ({self.book_year}). {self.book_title}. {context.source_chapter}, {context.source_section}."
            
            citation = CitationModel(
                apa_text=apa_text,
                source_chapter=context.source_chapter,
                source_section=context.source_section,
                source_page=context.source_page,
                quoted_text=context.content[:200] + "..." if len(context.content) > 200 else context.content  # First 200 chars as sample
            )
            
            return citation
            
        except Exception as e:
            logger.error(f"Error generating citation from context: {str(e)}")
            raise CitationException(f"Failed to generate citation from context: {str(e)}")
    
    def generate_citations_from_contexts(
        self, 
        contexts: List[RetrievedContext]
    ) -> List[CitationModel]:
        """
        Generate APA-formatted citations from a list of retrieved contexts.
        
        Args:
            contexts: List of retrieved contexts to generate citations for
            
        Returns:
            List of CitationModel objects
        """
        citations = []
        for context in contexts:
            citation = self.generate_citation_from_context(context)
            citations.append(citation)
        
        return citations
    
    def validate_citation_format(self, citation_text: str) -> bool:
        """
        Validate that a citation is in proper APA format.
        
        Args:
            citation_text: The citation text to validate
            
        Returns:
            True if valid APA format, False otherwise
        """
        # Basic validation: check if it has author, year, and title elements
        # This is a simplified check - a full implementation would be more thorough
        has_author_year = '(' in citation_text and ')' in citation_text
        has_title = self.book_title.lower() in citation_text.lower()
        
        return has_author_year and has_title


# Global instance of the service
citation_service = CitationService()