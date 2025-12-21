# Quickstart Guide: Integrated RAG Chatbot for Academic Book

## Prerequisites

- Python 3.11+
- pip package manager
- Git
- Access to Cohere API (with Qwen models)
- Access to Qdrant Cloud
- Neon Serverless Postgres account
- (Optional) Docker and Docker Compose for containerized development

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/ai-book-rag-chatbot.git
cd ai-book-rag-chatbot
```

### 2. Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
NEON_DB_URL=postgresql://neondb_owner:your_password@ep-floral-lake-ahzd486u-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# Vector Database Configuration
QDRANT_URL=https://6c0a5f3f-0328-496b-adf5-d0bc5613920b.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=book_content_chunks

# LLM Provider Configuration
COHERE_API_KEY=your_cohere_api_key
MODEL_NAME=qwen-7b # or whichever Qwen model you're using

# Application Configuration
SECRET_KEY=your_secret_key
DEBUG=False
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_WINDOW_SECONDS=60

# Book Content Configuration
BOOK_TITLE="AI-Native Software Development"
BOOK_AUTHOR="Author Name"
BOOK_PUBLICATION_YEAR=2024
```

### 3. Install Dependencies

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Database Setup

First, set up your Neon Postgres database and run migrations:

```bash
# Install Alembic if not already in requirements
pip install alembic

# Run the initial migration
alembic upgrade head
```

### 5. Populate Vector Database

Before the RAG system can work, you need to index the book content into Qdrant:

```bash
# Run the indexing script
python -m src.scripts.index_book_content --book-path /path/to/book/files
```

This process:
- Reads the book content (chapters, sections)
- Chunks content appropriately for semantic search
- Generates embeddings using a non-OpenAI model
- Stores chunks in Qdrant with metadata

## Running the Application

### Development Mode

```bash
# Activate your virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start the FastAPI server
uvicorn src.api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### Production Mode

```bash
# Using gunicorn (install with pip install gunicorn)
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Usage

### Basic Query

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the main principles of AI-native development?",
    "session_id": "unique-session-id"
  }'
```

### Selected-Text-Only Mode

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain the concept mentioned here",
    "selected_text": "The concept of AI-native development involves building systems from the ground up with AI as a core component rather than an afterthought...",
    "session_id": "unique-session-id"
  }'
```

### Response Format

```json
{
  "answer": "AI-native development involves building systems from the ground up with AI as a core component rather than an afterthought. This approach ensures that AI capabilities are deeply integrated into the system architecture, allowing for more sophisticated and effective AI implementations. [Citation: Author, 2024, Chapter 3]",
  "citations": [
    {
      "apa_text": "Author, A. (2024). Title of Book. Publisher. Chapter 3.",
      "source_chapter": "Chapter 3",
      "source_section": "3.2",
      "pages": [45, 47]
    }
  ],
  "retrieved_contexts": [
    {
      "content": "The concept of AI-native development involves building systems from the ground up with AI as a core component rather than an afterthought...",
      "source": "Chapter 3, Section 3.2, Pages 45-47",
      "similarity_score": 0.87
    }
  ],
  "selected_text_mode": false,
  "model_used": "qwen-7b"
}
```

## Frontend Integration

The backend provides a REST API that can be integrated into any frontend. For the embedded book widget:

1. Include the widget JavaScript in your book pages
2. Configure the API endpoint URL
3. The widget will handle text selection and API communication

Example frontend integration:

```html
<!-- Include the chat widget -->
<div id="book-chat-widget" data-book-section="chapter-3"></div>
<script src="/static/chat-widget.js"></script>
<script>
  BookChatWidget.init({
    apiEndpoint: 'http://localhost:8000/api/v1',
    bookSection: 'chapter-3'
  });
</script>
```

## Testing

Run the test suite:

```bash
# Activate your virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/
```

## Troubleshooting

1. **Cohere API errors**: Verify your `COHERE_API_KEY` is correct and has access to Qwen models
2. **Qdrant connection errors**: Check your `QDRANT_URL` and `QDRANT_API_KEY`
3. **Neon Postgres errors**: Ensure your database URL is correct and accessible
4. **No results found**: Verify the book content has been properly indexed in Qdrant

## Development

### Adding New Features

1. Modify the data model in `data-model.md` as needed
2. Update the API contracts in the `contracts/` directory
3. Implement the backend logic in `src/services/`
4. Add new endpoints in `src/api/routes/`
5. Write tests in the `tests/` directory
6. Update this quickstart guide if necessary

### Environment Variables for Development

Additional environment variables for development:

```env
# Enable debug output
DEBUG=True

# Use a local vector store for development instead of Qdrant Cloud
USE_LOCAL_QDRANT=True
LOCAL_QDRANT_PATH=./local_qdrant_storage

# Use test Cohere model
COHERE_MODEL=command-light-nightly
```