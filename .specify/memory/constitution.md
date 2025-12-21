# AI Book Docusaurus 2025 — Constitution

> This document defines the governance, structure, and features of the AI book project.

---

## Project Overview

The purpose of this book project is to provide a structured, interactive learning experience on AI systems in the physical world.  
The book emphasizes **embodied intelligence** and aims to bridge **digital brain and physical body concepts** for students and readers.

---

## Governance

1. **Authority Document**: `constitution.md` is the primary governance document.
2. **Chapter Management**: Chapters are stored in `/docs/chapter-01.md` … `/docs/chapter-12.md`.
3. **Updates**:
   - Any change to core content must follow the approval process.
   - AI-generated drafts or content must be reviewed and validated before publishing.
4. **Versioning**: All updates tracked in Git; GitHub repository is authoritative.

---

## Structure

- `docs/` — Markdown files for chapters and constitution.
- `src/pages/` — React/Docusaurus pages for frontend.
- `static/images/` — Diagrams and illustrations.
- `docusaurus.config.js` — Site configuration.
- `sidebars.js` — Automatic sidebar generation.

---

## Addons / Features

- **Book-Aware AI Chatbot** (2025-12-15)
  - Answers user questions strictly from book content.
  - Uses a vector database and OpenAI Agents SDK for retrieval-augmented generation (RAG).
  - Backend deployed on Render; frontend integrated as floating chat widget.
  - Refuses questions not present in the book.
  - Supports incremental updates as new chapters are added.

---

## Technology Stack (Addons)

- **Backend**: Python 3.11, FastAPI, uv, OpenAI Agents SDK, Chroma vector database  
- **Frontend**: Docusaurus v3, React, Chatbot widget  
- **Deployment**: GitHub Pages (frontend), Render (backend)

---

## Chapter Guidelines

1. Chapters should be clear, concise, and follow the agreed numbering scheme.
2. AI-generated content may be used as drafts, but all edits must be verified.
3. Diagrams should be included in `/static/images/` and referenced with alt text.

---

## Using the AI Chatbot

- Click the floating chatbot button on any page.
- Ask a question about book content.
- The chatbot responds using information strictly from the book.
- Out-of-book questions will be politely refused.
- Backend automatically uses the vector database for retrieval; no manual ingestion is required after deployment.

---

## Contribution Guidelines

- Contributions follow the standard Git workflow.
- Use Spec-Kit Plus, Gemini CLI, or Qwen Code for content generation or updates.
- Tests and verification are mandatory for AI and backend features.
- All pull requests must pass CI checks before merge.

---

## Versioning & Updates

- Version: 1.0.0  
- Date Ratified: 2025-12-15  
- Updates tracked via Git commits with clear messages.
- Major feature additions are recorded in the Addons / Features section.

---

## Acceptance Criteria

- Constitution defines governance, structure, features, and usage guidelines clearly.
- AI Chatbot integration is documented but does not modify core chapters.
- All contributors understand deployment workflow for frontend and backend.
- Changes are auditable and maintain history in Git.

---

*End of Constitution — AI Book Docusaurus 2025*
