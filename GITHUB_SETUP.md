# GitHub Setup Guide 🚀

Follow these steps to set up your GitHub repository and deploy to Railway.

---

## Step 1: Initialize Git Repository

Open your terminal and run these commands:

```bash
cd /Users/chris/Documents/campaign-automation

# Initialize git repository
git init

# Add all files (except .env and .venv which are in .gitignore)
git add .

# Create initial commit
git commit -m "Initial commit: Campaign automation tool with HubSpot and Salesforce integration"
```

---

## Step 2: Create GitHub Repository

### Option A: Using GitHub Website (Easiest)

1. Go to **https://github.com/new**
2. **Repository name**: `campaign-automation` (or any name you prefer)
3. **Description**: "Automated campaign creation for HubSpot and Salesforce"
4. **Visibility**: Choose Private (recommended) or Public
5. **DO NOT** check "Initialize with README" (we already have files)
6. Click **"Create repository"**

### Option B: Using GitHub CLI (if you have it)

```bash
gh repo create campaign-automation --private --source=. --remote=origin --push
```

---

## Step 3: Connect Local Repository to GitHub

After creating the GitHub repository, GitHub will show you commands. Use these:

```bash
# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/campaign-automation.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Note**: If you used GitHub CLI in Step 2, you can skip this step.

---

## Step 4: Deploy to Railway

1. Go to **https://railway.app**
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub (if needed)
5. Select your `campaign-automation` repository
6. Railway will automatically detect Flask and start deploying

---

## Step 5: Add Environment Variables in Railway

1. In Railway, click your project
2. Click **"Variables"** tab
3. Click **"New Variable"** and add each:

   ```
   HUBSPOT_ACCESS_TOKEN=your-token-from-env-file
   SALESFORCE_USERNAME=your-username-from-env-file
   SALESFORCE_PASSWORD=your-password-from-env-file
   SALESFORCE_SECURITY_TOKEN=your-token-from-env-file
   ```

   **Important**: Get these values from your `.env` file (which is NOT pushed to GitHub for security)

4. Railway will automatically redeploy with the new variables

---

## Step 6: Get Your Public URL

1. In Railway, click your project
2. Click **"Settings"** tab
3. Under **"Domains"**, Railway will show your public URL
   - Example: `https://campaign-automation-production.up.railway.app`
4. **Copy this URL** - you'll need it for the HubSpot JavaScript!

---

## Step 7: Add JavaScript to HubSpot Landing Page

1. Go to **HubSpot** → **Marketing** → **Landing Pages**
2. Edit your landing page
3. Click **"Settings"** → **"Advanced"** → **"Custom HTML"**
4. Add the JavaScript from `QUICK_DEPLOYMENT_STEPS.md`
5. **Replace** `https://your-app.up.railway.app` with your actual Railway URL
6. Publish the page

---

## Troubleshooting

### Git push asks for credentials

If GitHub asks for username/password:
- Use a **Personal Access Token** instead of password
- Create one: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
- Or use GitHub CLI: `gh auth login`

### Railway deployment fails

1. Check Railway logs: Railway dashboard → Your project → Deployments → View logs
2. Common issues:
   - Missing environment variables
   - Python version mismatch
   - Missing dependencies

### Files not showing in GitHub

Make sure you:
- Ran `git add .` to stage files
- Ran `git commit` to commit files
- Ran `git push` to push to GitHub

---

## What Gets Pushed to GitHub?

✅ **Pushed** (safe):
- All Python code (`src/`, `app.py`, `webhook_server.py`)
- Configuration files (`requirements.txt`, `Procfile`)
- Documentation (`.md` files)
- Templates (`templates/`)
- Example configs (`config/`)

❌ **NOT Pushed** (excluded by `.gitignore`):
- `.env` (contains secrets)
- `.venv/` (virtual environment)
- `__pycache__/` (Python cache)
- `.DS_Store` (macOS files)

---

## Next Steps

After deployment:
1. ✅ Get Railway URL
2. ✅ Add JavaScript to HubSpot landing page
3. ✅ Test form submission
4. ✅ Verify campaigns are created

See `QUICK_DEPLOYMENT_STEPS.md` for the complete flow!
