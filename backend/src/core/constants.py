"""
Core constants module for application-wide constants.
"""

# API Response Constants
INSUFFICIENT_CONTENT_MESSAGE = "The provided sources do not contain sufficient information to answer this question."
ACADEMIC_TONE_PROMPT = "Maintain a formal academic tone suitable for computer science researchers and graduate students."
FLESCH_KINCAID_TARGET = (10, 12)  # Grade level range
MAX_RESPONSE_TIME = 10  # seconds

# Database Constants
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# RAG Constants
DEFAULT_TOP_K = 5
DEFAULT_MIN_SIMILARITY = 0.3
DEFAULT_EMBEDDING_DIMENSION = 768  # For Cohere embeddings

# Validation Constants
MAX_QUESTION_LENGTH = 2000  # characters
MAX_SELECTED_TEXT_LENGTH = 10000  # characters
MAX_RESPONSE_TOKENS = 1000

# Service Constants
COHERE_TIMEOUT = 30  # seconds
QDRANT_TIMEOUT = 10  # seconds
DATABASE_TIMEOUT = 5  # seconds

# Content Constants
BOOK_CONTENT_SOURCE = "book"
SELECTED_TEXT_SOURCE = "selected_text"
SUPPORTED_FILE_FORMATS = [".pdf", ".txt", ".md", ".docx"]

# Logging Constants
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Model Constants
QWEN_MODEL_FAMILY = "qwen"
MODEL_TEMPERATURE = 0.7
MODEL_MAX_TOKENS = 500