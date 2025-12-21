import uvicorn
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    print("Starting the Academic RAG Chatbot API server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation available at: http://localhost:8000/docs")
    
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )