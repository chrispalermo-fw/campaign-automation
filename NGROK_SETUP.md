# ngrok Setup - Quick Guide

ngrok now requires a free account. Here's how to set it up:

## Option 1: Set Up ngrok (Recommended)

### Step 1: Sign Up (Free)

1. Go to: https://dashboard.ngrok.com/signup
2. Sign up with your email (free account)
3. Verify your email

### Step 2: Get Your Authtoken

1. After signing up, go to: https://dashboard.ngrok.com/get-started/your-authtoken
2. Copy your authtoken (looks like: `2abc123def456...`)

### Step 3: Configure ngrok

Run this command (replace with your actual token):

```bash
cd /Users/chris/Documents/campaign-automation
./ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

### Step 4: Start ngrok

```bash
./ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

## Option 2: Use Alternative - localtunnel (No Signup)

If you don't want to sign up for ngrok, use localtunnel instead:

```bash
# Install localtunnel
npm install -g localtunnel

# Start tunnel
lt --port 5000
```

This will give you a URL like `https://abc123.loca.lt`

## Option 3: Deploy to Cloud (Production)

For production, deploy the webhook server to:
- **Heroku**: Free tier available
- **AWS Lambda**: Serverless
- **Google Cloud Run**: Free tier
- **Railway**: Easy deployment

Then use that URL directly (no ngrok needed).

## Quick Start Commands

After setting up ngrok authtoken:

```bash
# Terminal 1: Webhook server (already running)
# Should be running at http://localhost:5000

# Terminal 2: Start ngrok
cd /Users/chris/Documents/campaign-automation
./ngrok http 5000
```

Copy the HTTPS URL and use it in your HubSpot workflow!
