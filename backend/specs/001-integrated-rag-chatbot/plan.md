# Implementation Plan: Integrated RAG Chatbot for AI-Native Software Development Book

**Branch**: `001-integrated-rag-chatbot` | **Date**: 2025-12-16 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-integrated-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a production-ready, constitution-compliant Retrieval-Augmented Generation (RAG) chatbot embedded within a published academic book on AI-native software development. The chatbot must answer questions strictly from book content or user-selected text while maintaining academic rigor and full citation traceability. The implementation will use FastAPI for the backend, Qdrant Cloud for vector storage, Neon Serverless Postgres for metadata, and Qwen models via Cohere API for generation, with an embedded chat widget compatible with Docusaurus.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, Qdrant, Neon Postgres, Cohere API, SpecifyKit-Plus
**Storage**: Qdrant Cloud (vector DB), Neon Serverless Postgres (metadata), Book content
**Testing**: pytest
**Target Platform**: Linux server (cloud deployment)
**Project Type**: Web application (backend + frontend integration)
**Performance Goals**: End-to-end response < 5 seconds, retrieval latency < 1 second
**Constraints**: No OpenAI usage, <200ms p95 DB queries, <10 concurrent API calls per IP (rate limiting)
**Scale/Scope**: Support up to 100 concurrent users, handle 1000 daily active users, 99.5% uptime

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**STATUS: PASSED** - All constitution principles are addressed in the planned architecture:

1. **Grounded Accuracy**: The system will strictly answer using retrieved context from the vector database or user-selected text. If relevant information is not found, the system will explicitly state: "The provided sources do not contain sufficient information to answer this question."

2. **Zero Hallucination Policy**: The system will not infer, guess, extrapolate, or fabricate information. No external knowledge beyond retrieved context will be allowed. Implementation will include validation services to enforce this.

3. **Academic Rigor**: Responses will maintain an academic tone suitable for a computer science audience. All claims will be supported by citations. The prompt engineering and response formatting will enforce this requirement.

4. **Citation & Traceability**: All factual claims will include APA-style citations that directly correspond to retrieved source chunks. No uncited factual statements will be allowed. A dedicated citation service will generate proper APA citations.

5. **Selected-Text Isolation Mode**: When the user provides selected text, the system will ignore the rest of the book, answer strictly based on the selected text, and explicitly state limitations if the selection is insufficient. This will be implemented as a distinct mode in the RAG service.

6. **Reproducibility & Transparency**: Answers will be deterministic given the same inputs. The system will explain reasoning steps only in terms of source alignment. Session tracking and logging will ensure reproducibility.

7. **Writing Quality Standards**: Responses will maintain Flesch-Kincaid Grade 10-12 clarity level with concise, structured, and formal academic language. Response formatting will enforce these standards.

8. **Plagiarism Prevention**: Responses will be original reformulations. Direct quotations will be clearly marked and cited. Plagiarism tolerance is 0%. The generation service will include checks to ensure originality.

## Project Structure

### Documentation (this feature)

```text
specs/001-integrated-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── question.py
│   │   ├── response.py
│   │   ├── citation.py
│   │   └── book_content.py
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── retrieval_service.py
│   │   ├── generation_service.py
│   │   ├── citation_service.py
│   │   └── validation_service.py
│   ├── api/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── query.py
│   │   │   └── health.py
│   │   └── middleware/
│   │       └── rate_limiter.py
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   └── core/
│       ├── config.py
│       ├── constants.py
│       └── exceptions.py
└── tests/
    ├── unit/
    │   ├── test_rag_service.py
    │   ├── test_retrieval_service.py
    │   └── test_generation_service.py
    ├── integration/
    │   ├── test_query_endpoint.py
    │   └── test_selected_text_mode.py
    └── conftest.py
```

**Structure Decision**: We're implementing a web application with a backend API and frontend integration. The backend will be built with FastAPI and deployed as a service that the frontend can interact with. The structure reflects the need for RAG-specific services, API endpoints, database models, and comprehensive testing.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |