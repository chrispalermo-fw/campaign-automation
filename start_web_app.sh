#!/bin/bash
# Startup script for the Campaign Automation Web App

echo "🚀 Starting Campaign Automation Web App..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask..."
    pip install -q Flask
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Make sure your credentials are configured."
fi

# Start the app
echo "✅ Starting web server..."
echo "📍 Open your browser to: http://localhost:5000"
echo ""
python app.py
