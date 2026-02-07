# Debug Steps - Form Not Working 🔍

Let's debug step by step:

---

## Issue 1: Environment Variables Not Loading

The webhook test showed: `"HUBSPOT_ACCESS_TOKEN required"`

**Fix this first:**

1. **In Railway**, go to your project → **Variables** tab
2. **Verify** these variables exist:
   - `HUBSPOT_ACCESS_TOKEN`
   - `SALESFORCE_USERNAME`
   - `SALESFORCE_PASSWORD`
   - `SALESFORCE_SECURITY_TOKEN`

3. **Check the values:**
   - Make sure there are no extra spaces
   - Make sure values are correct
   - Copy/paste from your `.env` file to be sure

4. **Redeploy:**
   - After checking variables, Railway should auto-redeploy
   - Or click "Redeploy" in the Deployments tab

5. **Test again:**
   ```bash
   curl https://campaign-automation-production-c59f.up.railway.app/health
   ```
   Should return: `{"status":"ok"}`

---

## Issue 2: JavaScript Not Finding Form

**Check browser console:**

1. Go to your HubSpot landing page
2. Press **F12** (or `Cmd+Option+I` on Mac)
3. Click **Console** tab
4. Submit the form
5. Look for:
   - ✅ "Campaign automation script starting..."
   - ✅ "Found form with selector: ..."
   - ✅ "Form submitted, preparing webhook call..."
   - ❌ "HubSpot form not found" = form detection issue
   - ❌ Any red errors = JavaScript error

**Share what you see in the console!**

---

## Issue 3: Improved JavaScript

I've created `HUBSPOT_JAVASCRIPT_IMPROVED.js` with:
- Better form detection (tries multiple selectors)
- More debugging (logs everything)
- Retry logic (tries multiple times)

**Replace the JavaScript in HubSpot with the improved version:**

1. Open `HUBSPOT_JAVASCRIPT_IMPROVED.js`
2. Copy the entire script
3. Go to HubSpot → Landing Pages → Edit your page
4. Settings → Advanced → Custom HTML → Footer HTML
5. Replace the old script with the new one
6. Publish

---

## Quick Test Checklist

- [ ] Railway Variables tab shows all 4 variables
- [ ] Railway deployment is active
- [ ] Browser console shows "Campaign automation script starting..."
- [ ] Browser console shows "Found form..."
- [ ] Browser console shows "Form submitted..."
- [ ] Browser console shows "Calling webhook..."
- [ ] Railway logs show incoming webhook request

---

## What to Share

Please share:
1. **Railway Variables tab** - Are all 4 variables there?
2. **Browser console output** - What messages do you see?
3. **Railway logs** - Any errors when submitting form?

This will help me identify the exact issue!
