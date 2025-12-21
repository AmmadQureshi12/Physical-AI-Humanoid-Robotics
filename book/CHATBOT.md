# AI-Humanoid Robotics Book - Chatbot Integration

This directory contains the implementation for the AI-powered chatbot integrated into the AI-Humanoid Robotics book. The chatbot connects to the backend API to provide intelligent responses about the book content.

## Components

### Chatbot Component (`src/components/Chatbot`)
- A React component that provides a chat interface
- Connects to the backend API at `http://localhost:8000/api/v1/chat`
- Supports different message types (hints, explanations, resource links)
- Maintains conversation context and session state

### Floating Chatbot Button
- A floating button that appears on documentation pages
- Allows users to open the chatbot without navigating away from the content
- Preserves the current page context when querying the chatbot

## Backend Connection

The chatbot connects to the backend API running on port 8000. The backend must be started separately using:

```bash
cd backend
python start_backend.py
```

## Usage

1. Ensure the backend API is running
2. Start the book documentation:
   ```bash
   cd book
   npm start
   ```
3. Navigate to the chatbot page at `/chatbot` or use the floating button on documentation pages

## Configuration

The chatbot can receive contextual information about the current page through the `context` prop, allowing it to provide more relevant responses based on the chapter or topic being viewed.