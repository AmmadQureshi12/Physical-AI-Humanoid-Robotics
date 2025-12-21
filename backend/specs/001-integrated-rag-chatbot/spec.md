# Feature Specification: Integrated RAG Chatbot for Academic Book

**Feature Branch**: `001-integrated-rag-chatbot`
**Created**: 2025-12-16
**Status**: Draft
**Input**: User description: "Integrated RAG Chatbot for Academic Book: AI-Native Software Development Project Type: AI-native academic RAG system embedded inside a published research book / website. Primary Objective: Design and implement a production-grade Retrieval-Augmented Generation (RAG) chatbot that can answer user questions strictly based on the book's content, including an isolated mode where answers are generated only from user-selected text. Target Audience: - Computer Science researchers - Graduate-level students - AI / Software Engineering professionals - Academic reviewers Core Capabilities: 1. Embedded Chatbot - Chat UI integrated directly within the published book website. - Supports free-form questions about the book's content. - Supports 'selected text only' question-answering mode. 2. Strict RAG Enforcement - No response without retrieved context. - No external knowledge usage. - Explicit refusal when sources are insufficient. 3. Academic Output Quality - Formal academic tone. - APA-style inline citations. - Claims fully traceable to source chunks. Technology Stack (Fixed & Required): - Backend: FastAPI - RAG Orchestration: SpecifyKit-Plus - LLM Provider: Qwen models via Cohere API (OpenAI strictly prohibited) - Vector Database: Qdrant Cloud (Free Tier) - Relational Database: Neon Serverless Postgres - Frontend: Embedded widget compatible with Docusaurus Infrastructure Credentials (Runtime Configuration): - Neon Postgres Database: postgresql://neondb_owner:npg_am6kr9fbODhv@ep-floral-lake-ahzd486u-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require - Qdrant Cloud: Cluster ID: 6c0a5f3f-0328-496b-adf5-d0bc5613920b URL: https://6c0a5f3f-0328-496b-adf5-d0bc5613920b.us-east4-0.gcp.cloud.qdrant.io:6333 API Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.TqzYwK3-fEBd3smRL3WItTijQZB3f_QW21lG1yXkIEo - Cohere API (Qwen models): API Key: M8Lh6vHl4fzxOmrQD3F5t4ThbZhLgsQllAZwsUGo Data Sources: - Book chapters and sections - Peer-reviewed academic references cited within the book - User-selected text segments (highest priority) Success Criteria: - Answers are generated only from retrieved or selected content. - Every factual claim is cited (APA format). - Zero hallucinations. - Deterministic and reproducible outputs. - Academic reviewers can trace every answer back to the book text. Constraints: - No OpenAI SDKs, APIs, or embeddings. - No web browsing or external search. - No uncited claims. - No informal or conversational tone. Not Building: - General-purpose chatbot - Creative writing assistant - External knowledge QA system - Web search or live citation fetcher - Ethical or philosophical discussion outside book scope Deliverables: 1. RAG-enabled FastAPI backend 2. Qdrant indexing and retrieval pipeline 3. Cohere + Qwen response generation 4. Embedded book chatbot UI 5. Selected-text-only RAG answering mode 6. Full SpecifyKit-compatible plan and tasks"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions About Book Content (Priority: P1)

A Computer Science researcher wants to ask questions about specific topics in the AI-native software development book. They visit the book's website, use the embedded chatbot to pose a question, and receive a response with citations to relevant sections of the book.

**Why this priority**: This is the core functionality of the RAG system - enabling researchers to get value from the book content through natural language questions.

**Independent Test**: Can be fully tested by asking questions about different topics in the book and verifying that responses are grounded in the book content with proper citations.

**Acceptance Scenarios**:

1. **Given** user is on the book website, **When** they ask a question about content in the book, **Then** the system provides an answer with APA-style citations to relevant sections of the book
2. **Given** a graduate student asks a question about a concept in the book, **When** the question is processed, **Then** the response maintains formal academic tone appropriate for computer science audience
3. **Given** a question is asked that cannot be answered using the book content, **When** processing is complete, **Then** the system explicitly states that the book does not contain sufficient information to answer

---

### User Story 2 - Query Selected Text Only (Priority: P2)

A graduate student is reading the book and selects a specific text passage. They want to ask questions about only that selected text rather than the entire book. They use the selected-text mode of the chatbot to get answers strictly based on the selected content.

**Why this priority**: Provides specialized functionality for users who want to focus on specific portions of the book for analysis or study.

**Independent Test**: Can be fully tested by selecting text and asking questions that should only be answered based on the selected text, not the wider book context.

**Acceptance Scenarios**:

