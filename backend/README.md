# Integrated RAG Chatbot for Academic Book

This project implements a production-ready, constitution-compliant Retrieval-Augmented Generation (RAG) chatbot embedded within a published academic book on AI-native software development. The chatbot answers questions strictly from book content or user-selected text while maintaining academic rigor and full citation traceability.

## Features

- Ask questions about book content and receive responses with APA citations
- Selected-text-only question answering mode
- Strict academic tone enforcement
- Zero hallucination policy compliance
- Full traceability of claims back to source material

## Tech Stack

- Backend: FastAPI
- Vector Database: Qdrant Cloud
- Relational Database: Neon Serverless Postgres
- LLM Provider: Qwen models via Cohere API
- Frontend: Embedded widget compatible with Docusaurus

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and update with your configuration
6. Run the application: `uvicorn src.api.main:app --reload`

## Usage

The API provides the following endpoints:

- `POST /api/v1/query` - Process a user question and return a RAG-enhanced response
- `GET /api/v1/health` - Health check endpoint

For detailed API usage, see the OpenAPI documentation at `/docs` when running in development mode.

## Development

To run tests: `pytest`

## Architecture

The system follows a service-oriented architecture with:
- Models representing the data entities
- Services implementing business logic
- API layer handling request/response
- Database layer managing persistence
- Core utilities for configuration and exceptions