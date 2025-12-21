# Research: Integrated RAG Chatbot for Academic Book

## Decision: Technology Stack Selection
**Rationale**: The technology stack was predetermined in the specification and constitution: FastAPI for the backend due to its performance and async capabilities, Qdrant for vector storage due to its efficiency with embeddings, Neon Serverless Postgres for metadata storage, and Qwen models via Cohere API to comply with the constraint prohibiting OpenAI usage.

**Alternatives considered**: 
- Backend: Flask (rejected for performance reasons), Django (rejected for being too heavy for this use case)
- Vector DB: Pinecone (rejected due to cost considerations), Weaviate (not specified in requirements)
- LLM Provider: OpenAI (explicitly prohibited by constitution), Anthropic (not specified in requirements)

## Decision: Embedding Strategy
**Rationale**: Using a non-OpenAI embedding solution to comply with the constitution. Options include sentence-transformers, Cohere embeddings, or other open-source solutions like BGE (BAAI General Embeddings). Given that we're already using Cohere for the LLM, Cohere embeddings would provide consistency.

**Alternatives considered**:
- Sentence-transformers (like all-MiniLM-L6-v2): Free but may not be as performant as commercial options
- BGE: Good open-source option but requires local deployment and maintenance
- Cohere embeddings: Consistent with our LLM choice and commercially supported

## Decision: Chunking Strategy for Academic Text
**Rationale**: Academic texts require special consideration for chunking to preserve context and meaning. We'll use a hybrid approach that respects document hierarchy (chapters, sections, subsections) while ensuring semantic coherence. Each chunk will have metadata linking back to its source (chapter, section, page, etc.).

**Alternatives considered**:
- Fixed-size token chunks: Simpler but may break important semantic boundaries
- Hierarchical chunking by document structure: Respects academic organization but might create very large or small chunks
- Semantic chunking: Maintains meaning but requires complex implementation

## Decision: Citation Format and Generation
**Rationale**: To comply with the constitution's requirement for APA-style citations, we'll implement a citation service that can generate proper APA citations based on the book's metadata. Each retrieved chunk will be tagged with proper source information that can be transformed into a citation.

**Alternatives considered**:
- Storing pre-formatted citations: More storage but simpler retrieval
- Generating citations on-the-fly: Less storage but requires citation logic implementation
- Simple reference format: Less rigorous but potentially easier to implement

## Decision: Rate Limiting Implementation
**Rationale**: To handle the requirement of "60 requests per minute per IP" from the clarifications, we'll implement a rate limiter using a Redis backend or similar in-memory store for efficient tracking.

**Alternatives considered**:
- In-application memory: Simpler but doesn't work in multi-instance deployments
- Database storage: More persistent but adds latency to each request
- Redis/memcached: Optimal performance and works across multiple instances

## Decision: Selected-Text Isolation Mode Implementation
**Rationale**: For the selected-text-only mode, we'll implement a specific flow that bypasses the RAG retrieval and only uses the user-provided text as context for the LLM. This requires special validation to ensure no information from the book is used when this mode is active.

**Alternatives considered**:
- Separate service: More isolation but adds complexity
- Same service with mode flag: Simpler but requires careful implementation to avoid contamination
- Client-side only: Doesn't provide the backend validation required for academic rigor

## Decision: Failure Handling and Graceful Degradation
**Rationale**: To meet the 99.5% uptime requirement, we need to implement error handling for different failure modes:
- Qdrant unavailable: Return appropriate error message
- Cohere API unavailable: Cache responses or provide graceful error
- Postgres unavailable: Still allow queries but not log, or queue for later

**Alternatives considered**:
- Stop all service during any dependency failure: More reliable but reduces uptime
- Allow degraded responses: Maintains availability but might not meet quality requirements
- Implement circuit breakers: Balances availability and quality