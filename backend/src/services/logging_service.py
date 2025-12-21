"""
Service to handle logging of queries and responses to Neon Postgres.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connection import get_db_session
from src.database.models import Question as QuestionModel, Answer as AnswerModel, LogEntry as LogEntryModel
from src.core.logging_config import get_logger
from src.core.exceptions import DatabaseException
from datetime import datetime


logger = get_logger(__name__)


class LoggingService:
    """Service to handle logging of interactions to the database."""
    
    async def log_query(
        self,
        session: AsyncSession,
        question_text: str,
        session_id: str,
        selected_text: Optional[str] = None,
        book_metadata: Optional[dict] = None
    ) -> QuestionModel:
        """
        Log a user query to the database.
        
        Args:
            session: Database session
            question_text: The text of the user's question
            session_id: Session identifier
            selected_text: Optional selected text from the user
            book_metadata: Optional metadata about the book section
            
        Returns:
            The created QuestionModel
        """
        try:
            logger.info(f"Logging query for session {session_id}: {question_text[:50]}...")
            
            # Create a QuestionModel instance
            question = QuestionModel(
                content=question_text,
                session_id=session_id,
                selected_text=selected_text,
                book_metadata=book_metadata
            )
            
            # Add the question to the session
            session.add(question)
            await session.commit()
            await session.refresh(question)
            
            logger.info(f"Successfully logged question with ID {question.id}")
            return question
            
        except Exception as e:
            logger.error(f"Error logging query: {str(e)}")
            await session.rollback()
            raise DatabaseException(f"Failed to log query: {str(e)}")
    
    async def log_answer(
        self,
        session: AsyncSession,
        question_id: str,
        answer_text: str,
        model_used: str,
        tokens_used: Optional[int] = None,
        selected_text_mode: bool = False
    ) -> AnswerModel:
        """
        Log an answer to the database.
        
        Args:
            session: Database session
            question_id: ID of the associated question
            answer_text: The generated answer text
            model_used: Name of the model that generated the answer
            tokens_used: Number of tokens in the answer (optional)
            selected_text_mode: Whether this was generated in selected text mode
            
        Returns:
            The created AnswerModel
        """
        try:
            logger.info(f"Logging answer for question {question_id}")
            
            # Create an AnswerModel instance
            answer = AnswerModel(
                question_id=question_id,
                content=answer_text,
                model_used=model_used,
                tokens_used=tokens_used,
                selected_text_mode=selected_text_mode
            )
            
            # Add the answer to the session
            session.add(answer)
            await session.commit()
            await session.refresh(answer)
            
            logger.info(f"Successfully logged answer with ID {answer.id}")
            return answer
            
        except Exception as e:
            logger.error(f"Error logging answer: {str(e)}")
            await session.rollback()
            raise DatabaseException(f"Failed to log answer: {str(e)}")
    
    async def log_action(
        self,
        session: AsyncSession,
        question_id: str,
        action: str,
        details: Optional[dict] = None,
        success: bool = True
    ) -> LogEntryModel:
        """
        Log an action related to a question.
        
        Args:
            session: Database session
            question_id: ID of the associated question
            action: Description of the action taken
            details: Additional details about the action
            success: Whether the action was successful
            
        Returns:
            The created LogEntryModel
        """
        try:
            logger.info(f"Logging action '{action}' for question {question_id}")
            
            # Create a LogEntryModel instance
            log_entry = LogEntryModel(
                question_id=question_id,
                action=action,
                details=details,
                success=success,
                timestamp=datetime.utcnow()
            )
            
            # Add the log entry to the session
            session.add(log_entry)
            await session.commit()
            await session.refresh(log_entry)
            
            logger.info(f"Successfully logged action with ID {log_entry.id}")
            return log_entry
            
        except Exception as e:
            logger.error(f"Error logging action: {str(e)}")
            await session.rollback()
            raise DatabaseException(f"Failed to log action: {str(e)}")


# Global instance of the service
logging_service = LoggingService()