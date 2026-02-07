#!/bin/bash
# Start ngrok tunnel for webhook server

echo "🔗 Starting ngrok tunnel..."
echo ""

# Check if ngrok is configured
if [ ! -f ~/.ngrok2/ngrok.yml ] && [ ! -f ~/Library/Application\ Support/ngrok/ngrok.yml ]; then
    echo "⚠️  ngrok requires authentication!"
    echo ""
    echo "Quick setup:"
    echo "1. Sign up: https://dashboard.ngrok.com/signup"
    echo "2. Get authtoken: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "3. Run: ./ngrok config add-authtoken YOUR_TOKEN"
    echo ""
    echo "Or use localtunnel (no signup):"
    echo "  npm install -g localtunnel && lt --port 5000"
    echo ""
    exit 1
fi

# Start ngrok
cd /Users/chris/Documents/campaign-automation
./ngrok http 5000
