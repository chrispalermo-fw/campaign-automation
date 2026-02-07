# Complete HubSpot Landing Page Setup Guide 🚀

This guide will help you set up a HubSpot landing page that automatically creates campaigns in HubSpot and Salesforce when you submit a form. **No workflows needed!**

---

## Part 1: Deploy Webhook Server

### Step 1: Files Are Ready ✅

The following files have been updated:
- ✅ `webhook_server.py` - Updated for production
- ✅ `requirements.txt` - Added gunicorn
- ✅ `Procfile` - Created for deployment

### Step 2: Deploy to Railway

1. **Push to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Prepare webhook server for deployment"
   git push origin main
   ```

2. **Go to Railway**:
   - Visit https://railway.app
   - Sign up/login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `campaign-automation` repository

3. **Railway will auto-detect Flask** and start deploying

4. **Add Environment Variables**:
   - Click your project → "Variables" tab
   - Add these (get values from your `.env` file):
     ```
     HUBSPOT_ACCESS_TOKEN=your-token-here
     SALESFORCE_USERNAME=your-username
     SALESFORCE_PASSWORD=your-password
     SALESFORCE_SECURITY_TOKEN=your-token
     ```

5. **Get Your Public URL**:
   - Railway will give you a URL like: `https://your-app.up.railway.app`
   - **Save this URL** - you'll need it for the JavaScript!

---

## Part 2: Create HubSpot Form

### Step 1: Create Form in HubSpot

1. Go to **HubSpot** → **Marketing** → **Forms** → **Create form**
2. **Form name**: `Campaign Automation Form`
3. **Form type**: Standard form

### Step 2: Add Required Fields

Click "Add field" for each:

#### 1. Campaign Name
- **Field type**: Single-line text
- **Field name**: `campaign_name` ← **CRITICAL: Must match exactly!**
- **Label**: "Campaign Name"
- **Required**: ✅ Yes
- **Placeholder**: "e.g., 1PEvent_GTC Nvidia Afterparty_San Jose_03162026"
- **Help text**: "Format: Type_name_Location_Date"
- **Connect to property**: ❌ Leave empty (custom field)

#### 2. Start Date
- **Field type**: Date picker
- **Field name**: `start_date` ← **CRITICAL: Must match exactly!**
- **Label**: "Start Date"
- **Required**: ✅ Yes
- **Connect to property**: ❌ Leave empty

#### 3. End Date
- **Field type**: Date picker
- **Field name**: `end_date` ← **CRITICAL: Must match exactly!**
- **Label**: "End Date"
- **Required**: ✅ Yes
- **Connect to property**: ❌ Leave empty

#### 4. Member Statuses
- **Field type**: Multi-line text (textarea)
- **Field name**: `member_statuses` ← **CRITICAL: Must match exactly!**
- **Label**: "Member Statuses"
- **Required**: ✅ Yes
- **Placeholder**: "Registered\nWaitlist\nAttended\nNo Show"
- **Help text**: "Enter one status per line"
- **Connect to property**: ❌ Leave empty

### Step 3: Add Optional Fields (Optional)

#### 5. Salesforce Status
- **Field type**: Single-line text
- **Field name**: `salesforce_status`
- **Label**: "Salesforce Campaign Status"
- **Required**: No
- **Default value**: "Planned"

#### 6. Campaign Description
- **Field type**: Multi-line text
- **Field name**: `salesforce_description`
- **Label**: "Campaign Description"
- **Required**: No

#### 7. Campaign Type
- **Field type**: Single-line text
- **Field name**: `salesforce_type`
- **Label**: "Campaign Type"
- **Required**: No
- **Placeholder**: "e.g., Event, Webinar, Email"

#### 8. Parent Campaign
- **Field type**: Single-line text
- **Field name**: `parent_campaign`
- **Label**: "Parent Campaign Name"
- **Required**: No

#### 9. HubSpot Notes
- **Field type**: Multi-line text
- **Field name**: `hubspot_notes`
- **Label**: "HubSpot Notes"
- **Required**: No

