"""
Database models for the RAG Chatbot entities.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, UUID, ForeignKey, JSON, Table
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
import uuid


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


# Link table for many-to-many relationship between Answer and RetrievedContext
answer_retrieved_context = Table(
    "answer_retrieved_context",
    Base.metadata,
    Column("answer_id", PG_UUID(as_uuid=True), ForeignKey("answers.id")),
    Column("retrieved_context_id", PG_UUID(as_uuid=True), ForeignKey("retrieved_contexts.id"))
)


class Question(Base):
    """Represents a query posed by the user about the book content"""
    __tablename__ = "questions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True
    )
    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False
    )
    selected_text: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    book_metadata: Mapped[dict] = mapped_column(JSON, nullable=True)

    # Relationships
    answer: Mapped["Answer"] = relationship("Answer", back_populates="question", uselist=False)
    log_entries: Mapped[list["LogEntry"]] = relationship("LogEntry", back_populates="question")
    retrieved_contexts: Mapped[list["RetrievedContext"]] = relationship("RetrievedContext", back_populates="question")


class RetrievedContext(Base):
    """Represents book passages retrieved from the vector database that are relevant to answering a user's question"""
    __tablename__ = "retrieved_contexts"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    question_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("questions.id"),
        nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_chapter: Mapped[str] = mapped_column(String, nullable=False)
    source_section: Mapped[str] = mapped_column(String, nullable=False)
    source_page: Mapped[int] = mapped_column(Integer, nullable=True)
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False)
    chunk_id: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    question: Mapped["Question"] = relationship("Question", back_populates="retrieved_contexts")
    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        secondary=answer_retrieved_context,
        back_populates="retrieved_contexts"
    )


class Answer(Base):
    """The chatbot's response to a user's question, including citations to source material"""
    __tablename__ = "answers"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    question_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("questions.id"),
        nullable=False,
        unique=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    model_used: Mapped[str] = mapped_column(String, nullable=False)
    tokens_used: Mapped[int] = mapped_column(Integer, nullable=True)
    selected_text_mode: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    question: Mapped["Question"] = relationship("Question", back_populates="answer")
    citations: Mapped[list["Citation"]] = relationship("Citation", back_populates="answer")
    retrieved_contexts: Mapped[list["RetrievedContext"]] = relationship(
        "RetrievedContext",
        secondary=answer_retrieved_context,
        back_populates="answers"
    )


class Citation(Base):
    """Reference in APA format to specific sections of the book that support claims made in the response"""
    __tablename__ = "citations"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    answer_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("answers.id"),
        nullable=False
    )
    apa_text: Mapped[str] = mapped_column(Text, nullable=False)
    source_chapter: Mapped[str] = mapped_column(String, nullable=False)
    source_section: Mapped[str] = mapped_column(String, nullable=False)
    source_page: Mapped[int] = mapped_column(Integer, nullable=True)
    quoted_text: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationship
    answer: Mapped["Answer"] = relationship("Answer", back_populates="citations")


class BookContent(Base):
    """The published academic book's text, including chapters, sections, and peer-reviewed references"""
    __tablename__ = "book_contents"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    chapter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    chapter_title: Mapped[str] = mapped_column(String, nullable=False)
    section_number: Mapped[str] = mapped_column(String, nullable=False)
    section_title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    page_start: Mapped[int] = mapped_column(Integer, nullable=False)
    page_end: Mapped[int] = mapped_column(Integer, nullable=False)
    vector_id: Mapped[str] = mapped_column(String, nullable=False)  # ID in vector database
    hash: Mapped[str] = mapped_column(String, nullable=False)  # For change detection


class LogEntry(Base):
    """Log entry for each interaction to enable reproducibility and traceability"""
    __tablename__ = "log_entries"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    question_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("questions.id"),
        nullable=False
    )
    action: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "query_processed", "response_generated"
    details: Mapped[dict] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    success: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationship
    question: Mapped["Question"] = relationship("Question", back_populates="log_entries")