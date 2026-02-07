#!/bin/bash
# Startup script for the HubSpot webhook server

echo "🔗 Starting HubSpot Webhook Server..."
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

# Start the webhook server
echo "✅ Starting webhook server..."
echo "📍 Webhook endpoint: http://localhost:5000/webhook/campaign-create"
echo "📍 Health check: http://localhost:5000/health"
echo ""
echo "💡 For HubSpot integration:"
echo "   1. Use ngrok to expose: ngrok http 5000"
echo "   2. Use the ngrok URL in HubSpot workflow webhook action"
echo ""
python webhook_server.py
