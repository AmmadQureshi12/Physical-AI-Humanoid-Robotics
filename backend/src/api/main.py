"""
Main FastAPI application with CORS and middleware setup.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.middleware.rate_limiter import rate_limit_middleware
from src.core.config import settings
from src.core.logging_config import setup_logging
from src.core.qdrant_initializer import initialize_qdrant_collection
from src.database.init_db import init_db
import uvicorn
import atexit


# Initialize logging
setup_logging(log_level=settings.log_level)

# Create FastAPI app instance
app = FastAPI(
    title="Academic RAG Chatbot API",
    description="API for the Integrated RAG Chatbot for Academic Book",
    version="1.0.0",
    debug=settings.debug,
)


# Register startup event
@app.on_event("startup")
async def startup_event():
    """Async startup event handler."""
    try:
        # Initialize database tables - running in a thread to avoid blocking
        import asyncio
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, init_db)
        print("Database initialized successfully")

        # Initialize Qdrant collection
        initialize_qdrant_collection()
        print("Qdrant collection initialized successfully")
    except Exception as e:
        print(f"Error during startup initialization: {str(e)}")
        raise


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default port
        "http://localhost:3001",  # Alternative React port
        "http://127.0.0.1:3000",  # Alternative localhost format
        "http://127.0.0.1:3001",  # Alternative localhost format
        "http://localhost:8080",  # Common development servers
        "http://localhost:3002",  # Additional common port
        "http://localhost:3003",  # Additional common port
        "http://localhost:3004",  # Additional common port
        "http://localhost:3005",  # Additional common port
        "*"  # For development; restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose custom headers if needed
    # expose_headers=["Access-Control-Allow-Origin"]
)


# Add rate limiting middleware
@app.middleware("http")
async def add_rate_limit_middleware(request, call_next):
    """Apply rate limiting to all requests."""
    # Apply rate limiting
    rate_limit_middleware(request)
    # Continue with the request
    response = await call_next(request)
    return response


# Include API routes
from src.api.routes import query, health, chatbot
app.include_router(query.router, prefix="/api/v1", tags=["Query"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(chatbot.router, prefix="/api/v1", tags=["Chatbot"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint for the API."""
    return {
        "message": "Welcome to the Academic RAG Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    # Run the application with uvicorn when executed directly
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.debug else False,
        log_level=settings.log_level.lower()
    )