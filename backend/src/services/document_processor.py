"""
Document processing service to index book content into the vector database.
"""
import asyncio
from typing import List, Dict, Any
from pathlib import Path
import hashlib
import uuid
from src.core.qdrant_client import get_qdrant_client, get_collection_name
from src.database.models import BookContent
from src.core.exceptions import AppBaseException
from src.core.logging_config import get_logger
from src.core.config import settings
import cohere
import PyPDF2
import docx


logger = get_logger(__name__)


class DocumentProcessor:
    """Service to process documents and index them into the vector database."""

    def __init__(self):
        self.client = get_qdrant_client()
        self.collection_name = get_collection_name()
        # Initialize Cohere client for embedding generation
        self.cohere_client = cohere.Client(settings.cohere_api_key)

    async def process_and_index_book_content(
        self,
        book_content: List[Dict[str, Any]]
    ) -> bool:
        """
        Process and index book content into the vector database.

        Args:
            book_content: List of book content chunks with metadata

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Starting to process and index {len(book_content)} book content chunks")

            # Prepare points for Qdrant
            points = []
            for idx, content_chunk in enumerate(book_content):
                # Generate embedding for the content
                response = self.cohere_client.embed(
                    texts=[content_chunk['content']],
                    model="embed-multilingual-v2.0"  # Cohere embedding model
                )
                embedding = response.embeddings[0]

                # Create a unique ID for the chunk
                content_hash = hashlib.md5(content_chunk['content'].encode()).hexdigest()
                chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, content_hash))

                # Prepare the payload with content and metadata
                payload = {
                    "content": content_chunk['content'],
                    "source_chapter": content_chunk.get('chapter_title', 'Unknown'),
                    "source_section": content_chunk.get('section_number', 'Unknown'),
                    "source_page": content_chunk.get('page_start', None)
                }

                # Create a Qdrant point
                point = {
                    "id": chunk_id,
                    "vector": embedding,
                    "payload": payload
                }

                points.append(point)

            # Upsert all points to Qdrant collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully indexed {len(points)} content chunks into Qdrant collection: {self.collection_name}")
            return True

        except Exception as e:
            logger.error(f"Error during document processing and indexing: {str(e)}")
            raise AppBaseException(f"Failed to process and index document: {str(e)}")

    async def process_file_for_indexing(
        self,
        file_path: str,
        chapter_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Process a single file and return a list of content chunks ready for indexing.

        Args:
            file_path: Path to the file to process
            chapter_info: Metadata about the chapter

        Returns:
            List of content chunks with metadata
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == ".pdf":
            return await self._process_pdf_file(file_path, chapter_info)
        elif file_ext == ".txt":
            return await self._process_text_file(file_path, chapter_info)
        elif file_ext == ".docx":
            return await self._process_docx_file(file_path, chapter_info)
        elif file_ext == ".md":
            return await self._process_markdown_file(file_path, chapter_info)
        else:
            raise AppBaseException(f"Unsupported file format: {file_ext}")

    async def _process_pdf_file(
        self,
        file_path: str,
        chapter_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Process a PDF file into content chunks."""
        content_chunks = []
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    
                    # Split page text into chunks at paragraph boundaries
                    paragraphs = page_text.split('\n\n')
                    
                    for para_idx, paragraph in enumerate(paragraphs):
                        if paragraph.strip():  # Skip empty paragraphs
                            chunk = {
                                "content": paragraph.strip(),
                                "chapter_number": chapter_info.get('chapter_number', 0),
                                "chapter_title": chapter_info.get('chapter_title', 'Unknown'),
                                "section_number": chapter_info.get('section_number', f"{page_num + 1}.{para_idx + 1}"),
                                "section_title": chapter_info.get('section_title', ''),
                                "page_start": page_num + 1,
                                "page_end": page_num + 1
                            }
                            content_chunks.append(chunk)
        except Exception as e:
            logger.error(f"Error processing PDF file {file_path}: {str(e)}")
            raise AppBaseException(f"Failed to process PDF file: {str(e)}")
        
        return content_chunks

    async def _process_text_file(
        self,
        file_path: str,
        chapter_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Process a text file into content chunks."""
        content_chunks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Split content into chunks at paragraph boundaries
                paragraphs = content.split('\n\n')
                
                for para_idx, paragraph in enumerate(paragraphs):
                    if paragraph.strip():  # Skip empty paragraphs
                        chunk = {
                            "content": paragraph.strip(),
                            "chapter_number": chapter_info.get('chapter_number', 0),
                            "chapter_title": chapter_info.get('chapter_title', 'Unknown'),
                            "section_number": chapter_info.get('section_number', f"1.{para_idx + 1}"),
                            "section_title": chapter_info.get('section_title', ''),
                            "page_start": 1,  # Text files don't have clear page breaks
                            "page_end": 1
                        }
                        content_chunks.append(chunk)
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {str(e)}")
            raise AppBaseException(f"Failed to process text file: {str(e)}")
        
        return content_chunks

    async def _process_docx_file(
        self,
        file_path: str,
        chapter_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Process a DOCX file into content chunks."""
        content_chunks = []
        
        try:
            doc = docx.Document(file_path)
            
            # Collect all paragraphs
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            
            for para_idx, paragraph in enumerate(paragraphs):
                if paragraph.strip():  # Skip empty paragraphs
                    chunk = {
                        "content": paragraph.strip(),
                        "chapter_number": chapter_info.get('chapter_number', 0),
                        "chapter_title": chapter_info.get('chapter_title', 'Unknown'),
                        "section_number": chapter_info.get('section_number', f"1.{para_idx + 1}"),
                        "section_title": chapter_info.get('section_title', ''),
                        "page_start": 1,  # DOCX files don't have clear page breaks in this implementation
                        "page_end": 1
                    }
                    content_chunks.append(chunk)
        except Exception as e:
            logger.error(f"Error processing DOCX file {file_path}: {str(e)}")
            raise AppBaseException(f"Failed to process DOCX file: {str(e)}")
        
        return content_chunks

    async def _process_markdown_file(
        self,
        file_path: str,
        chapter_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Process a Markdown file into content chunks."""
        content_chunks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Split content into chunks - could be by headers or paragraphs
                # For now, splitting on double newlines
                parts = content.split('\n\n')
                
                for part_idx, part in enumerate(parts):
                    if part.strip():  # Skip empty parts
                        chunk = {
                            "content": part.strip(),
                            "chapter_number": chapter_info.get('chapter_number', 0),
                            "chapter_title": chapter_info.get('chapter_title', 'Unknown'),
                            "section_number": chapter_info.get('section_number', f"1.{part_idx + 1}"),
                            "section_title": chapter_info.get('section_title', ''),
                            "page_start": 1,  # Markdown files don't have clear page breaks
                            "page_end": 1
                        }
                        content_chunks.append(chunk)
        except Exception as e:
            logger.error(f"Error processing Markdown file {file_path}: {str(e)}")
            raise AppBaseException(f"Failed to process Markdown file: {str(e)}")
        
        return content_chunks

    async def clear_collection(self) -> bool:
        """
        Delete the Qdrant collection.

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Deleting collection: {self.collection_name}")
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info(f"Successfully deleted collection: {self.collection_name}")
            return True
        except Exception as e:
            # It's possible the collection doesn't exist, which is fine.
            if "not found" in str(e).lower():
                logger.info(f"Collection {self.collection_name} does not exist, nothing to delete.")
                return True
            logger.error(f"Error deleting collection: {str(e)}")
            raise AppBaseException(f"Failed to delete collection: {str(e)}")


# Global instance of the service
document_processor = DocumentProcessor()