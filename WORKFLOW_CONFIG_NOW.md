# HubSpot Workflow Configuration - Copy & Paste

## ✅ Everything is Ready!

- ✅ Webhook server: Running
- ✅ ngrok: Running  
- ✅ Public URL: `https://nonobligatory-defamatorily-lonnie.ngrok-free.dev`

## Create Workflow in HubSpot

### Step 1: Go to Workflows

**HubSpot** → **Automation** → **Workflows** → **Create workflow**

### Step 2: Basic Settings

- **Workflow Name**: `Campaign Creation Webhook`

### Step 3: Enrollment Trigger

1. Click **"Add enrollment trigger"**
2. Select: **"Contact submits form"**
3. Choose: **"Campaign Automation Form"**
4. Click **"Save"**

### Step 4: Add Webhook Action

1. Click **"Add action"**
2. Search for: **"Send webhook"**
3. Click **"Send webhook"**

### Step 5: Configure Webhook

**Webhook URL**: 
```
https://nonobligatory-defamatorily-lonnie.ngrok-free.dev/webhook/campaign-create
```

**HTTP Method**: `POST`

**Request Body Type**: `JSON`

**Request Body**: Copy this EXACTLY:
```json
{
  "campaign_name": "{{ form.campaign_name }}",
  "start_date": "{{ form.start_date }}",
  "end_date": "{{ form.end_date }}",
  "member_statuses": "{{ form.member_statuses }}",
  "salesforce_status": "{{ form.salesforce_status }}",
  "salesforce_description": "{{ form.salesforce_description }}",
  "salesforce_type": "{{ form.salesforce_type }}",
  "parent_campaign": "{{ form.parent_campaign }}",
  "hubspot_notes": "{{ form.hubspot_notes }}",
  "wait_minutes": "{{ form.wait_minutes }}",
  "webhook_url": "{{ form.webhook_url }}"
}
```

### Step 6: Activate

1. Click **"Save"** on the webhook action
2. Toggle **"Activate"** in the top right
3. Confirm activation

## 🎉 Test It!

1. Go to your landing page
2. Fill out the form
3. Submit
4. Watch campaigns appear automatically!

## Check Results

- **Webhook server terminal**: Should show campaign creation logs
- **HubSpot** → Marketing → Campaigns: New campaign
- **Salesforce** → Campaigns: New campaign  
- **HubSpot** → Automation → Workflows: New workflows created

## Important Notes

- **ngrok URL changes** if you restart ngrok (free tier)
- For production, deploy webhook server to cloud and use that URL
- Keep ngrok running while testing
- Webhook server must stay running for it to work
