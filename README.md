# AI-Humanoid Robotics Educational Chatbot

This project implements an educational chatbot for the AI-Humanoid Robotics curriculum. The system consists of a backend API that provides RAG (Retrieval-Augmented Generation) functionality and a frontend React application that provides an intuitive chat interface for students.

## Architecture

- **Backend**: FastAPI-based API server with RAG capabilities using Qdrant vector database
- **Frontend**: React-based chat interface with TypeScript and Tailwind CSS
- **AI Integration**: Uses Cohere's Qwen models for natural language processing

## Features

- Educational Q&A about AI-Humanoid Robotics concepts
- Different response types: hints, explanations, resource links
- Session management for continued conversations
- Integration with curriculum materials
- Exercise assistance without direct solutions

## Prerequisites

- Python 3.9+
- Node.js 18+ and npm
- Access to Cohere API (for Qwen models)
- Access to Qdrant Cloud (or local Qdrant instance)

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables by creating a `.env` file in the backend directory:
```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=your_qdrant_url
SECRET_KEY=your_secret_key
```

4. Start the backend server:
```bash
python -m uvicorn src.api.main:app --reload
```

The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the frontend directory:
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
```

4. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`.

## Running Both Servers

You can use the provided scripts to start both servers:

1. Start backend server:
```bash
python start_backend.py
```

2. In a separate terminal, start frontend server:
```bash
python start_frontend.py
```

## API Endpoints

- `GET /api/v1/chat/capabilities` - Get the capabilities of the chatbot
- `POST /api/v1/chat` - Send a message to the chatbot
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Project Structure

```
AI-humanoid-robotices/
├── backend/                 # FastAPI backend server
│   ├── src/
│   │   ├── api/            # API routes and middleware
│   │   ├── services/       # Business logic
│   │   ├── core/           # Core utilities and configuration
│   │   └── database/       # Database models and initialization
│   ├── tests/              # Backend tests
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── api/            # API client
│   │   ├── contexts/       # React contexts
│   │   └── utils/          # Utility functions
│   ├── public/
│   └── package.json
├── start_backend.py        # Script to start backend server
├── start_frontend.py       # Script to start frontend server
└── README.md
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Development

Both the frontend and backend support hot reloading during development.

## Deployment

For production deployment:
1. Set appropriate environment variables
2. Build the frontend with `npm run build`
3. Serve the build files through a web server
4. Deploy the backend to your preferred cloud provider

## Technologies Used

- **Backend**: Python, FastAPI, Qdrant, PostgreSQL, Cohere API
- **Frontend**: React, TypeScript, Tailwind CSS, Axios
- **AI**: Cohere's Qwen models for natural language processing