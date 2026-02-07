# Railway Deployment Error - Troubleshooting Guide

## Common Railway Deployment Errors & Fixes

### Error 1: "No Procfile found" or "No start command"

**Fix:** Make sure `Procfile` exists and contains:
```
web: gunicorn webhook_server:app
```

### Error 2: "Module not found" or "gunicorn not found"

**Fix:** Make sure `requirements.txt` includes:
```
gunicorn>=21.2.0
```

### Error 3: "Port binding error" or "Cannot bind to port"

**Fix:** Railway automatically sets the PORT environment variable. The webhook_server.py should use:
```python
port = int(os.environ.get("PORT", 5000))
```

### Error 4: "Python version not specified"

**Fix:** Create `runtime.txt` file with:
```
python-3.9.18
```

### Error 5: Railway not detecting Flask app

**Fix:** Make sure Railway is using the correct start command:
- In Railway → Your service → Settings → Deploy
- Start Command should be: `gunicorn webhook_server:app`
- Or leave it blank to use Procfile

---

## Step-by-Step Fix

### 1. Check Railway Logs

1. In Railway, click your project
2. Click **"Logs"** tab
3. Look for the error message
4. Share the error with me so I can help fix it

### 2. Verify Files Are Pushed to GitHub

Make sure these files are in your GitHub repo:
- ✅ `Procfile`
- ✅ `requirements.txt` (with gunicorn)
- ✅ `webhook_server.py`
- ✅ `runtime.txt` (optional but recommended)

### 3. Check Railway Service Settings

1. In Railway, click your service
2. Click **"Settings"** tab
3. Check **"Build Command"** - should be empty or `pip install -r requirements.txt`
4. Check **"Start Command"** - should be empty (uses Procfile) or `gunicorn webhook_server:app`

### 4. Force Redeploy

1. In Railway, click your project
2. Click **"Deployments"** tab
3. Click **"Redeploy"** on the latest deployment
4. Or push a new commit to trigger redeploy

---

## Quick Fixes to Try

### Fix 1: Add runtime.txt

I've created `runtime.txt` for you. Commit and push it:

```bash
git add runtime.txt
git commit -m "Add Python runtime version"
git push origin main
```

### Fix 2: Verify Procfile

Make sure `Procfile` has no extension and contains exactly:
```
web: gunicorn webhook_server:app
```

### Fix 3: Check Railway Service Type

Railway might need you to specify it's a web service:
1. Click your service in Railway
2. Settings → Networking
3. Make sure it's set as a "Web Service" not "Background Worker"

---

## What Error Are You Seeing?

Please share:
1. **The exact error message** from Railway logs
2. **What step fails** (Building, Starting, etc.)
3. **Any error codes** or status messages

This will help me provide a specific fix!
