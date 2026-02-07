# Railway Deployment Checklist ✅

While Railway is deploying, here's what you can do:

---

## ✅ Pre-Deployment Checklist

### 1. Verify Form Field Names Match

Make sure your HubSpot form has these exact field names:

**Required:**
- ✅ `campaign_name` (text field)
- ✅ `start_date` (date field)
- ✅ `end_date` (date field)
- ✅ `member_statuses` (textarea)

**Optional:**
- `salesforce_status` (text)
- `salesforce_description` (textarea)
- `salesforce_type` (text)
- `parent_campaign` (text)
- `hubspot_notes` (textarea)
- `wait_minutes` (number)

**To check:** Go to HubSpot → Marketing → Forms → Edit your form → Check each field's "Field name"

---

## 🚀 During Deployment

### 2. Prepare JavaScript Snippet

1. Open `HUBSPOT_JAVASCRIPT_SNIPPET.js` (just created)
2. Copy the entire script
3. **Wait for Railway URL** before pasting (see step 3 below)

---

## ⏳ After Railway Deployment Completes

### 3. Get Your Railway URL

1. Go to Railway dashboard: https://railway.app
2. Click your project
3. Click **"Settings"** tab
4. Under **"Domains"**, you'll see your public URL
   - Example: `https://campaign-automation-production.up.railway.app`
5. **Copy this URL**

### 4. Add Environment Variables (if not done)

1. In Railway, click **"Variables"** tab
2. Add these (get values from your `.env` file):
   ```
   HUBSPOT_ACCESS_TOKEN=your-token-here
   SALESFORCE_USERNAME=your-username
   SALESFORCE_PASSWORD=your-password
   SALESFORCE_SECURITY_TOKEN=your-token
   ```
3. Railway will automatically redeploy

### 5. Test Webhook Endpoint

Once deployed, test that the webhook is working:

```bash
# Replace YOUR_RAILWAY_URL with your actual URL
curl -X POST https://YOUR_RAILWAY_URL/webhook/campaign-create \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Test Campaign",
    "start_date": "2026-02-07",
    "end_date": "2026-02-07",
    "member_statuses": "Registered\nWaitlist"
  }'
```

Or test the health endpoint:
```bash
curl https://YOUR_RAILWAY_URL/health
```

Should return: `{"status":"ok"}`

---

## 📝 Add JavaScript to HubSpot Landing Page

### 6. Update JavaScript with Railway URL

1. Open `HUBSPOT_JAVASCRIPT_SNIPPET.js`
2. Find this line:
   ```javascript
   const WEBHOOK_URL = 'YOUR_RAILWAY_URL/webhook/campaign-create';
   ```
3. Replace `YOUR_RAILWAY_URL` with your actual Railway URL
   - Example: `https://campaign-automation-production.up.railway.app`
4. **Don't include** `/webhook/campaign-create` in the URL replacement
   - Final should be: `'https://your-app.up.railway.app/webhook/campaign-create'`

### 7. Add to HubSpot Landing Page

1. Go to **HubSpot** → **Marketing** → **Landing Pages**
2. Click **"Edit"** on your landing page
3. Click **"Settings"** (gear icon)
4. Go to **"Advanced"** tab
5. Scroll to **"Custom HTML"** section
6. Paste the updated JavaScript in **"Footer HTML"**
7. Click **"Publish"** or **"Update"**

---

## 🧪 Test Everything

### 8. Test Form Submission

1. Go to your HubSpot landing page
2. Fill out the form:
   - Campaign Name: `Test Campaign_Location_02072026`
   - Start Date: Choose a date
   - End Date: Choose a date
   - Member Statuses:
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

### 9. Check Logs (if issues)

**Railway Logs:**
- Railway dashboard → Your project → Deployments → View logs
- Look for errors or webhook requests

**Browser Console:**
- Press F12 → Console tab
- Look for JavaScript errors or webhook responses

---

## 🎉 Success!

Once everything works:
- ✅ Form submits
- ✅ Webhook is called
- ✅ Campaigns created in HubSpot and Salesforce
- ✅ Success message shows campaign IDs

**You're done!** 🚀

---

## 🆘 Troubleshooting

### Webhook returns 500 error
- Check Railway logs for errors
- Verify environment variables are set
- Check credentials are correct

### Form not calling webhook
- Open browser console (F12)
- Check for JavaScript errors
- Verify Railway URL is correct
- Make sure JavaScript is in Footer HTML

### Campaigns not created
- Check Railway logs
- Verify HubSpot and Salesforce credentials
- Check API scopes/permissions

---

## Quick Reference

- **JavaScript file**: `HUBSPOT_JAVASCRIPT_SNIPPET.js`
- **Railway dashboard**: https://railway.app
- **HubSpot forms**: HubSpot → Marketing → Forms
- **HubSpot landing pages**: HubSpot → Marketing → Landing Pages
