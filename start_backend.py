#!/usr/bin/env python
"""
Script to start the backend server for the AI-Humanoid Robotics chatbot.
"""
import subprocess
import sys
import os
from pathlib import Path

def start_backend():
    """Start the backend server."""
    backend_dir = Path(__file__).parent / "backend"
    
    # Change to the backend directory
    os.chdir(backend_dir)
    
    print("Starting backend server...")
    print("Navigate to http://localhost:8000/docs to view the API documentation")
    
    # Start the server using uvicorn
    try:
        result = subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"  # Enable auto-reload during development
        ])
        
        if result.returncode != 0:
            print("Error starting the backend server")
            sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nBackend server stopped by user")
    except Exception as e:
        print(f"Error starting backend server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_backend()