# Data Model: Integrated RAG Chatbot for Academic Book

## Entity: Question
**Description**: Represents a query posed by the user about the book content

**Fields**:
- `id` (UUID): Unique identifier for the question
- `content` (Text): The text of the question posed by the user
- `user_id` (UUID, nullable): Identifier for the user who asked the question (for anonymous sessions, this may be null)
- `session_id` (UUID): Identifier for the conversation session
- `selected_text` (Text, nullable): Optional text selected by the user for "selected-text-only" mode
- `created_at` (DateTime): Timestamp when the question was asked
- `book_metadata` (JSON): Metadata about the book section/chapter where the question originated

**Relationships**:
- One-to-Many with Answer (one question generates one answer)
- One-to-Many with LogEntry (for logging purposes)

## Entity: RetrievedContext
**Description**: Represents book passages retrieved from the vector database that are relevant to answering a user's question

**Fields**:
- `id` (UUID): Unique identifier for the retrieved context
- `question_id` (UUID): Reference to the question this context is for
- `content` (Text): The text of the retrieved passage
- `source_chapter` (String): The chapter from which the content was retrieved
- `source_section` (String): The specific section within the chapter
- `source_page` (Integer, nullable): Page number if available
- `similarity_score` (Float): The similarity score from vector search
- `chunk_id` (String): The unique ID of this chunk in the vector database

**Relationships**:
- Many-to-One with Question (many retrieved contexts can be associated with one question)
- Many-to-Many with Answer (an answer can reference multiple retrieved contexts)

## Entity: Answer
**Description**: The chatbot's response to a user's question, including citations to source material

**Fields**:
- `id` (UUID): Unique identifier for the answer
- `question_id` (UUID): Reference to the question this is answering
- `content` (Text): The text of the generated answer
- `generated_at` (DateTime): Timestamp when the answer was generated
- `model_used` (String): Which model generated the answer (for tracking and reproducibility)
- `tokens_used` (Integer): Number of tokens in the response
- `selected_text_mode` (Boolean): Whether this answer was generated in selected-text-only mode

**Relationships**:
- One-to-One with Question (one answer per question)
- Many-to-Many with RetrievedContext (an answer can reference multiple retrieved contexts)
- One-to-Many with Citation (one answer can have multiple citations)

## Entity: Citation
**Description**: Reference in APA format to specific sections of the book that support claims made in the response

**Fields**:
- `id` (UUID): Unique identifier for the citation
- `answer_id` (UUID): Reference to the answer containing this citation
- `apa_text` (Text): The properly formatted APA citation
- `source_chapter` (String): Chapter referenced in the citation
- `source_section` (String): Section within the chapter
- `source_page` (Integer, nullable): Page number if available
- `quoted_text` (Text, nullable): If this citation refers to a direct quote, the actual text

**Relationships**:
- Many-to-One with Answer (multiple citations per answer)
- One-to-Many with ValidationLog (for tracking citation validity)

## Entity: BookContent
**Description**: The published academic book's text, including chapters, sections, and peer-reviewed references

**Fields**:
- `id` (UUID): Unique identifier for the book content piece
- `chapter_number` (Integer): The chapter number
- `chapter_title` (String): Title of the chapter
- `section_number` (String): Section identifier (e.g., "2.3")
- `section_title` (String): Title of the section
- `content` (Text): The actual content of this piece
- `page_start` (Integer): Starting page number
- `page_end` (Integer): Ending page number
- `vector_id` (String): The ID of this content in the vector database
- `hash` (String): Hash of the content for change detection

**Relationships**:
- One-to-Many with RetrievedContext (retrieved contexts come from book content)

## Entity: LogEntry
**Description**: Log entry for each interaction to enable reproducibility and traceability

**Fields**:
- `id` (UUID): Unique identifier for the log entry
- `question_id` (UUID): Reference to the question being logged
- `action` (String): The action being logged (e.g., "query_processed", "response_generated", "citation_added")
- `details` (JSON): Additional details about the action
- `timestamp` (DateTime): When the action occurred
- `success` (Boolean): Whether the action was successful

**Relationships**:
- Many-to-One with Question (multiple log entries per question)

## Validation Rules

1. **Question Validation**:
   - Content must not be empty
   - Selected text mode requires `selected_text` field to be populated
   - Session ID is required for all questions

2. **RetrievedContext Validation**:
   - Must have a similarity score between 0 and 1
   - Content must not be empty
   - Must be associated with a valid question

3. **Answer Validation**:
   - Content must not be empty
   - Must be associated with a valid question
   - If in selected text mode, should not reference book content outside the selected text

4. **Citation Validation**:
   - APA text must follow proper format
   - Must be associated with a valid answer
   - Source fields must reference actual book content

5. **BookContent Validation**:
   - Chapter number must be positive
   - Page numbers must be positive and end must be greater than start
   - Content must not be empty

## State Transitions

The entities in this system do not have complex state transitions like traditional workflow systems. However, the following logical transitions apply:

1. **Question Processing**:
   - NEW (received) → WITH_CONTEXT (retrieval complete) → ANSWERED (response generated) → LOGGED (interaction logged)

2. **Answer Validation**:
   - GENERATED → UNDER_REVIEW (if auto-validation fails) → APPROVED (ready for response) → DELIVERED (sent to user)