1. **Given** user has selected a text segment on the book page, **When** they activate the selected-text-only mode and ask a question, **Then** the system answers only based on the selected text with APA citations
2. **Given** user has selected text that is insufficient to answer a question, **When** they submit the query, **Then** the system explicitly states that the selected text is insufficient, ignoring the wider book content

---

### User Story 3 - Verify Academic Claims (Priority: P3)

An academic reviewer is examining responses from the chatbot and needs to verify that claims made in answers can be traced back to the source book. They check citations and verify that all claims are supported by the book content.

**Why this priority**: Ensures academic rigor and reproducibility, which are key requirements for the target academic audience.

**Independent Test**: Can be fully tested by reviewing chatbot responses for proper citation attribution and verifying that all factual claims can be traced back to the book content.

**Acceptance Scenarios**:

1. **Given** a chatbot response with multiple claims, **When** citations are examined, **Then** each claim is traceable to a specific section in the book with proper APA citation format
2. **Given** a complex question requiring multiple book sections, **When** response is generated, **Then** all sources used are cited and traceable to the original text

---

### Edge Cases

- What happens when users ask questions outside the book's scope?
- How does the system handle ambiguous questions that could refer to multiple topics?
- What happens when selected text is just a single word or phrase that cannot provide sufficient context?
- How does the system respond when the vector database is temporarily unavailable?
- What happens with very long questions that might exceed token limitations?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST answer questions strictly using retrieved context from the book's vector database or user-selected text
- **FR-002**: System MUST explicitly state when book sources do not contain sufficient information to answer a question
- **FR-003**: System MUST NOT infer, guess, extrapolate, or fabricate information beyond what's in the book
- **FR-004**: System MUST maintain formal academic tone appropriate for computer science researchers and graduate students
- **FR-005**: System MUST provide APA-style citations for all factual claims in responses
- **FR-006**: System MUST support a selected-text-only mode that answers questions only based on user-selected text segments
- **FR-007**: System MUST ensure all responses are deterministic when given identical inputs
- **FR-008**: System MUST reject questions that violate academic integrity or fall outside the book's scope
- **FR-009**: System MUST maintain Flesch-Kincaid Grade 10-12 readability level for all responses

*Example of marking unclear requirements:*

- **FR-010**: System MUST handle rate limiting for API calls to Cohere/Qwen services with maximum 60 requests per minute per IP
- **FR-011**: System MUST provide responses in 10 seconds or less for most queries

### Key Entities

- **Question**: A query posed by the user about the book content, which may be context-free or specifically about selected text
- **Retrieved Context**: Book passages retrieved from the vector database that are relevant to answering the user's question
- **Response**: The chatbot's answer to the user's question, including citations to source material
- **Citation**: Reference in APA format to the specific sections of the book that support claims made in the response
- **Book Content**: The published academic book's text, including chapters, sections, and peer-reviewed references

## Clarifications

### Session 2025-12-16

- Q: What level of security and privacy controls are required for user questions and data? → A: Standard web security with data anonymization and no user-identifying information retention
- Q: What are the expected concurrent user limits and traffic volumes for the chatbot? → A: Moderate scale: support up to 100 concurrent users with ability to handle 1000 daily active users
- Q: What level of system uptime and response availability is required for the chatbot? → A: High availability: 99.5% uptime with graceful degradation during partial outages
- Q: Are there any specific regulatory or compliance requirements (e.g., GDPR, FERPA, etc.) that apply to this academic system? → A: Standard compliance with regional data protection laws (e.g., GDPR, CCPA) but no specialized regulations
- Q: What are the requirements for system recovery and data backup in case of failures? → A: Automated daily backups with ability to restore within 4 hours of failure

## Dependencies and Assumptions

- **Infrastructure**: Access to Cohere API for Qwen model access, Qdrant Cloud vector database, Neon Serverless Postgres
- **Book Content**: Book chapters, sections and references are properly indexed in the vector database
- **User Access**: Users have access to the book website where the chatbot is embedded
- **Network**: Reliable internet connection for API calls to external services
- **Data Accuracy**: Source book content is accurate and properly formatted for retrieval

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of responses are generated only from retrieved or selected book content with no hallucinations
- **SC-002**: 100% of factual claims in responses include proper APA citations that correspond to actual book content
- **SC-003**: Academic reviewers can trace every answer back to the original book text with 100% success rate
- **SC-004**: The system maintains deterministic outputs given identical inputs
- **SC-005**: 95% of properly scoped questions receive useful answers with proper citations
- **SC-006**: All responses maintain Flesch-Kincaid Grade 10-12 readability level
- **SC-007**: Selected-text-only mode correctly ignores content outside of the user-selected text with 100% accuracy