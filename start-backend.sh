#!/bin/bash

# Start Backend Script for TodoList Application
# This script sets up and runs the Python FastAPI backend

echo "🚀 Starting TodoList Backend..."

# Navigate to backend directory
cd "$(dirname "$0")/backend" || exit 1

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env exists, create from example if not
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📝 Creating .env file from .env.example..."
        cp .env.example .env
    else
        echo "📝 Creating default .env file..."
        echo "MONGODB_URL=mongodb://localhost:27017" > .env
    fi
fi

# Start the server
echo "✅ Starting FastAPI server on http://localhost:8080"
echo "📖 API Documentation available at http://localhost:8080/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
