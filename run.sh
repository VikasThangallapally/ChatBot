#!/bin/bash
# Startup script for Brain Tumor Chatbot

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Create uploads directory
mkdir -p app/static/uploads

# Start the application
echo "Starting Brain Tumor Chatbot API..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
