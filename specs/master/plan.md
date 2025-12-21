File: /specs/001-ai-embodied-intelligence/plan.md
Branch: 001-ai-embodied-intelligence
Date: 2025-12-06
Spec: /specs/001-ai-embodied-intelligence/spec.md
Input: Specification for the AI Systems in the Physical World – Embodied Intelligence book project

# Implementation Plan: AI Systems in the Physical World — Embodied Intelligence

This implementation plan defines the execution workflow, phases, deliverables, verification gates, and repository structure for the creation of a fully AI-assisted technical book and documentation portal using:

Docusaurus 3+

Spec-Kit Plus 2.1.0

Gemini CLI

Claude Code / Qwen Code CLI

GitHub Pages

Context7 Server (optional integration)

This plan is generated according to Spec-Kit Plus planning template and is fully compliant with the Book Constitution v2.1.0.

## 1. Summary

The goal of this project is to produce a 5-chapter book on Physical AI & Humanoid Robotics deployed as a Docusaurus website, using a spec-driven workflow and AI-native authoring tools.

The book will teach fundamental principles of:

Humanoid robotics

Sensors & perception

Motion systems

Control & locomotion

AI agents + cloud-robot intelligence

The project implements:

A complete Docusaurus site

Fully structured book chapters (spec.md + index.md)

Diagrams + images

Code samples

Verification checklists

GitHub Pages deployment pipeline

AI-assisted workflows using Gemini CLI, Claude Code, and Qwen CLI

Spec-Kit Plus driven development and validation

This Plan defines how the specification will be executed across phases (0–2), including research, structure design, draft creation, testing, and deployment.

## 2. Technical Context
Languages / Tools

Markdown (Docusaurus content)

JavaScript / TypeScript (Docusaurus config)

Gemini CLI, Claude Code, Qwen Code CLI (AI content generators)

Spec-Kit Plus 2.1.0

Node.js 18+

GitHub Pages deployment

Dependencies

Docusaurus v3

@docusaurus/theme-classic

Spec-Kit Plus

GitHub Actions (deploy)

Gemini CLI

Claude Code

Qwen Code

Context7 MCP Server (optional)

Storage

Markdown files

/img directory for diagrams

/specs for specification files

Static assets in Docusaurus

Testing

Build testing (npm run build)

Link validation

Sidebar structure validation

Local preview testing (npm run start)

Target Platform

GitHub Pages hosted static site

Local development via Node.js

Performance Goals

Build time < 20s

Navigation instant (<50ms)

Image loading optimized via Webpack

Constraints

GitHub Pages must be enabled

Site must use baseUrl + path config

Gemini/Claude/Qwen CLI used for content, not deployment

Scope

5-chapter book (expandable)

AI-native documentation workflow demonstration

Full Docusaurus site with sidebar + home page

Automated deployment

## 3. Constitution Compliance Check
Spec-Driven Development (PASS)

All chapters produced strictly follow Spec-Kit Plus structure (purpose, tools, tasks, verification).

Technical Accuracy (PASS)

Chapters written using real robotics + AI engineering concepts.

Clarity (PASS)

Beginner-friendly, step-by-step educational tone.

Reproducibility (PASS)

Commands, folder paths, deployment steps included.

Tool Alignment (PASS)

Gemini CLI, Claude Code, Qwen CLI, and Docusaurus 3 supported.

## 4. Standards Compilation
Writing & Structure Standards

Each chapter = purpose, tools, steps, diagrams, verification

Professional formatting

No missing sections

Code & Config Standards

All examples testable

Node configs verified

GitHub Pages workflows correct

Documentation Standards

Minimum 10 diagrams

10k–15k words (5 chapters cover ~40–50% of total target)

Citation Standards

Must reference official documentation

## 5. Implementation Phases

The project follows Spec-Kit Plus execution pipeline:

### PHASE 0 — Research & Foundations

Deliverables:

/research.md

Topic research

Robotics fundamentals

AI agents + VLM research

Tool analysis (Gemini CLI, Claude Code, Qwen CLI, Docusaurus)

Tasks:

Gather references

Structure chapter outlines

Validate accuracy using spec.md

Gate:
Cannot move to Phase 1 until Constitution Check passes.

### PHASE 1 — System Design & Book Architecture

Deliverables:

/data-model.md

/quickstart.md

/contracts/*.md

Tasks:

Create full book architecture

Define chapters

Generate initial drafts

Create Docusaurus site skeleton

Sidebar structure

Home page design

Gate:
All files must match Constitution format.

### PHASE 2 — Content Creation & Technical Construction

Deliverables:

/tasks.md

Chapter drafts (full 5 chapters generated already)

Diagrams + illustrations

Code samples

Deployment pipeline

Tasks:

Convert AI-generated drafts into clean Markdown

Add code blocks

Add images + diagrams

Build Docusaurus site

Fix sidebar structure

Optimize for GitHub Pages

Gate:
Docusaurus must build successfully.

## 6. Project Structure (Updated)
specs/001-ai-embodied-intelligence/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── content.md
│   ├── tooling.md
│   ├── ai-policy.md
└── tasks.md

## 7. Book Structure (Matches Your 5 Chapters)
docs/
├── chapter-01-specification-basics.md
├── chapter-02-sensors-and-perception.md
├── chapter-03-actuators-and-motion.md
├── chapter-04-control-and-locomotion.md
├── chapter-05-ai-agents-and-cloud-intelligence.md
├── img/
│   ├── sensors/
│   ├── motion/
│   ├── control/
│   └── ai-agents/

## 8. Complexity Tracking

No violations.
Project fits Constitution requirements.