"""
Exception handling module with custom application exceptions.
"""


class AppBaseException(Exception):
    """Base application exception."""
    def __init__(self, message: str, error_code: str = "APP_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class RAGException(AppBaseException):
    """Exception related to RAG operations."""
    def __init__(self, message: str):
        super().__init__(message, "RAG_ERROR")


class RetrievalException(AppBaseException):
    """Exception related to retrieval operations."""
    def __init__(self, message: str):
        super().__init__(message, "RETRIEVAL_ERROR")


class GenerationException(AppBaseException):
    """Exception related to generation operations."""
    def __init__(self, message: str):
        super().__init__(message, "GENERATION_ERROR")


class ValidationException(AppBaseException):
    """Exception related to validation operations."""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class CitationException(AppBaseException):
    """Exception related to citation operations."""
    def __init__(self, message: str):
        super().__init__(message, "CITATION_ERROR")


class ConfigurationException(AppBaseException):
    """Exception related to configuration issues."""
    def __init__(self, message: str):
        super().__init__(message, "CONFIG_ERROR")


class DatabaseException(AppBaseException):
    """Exception related to database operations."""
    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR")


class ExternalServiceException(AppBaseException):
    """Exception related to external service calls."""
    def __init__(self, message: str, service_name: str = "EXTERNAL_SERVICE"):
        error_code = f"{service_name.upper()}_ERROR"
        super().__init__(message, error_code)