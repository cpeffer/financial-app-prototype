#!/bin/bash

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY is not set!"
    echo ""
    echo "To enable automatic receipt OCR, you need a Google Gemini API key."
    echo "Get one at: https://aistudio.google.com/app/apikey"
    echo ""
    read -p "Enter your Gemini API key (or press Enter to skip): " api_key
    if [ ! -z "$api_key" ]; then
        export GEMINI_API_KEY="$api_key"
        echo "✅ API key set!"
    else
        echo "ℹ️  Running without OCR. You can set GEMINI_API_KEY later."
    fi
    echo ""
fi

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/bin/flask" ]; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Run the Flask application
echo "Starting Receipt Tracker..."
echo "Access at: http://localhost:5000"
echo ""
python app.py
