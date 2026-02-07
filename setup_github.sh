#!/bin/bash
# Script to set up GitHub repository for campaign-automation

echo "🚀 Setting up GitHub repository..."
echo ""

# Check if git is already initialized
if [ -d ".git" ]; then
    echo "⚠️  Git repository already initialized"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "📦 Initializing git repository..."
    git init
fi

echo ""
echo "📝 Adding files to git..."
git add .

echo ""
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Campaign automation tool with HubSpot and Salesforce integration

- Webhook server for HubSpot form submissions
- Campaign creation in HubSpot and Salesforce
- Automated workflow setup
- Ready for Railway deployment"

echo ""
echo "✅ Git repository initialized and files committed!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Create a GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Name: campaign-automation"
echo "   - Choose Private or Public"
echo "   - DO NOT initialize with README"
echo "   - Click 'Create repository'"
echo ""
echo "2. Connect and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/campaign-automation.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to Railway:"
echo "   - Go to https://railway.app"
echo "   - New Project → Deploy from GitHub repo"
echo "   - Select your repository"
echo ""
echo "See GITHUB_SETUP.md for detailed instructions!"