#### 10. Wait Minutes
- **Field type**: Number
- **Field name**: `wait_minutes`
- **Label**: "Wait Time Before Sync (minutes)"
- **Required**: No
- **Default value**: "10"

### Step 4: Save Form

Click "Save" or "Publish" to save your form.

---

## Part 3: Create HubSpot Landing Page

### Step 1: Create Landing Page

1. Go to **HubSpot** → **Marketing** → **Landing Pages** → **Create landing page**
2. **Name**: `Campaign Automation Tool`
3. Choose a template (any template works)

### Step 2: Add Form Module

1. In the page editor, click "Add module" or drag a module
2. Select "Form" module
3. Choose your "Campaign Automation Form"
4. Position it where you want on the page

### Step 3: Add JavaScript (CRITICAL!)

1. In the page editor, click **"Settings"** (gear icon)
2. Go to **"Advanced"** tab
3. Scroll to **"Custom HTML"** section
4. Add this code in the **"Footer HTML"** or **"Head HTML"** field:

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

### Step 4: Publish Landing Page

1. Click "Publish" or "Update"
2. Your landing page is now live!

---

## Part 4: Test It!

1. **Go to your landing page** (get URL from HubSpot)
2. **Fill out the form**:
   - Campaign Name: `Test Campaign_Location_02072026`
   - Start Date: Choose a date
   - End Date: Choose a date
   - Member Statuses: 
     ```
     Registered
     Waitlist
     Attended
     ```
3. **Click Submit**
4. **You should see**:
   - HubSpot form submission confirmation
   - Alert popup with campaign IDs
5. **Check**:
   - HubSpot → Marketing → Campaigns (should see new campaign)
   - Salesforce → Campaigns (should see new campaign)

---

## Troubleshooting

### Form not calling webhook

**Check:**
- JavaScript is added to landing page (Settings → Advanced → Custom HTML)
- Railway URL is correct in JavaScript
- Webhook server is running (check Railway dashboard)
- Browser console for errors (F12 → Console)

### Campaign not created

**Check:**
- Field names match exactly (`campaign_name`, `start_date`, etc.)
- Required fields are filled
- Environment variables are set in Railway
- Railway logs for errors

### Webhook returns error

**Check Railway logs:**
- Go to Railway dashboard → Your project → Deployments → View logs
- Look for error messages
- Common issues:
  - Missing environment variables
  - Invalid credentials
  - API scope issues

---

## Field Name Reference

Make sure your HubSpot form field names match these exactly:

| Field Name | Type | Required |
|------------|------|----------|
| `campaign_name` | text | ✅ Yes |
| `start_date` | date | ✅ Yes |
| `end_date` | date | ✅ Yes |
| `member_statuses` | textarea | ✅ Yes |
| `salesforce_status` | text | No |
| `salesforce_description` | textarea | No |
| `salesforce_type` | text | No |
| `parent_campaign` | text | No |
| `hubspot_notes` | textarea | No |
| `wait_minutes` | number | No |

---

## Next Steps

After campaigns are created:

1. **Configure Workflow Enrollment Triggers** (in HubSpot UI):
   - Go to Automation → Workflows
   - For each workflow, set enrollment trigger: "Contact is added to list"
   - Select the corresponding list ID

2. **Add "Set Salesforce Campaign" Action**:
   - In each workflow, delete placeholder action
   - Add: "Set Salesforce Campaign"
   - Map to correct Salesforce Campaign ID and Status

3. **Activate Workflows**

See `CONFIGURE_WORKFLOWS.md` for detailed instructions.

---

## Summary

✅ **Deploy webhook server** to Railway  
✅ **Create HubSpot form** with correct field names  
✅ **Create HubSpot landing page** with form  
✅ **Add JavaScript** to call webhook  
✅ **Test** by submitting form  

**Result**: Fill out form → Submit → Campaigns created automatically! 🎉
