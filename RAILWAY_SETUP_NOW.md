# Railway Setup - Step by Step 🚀

Follow these steps to complete your Railway deployment:

---

## Step 1: Verify Deployment

1. In Railway dashboard, click your **campaign-automation** project
2. Check the **"Deployments"** tab
3. Wait for deployment to complete (should show "Active" status)
4. If there are errors, check the logs

---

## Step 2: Add Environment Variables

Railway needs your API credentials to connect to HubSpot and Salesforce.

1. In Railway, click your project
2. Click **"Variables"** tab
3. Click **"New Variable"** and add each one:

   **Variable Name:** `HUBSPOT_ACCESS_TOKEN`  
   **Value:** (get from your `.env` file - starts with `pat-na2-...`)

   **Variable Name:** `SALESFORCE_USERNAME`  
   **Value:** (your Salesforce username from `.env`)

   **Variable Name:** `SALESFORCE_PASSWORD`  
   **Value:** (your Salesforce password from `.env`)

   **Variable Name:** `SALESFORCE_SECURITY_TOKEN`  
   **Value:** (your Salesforce security token from `.env`)

4. After adding each variable, Railway will automatically redeploy

**Note:** Get these values from your `.env` file in the project directory.

---

## Step 3: Get Your Railway URL

1. In Railway, click your project
2. Click **"Settings"** tab
3. Scroll to **"Domains"** section
4. You'll see your public URL, something like:
   - `https://campaign-automation-production.up.railway.app`
   - Or `https://campaign-automation-production-xxxx.up.railway.app`
5. **Copy this URL** - you'll need it for the JavaScript!

---

## Step 4: Test the Webhook

Once deployed, test that it's working:

### Test Health Endpoint:
```bash
curl https://YOUR_RAILWAY_URL/health
```

Should return: `{"status":"ok"}`

### Test Webhook Endpoint:
```bash
curl -X POST https://YOUR_RAILWAY_URL/webhook/campaign-create \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Test Campaign",
    "campaign_start_date": "2026-02-07",
    "campaign_end_date": "2026-02-07",
    "campaign_member_statuses": "Registered\nWaitlist"
  }'
```

Should return a success response with campaign IDs.

---

## Step 5: Update JavaScript with Railway URL

1. Open `HUBSPOT_JAVASCRIPT_SNIPPET.js` in your project
2. Find this line:
   ```javascript
   const WEBHOOK_URL = 'YOUR_RAILWAY_URL/webhook/campaign-create';
   ```
3. Replace `YOUR_RAILWAY_URL` with your actual Railway URL
   - Example: `https://campaign-automation-production.up.railway.app`
   - Final should be: `'https://your-app.up.railway.app/webhook/campaign-create'`
4. **Save the file**

---

## Step 6: Add JavaScript to HubSpot Landing Page

1. Go to **HubSpot** → **Marketing** → **Landing Pages**
2. Find your landing page and click **"Edit"**
3. Click **"Settings"** (gear icon) in the page editor
4. Go to **"Advanced"** tab
5. Scroll to **"Custom HTML"** section
6. Paste the updated JavaScript from `HUBSPOT_JAVASCRIPT_SNIPPET.js` into **"Footer HTML"**
7. Click **"Publish"** or **"Update"**

---

## Step 7: Test Everything!

1. Go to your HubSpot landing page
2. Fill out the form:
   - **Campaign Name**: `Test Campaign_Location_02072026`
   - **Start Date**: Choose a date
   - **End Date**: Choose a date
   - **Member Statuses**: 
     ```
     Registered
     Waitlist
     Attended
     ```
3. Click **"Submit"**
4. You should see:
   - HubSpot form confirmation
   - Alert popup with campaign IDs
5. Check:
   - **HubSpot** → Marketing → Campaigns (new campaign should appear)
   - **Salesforce** → Campaigns (new campaign should appear)

---

## Troubleshooting

### Railway deployment fails
- Check Railway logs: Railway dashboard → Your project → Deployments → View logs
- Common issues:
  - Missing environment variables
  - Python version mismatch
  - Missing dependencies

### Webhook returns 500 error
- Check Railway logs for errors
- Verify environment variables are set correctly
- Check HubSpot and Salesforce credentials

### Form not calling webhook
- Open browser console (F12 → Console)
- Check for JavaScript errors
- Verify Railway URL is correct in JavaScript
- Make sure JavaScript is in Footer HTML

### Campaigns not created
- Check Railway logs
- Verify HubSpot and Salesforce credentials
- Check API scopes/permissions

---

## Quick Reference

- **Railway dashboard**: https://railway.app
- **JavaScript file**: `HUBSPOT_JAVASCRIPT_SNIPPET.js`
- **Webhook endpoint**: `https://YOUR_RAILWAY_URL/webhook/campaign-create`
- **Health endpoint**: `https://YOUR_RAILWAY_URL/health`

---

## Field Names Reference

Your HubSpot form fields:
- `campaign_name` ✅
- `campaign_start_date` ✅
- `campaign_end_date` ✅
- `campaign_member_statuses` ✅

The webhook supports both naming conventions, so you're all set!
