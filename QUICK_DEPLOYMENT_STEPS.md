# Quick Deployment Steps 🚀

Since you already have the HubSpot form and landing page, here's what's left:

---

## Step 1: Deploy Webhook Server to Railway

### 1. Push to GitHub

```bash
cd /Users/chris/Documents/campaign-automation
git add .
git commit -m "Prepare webhook server for deployment"
git push origin main
```

### 2. Deploy on Railway

1. Go to **https://railway.app**
2. Sign up/login with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your `campaign-automation` repository
5. Railway will auto-detect Flask and start deploying

### 3. Add Environment Variables

1. Click your project → **"Variables"** tab
2. Click **"New Variable"** and add each:
   - `HUBSPOT_ACCESS_TOKEN` = (your token from `.env`)
   - `SALESFORCE_USERNAME` = (your username from `.env`)
   - `SALESFORCE_PASSWORD` = (your password from `.env`)
   - `SALESFORCE_SECURITY_TOKEN` = (your token from `.env`)

### 4. Get Your Public URL

1. Railway will give you a URL like: `https://your-app.up.railway.app`
2. **Copy this URL** - you'll need it in the next step!

---

## Step 2: Add JavaScript to Your Landing Page

### 1. Edit Your Landing Page

1. Go to **HubSpot** → **Marketing** → **Landing Pages**
2. Find your landing page and click **"Edit"**

### 2. Add JavaScript

1. Click **"Settings"** (gear icon) in the page editor
2. Go to **"Advanced"** tab
3. Scroll to **"Custom HTML"** section
4. Paste this code in **"Footer HTML"**:

```html
<script>
(function() {
  // ⚠️ REPLACE THIS WITH YOUR RAILWAY URL!
  const WEBHOOK_URL = 'https://your-app.up.railway.app/webhook/campaign-create';
  
  // Wait for page to load
  window.addEventListener('load', function() {
    // Find HubSpot form
    const form = document.querySelector('form[data-form-id]');
    
    if (!form) {
      console.error('HubSpot form not found');
      return;
    }
    
    // Listen for form submission
    form.addEventListener('submit', function(e) {
      // Let HubSpot process the form first, then call webhook
      setTimeout(function() {
        // Collect form data
        const data = {};
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(function(input) {
          const name = input.getAttribute('name') || input.getAttribute('data-name');
          if (name) {
            if (input.type === 'checkbox' || input.type === 'radio') {
              if (input.checked) {
                data[name] = input.value;
              }
            } else {
              data[name] = input.value;
            }
          }
        });
        
        // Build payload
        const payload = {
          campaign_name: data.campaign_name || '',
          start_date: data.start_date || '',
          end_date: data.end_date || '',
          member_statuses: data.member_statuses || '',
          salesforce_status: data.salesforce_status || 'Planned',
          salesforce_description: data.salesforce_description || '',
          salesforce_type: data.salesforce_type || '',
          parent_campaign: data.parent_campaign || '',
          hubspot_notes: data.hubspot_notes || '',
          wait_minutes: data.wait_minutes || '10',
          webhook_url: data.webhook_url || ''
        };
        
        // Call webhook
        fetch(WEBHOOK_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(result => {
          console.log('✅ Campaign created:', result);
          if (result.status === 'success') {
            alert('🎉 Campaign created successfully!\n\nHubSpot Campaign ID: ' + result.data.hubspot_campaign_id + '\nSalesforce Campaign ID: ' + result.data.salesforce_campaign_id);
          } else {
            alert('⚠️ Campaign creation completed with warnings. Check console for details.');
          }
        })
        .catch(error => {
          console.error('❌ Error creating campaign:', error);
          alert('❌ Error creating campaign. Please check console for details or contact support.');
        });
      }, 1500); // Wait 1.5 seconds for HubSpot to process form
    });
  });
})();
</script>
```

5. **⚠️ IMPORTANT**: Replace `https://your-app.up.railway.app` with your actual Railway URL!

### 3. Publish

1. Click **"Publish"** or **"Update"**
2. Done! 🎉

---

## Step 3: Test It!

1. Go to your landing page URL
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
3. Click **Submit**
4. You should see:
   - HubSpot form submission confirmation
   - Alert popup with campaign IDs
5. Check:
   - **HubSpot** → Marketing → Campaigns (should see new campaign)
   - **Salesforce** → Campaigns (should see new campaign)

---

## Troubleshooting

### Form field names don't match

Make sure your HubSpot form field names are exactly:
- `campaign_name` (required)
- `start_date` (required)
- `end_date` (required)
- `member_statuses` (required)
- `salesforce_status` (optional)
- `salesforce_description` (optional)
- `salesforce_type` (optional)
- `parent_campaign` (optional)
- `hubspot_notes` (optional)
- `wait_minutes` (optional)

### Webhook not being called

1. Open browser console (F12 → Console)
2. Check for JavaScript errors
3. Verify Railway URL is correct in the JavaScript
4. Check Railway logs (Railway dashboard → Your project → Deployments → View logs)

### Campaign not created

1. Check Railway logs for errors
2. Verify environment variables are set correctly
3. Check that your HubSpot and Salesforce credentials are valid

---

## That's It! 🎉

Once deployed and JavaScript is added, your flow will be:
**Fill out form → Submit → Campaigns created automatically!**
