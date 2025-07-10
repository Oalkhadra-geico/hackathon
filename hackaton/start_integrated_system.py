#!/usr/bin/env python3
"""
Integrated System Startup Script
This script starts both the backend server and the frontend UI.
"""

import subprocess
import time
import sys
import os
from threading import Thread

def start_backend():
    """Start the backend Flask server"""
    print("🚀 Starting backend server...")
    try:
        subprocess.run([sys.executable, "backend_server.py"], cwd=os.path.dirname(__file__))
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")

def start_frontend():
    """Start the frontend ReactPy UI"""
    print("🎨 Starting frontend UI...")
    time.sleep(3)  # Wait for backend to start
    try:
        subprocess.run([sys.executable, "ui/simple_react.py"], cwd=os.path.dirname(__file__))
    except KeyboardInterrupt:
        print("\n🛑 Frontend UI stopped")

def main():
    print("🔧 Starting Integrated DOI Research Assistant System")
    print("=" * 60)
    
    # Check if required files exist
    required_files = [
        "backend_server.py",
        "ui/simple_react.py",
        "ResponseData.xlsx",
        "completion.py",
        "agent.py",
        "vector_searcher.py",
        "embedding.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all files are present before running the system.")
        return
    
    print("✅ All required files found")
    print("\n📋 System Components:")
    print("   - Backend API Server (Flask)")
    print("   - Frontend UI (ReactPy)")
    print("   - LLM Integration")
    print("   - Data Processing")
    
    print("\n⚠️  Prerequisites:")
    print("   - OpenSearch should be running on localhost:9200")
    print("   - Required Python packages should be installed")
    print("   - ResponseData.xlsx should be indexed in OpenSearch")
    
    print("\n🚀 Starting system...")
    print("=" * 60)
    
    # Start backend in a separate thread
    backend_thread = Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Start frontend
    start_frontend()

if __name__ == "__main__":
    main()