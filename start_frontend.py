#!/usr/bin/env python
"""
Script to start the frontend development server for the AI-Humanoid Robotics chatbot.
"""
import subprocess
import sys
import os
from pathlib import Path

def start_frontend():
    """Start the frontend development server."""
    frontend_dir = Path(__file__).parent / "book"

    # Change to the frontend directory
    os.chdir(frontend_dir)
    
    print("Starting frontend development server...")
    print("Navigate to http://localhost:3000 to view the application")
    
    # Start the frontend using npm
    try:
        result = subprocess.run([
            "npm", "start"
        ])
        
        if result.returncode != 0:
            print("Error starting the frontend development server")
            sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nFrontend development server stopped by user")
    except Exception as e:
        print(f"Error starting frontend development server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_frontend()