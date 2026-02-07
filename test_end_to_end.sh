#!/bin/bash
# Test script to verify the end-to-end flow works

echo "🧪 Testing Campaign Automation End-to-End"
echo "========================================"
echo ""

# Check if webhook server is running
echo "1. Checking webhook server..."
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "   ✅ Webhook server is running"
else
    echo "   ❌ Webhook server is NOT running"
    echo "   → Start it with: ./start_webhook_server.sh"
    exit 1
fi

# Test webhook endpoint
echo ""
echo "2. Testing webhook endpoint..."
response=$(curl -s -X POST http://localhost:5000/webhook/campaign-create \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Test Campaign Automation",
    "start_date": "2026-02-07",
    "end_date": "2026-02-07",
    "member_statuses": "Registered\nWaitlist"
  }')

if echo "$response" | grep -q "success"; then
    echo "   ✅ Webhook endpoint is working!"
    echo "   Response: $response" | head -c 200
    echo ""
else
    echo "   ⚠️  Webhook returned: $response"
fi

echo ""
echo "3. Next steps:"
echo "   - Make sure ngrok is running: ngrok http 5000"
echo "   - Create HubSpot workflow with ngrok URL"
echo "   - Test by submitting form on landing page"
echo ""
echo "See FINAL_SETUP_STEPS.md for complete instructions"
