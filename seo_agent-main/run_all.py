#!/usr/bin/env python3
"""
Run Backend and Frontend simultaneously
Works on Windows, Mac, and Linux
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def run_all():
    """Run backend and frontend simultaneously"""
    
    print("\n" + "=" * 70)
    print("🚀 SEO AGENT - STARTING BACKEND + FRONTEND")
    print("=" * 70)
    
    # Get project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if venv exists
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("\n❌ ERROR: Virtual environment not found!")
        print("Please run: python -m venv venv")
        print("Then run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if .env exists
    env_path = project_root / ".env"
    if not env_path.exists():
        print("\n❌ ERROR: .env file not found!")
        print("Please create .env with your GROQ_API_KEY")
        sys.exit(1)
    
    print("\n📍 Starting Backend Server...")
    print("   🔗 Backend: http://127.0.0.1:8000")
    print("   📚 API Docs: http://127.0.0.1:8000/docs")
    
    # Start backend
    backend_process = subprocess.Popen(
        [sys.executable, "backend/main.py"],
        cwd=project_root
    )
    
    # Wait for backend to initialize
    print("   ⏳ Waiting for backend to start...")
    time.sleep(3)
    
    print("\n🌐 Starting Frontend Server...")
    print("   🔗 Frontend: http://localhost:8080")
    
    # Start frontend
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8080", "--directory", "frontend"],
        cwd=project_root
    )
    
    print("\n" + "=" * 70)
    print("✅ BOTH SERVERS ARE RUNNING!")
    print("=" * 70)
    print("\n📌 OPEN IN BROWSER: http://localhost:8080")
    print("\n🔑 To stop: Press Ctrl+C in this terminal")
    print("\n" + "=" * 70 + "\n")
    
    # Keep processes running
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n\n⛔ Shutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        
        # Wait for processes to terminate
        try:
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            frontend_process.kill()
        
        print("✅ Servers stopped\n")
        sys.exit(0)

if __name__ == "__main__":
    run_all()
