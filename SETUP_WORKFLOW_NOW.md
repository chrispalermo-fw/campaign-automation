# Set Up Workflow Right Now - Copy & Paste Guide

I've started your webhook server! Here's exactly what to do next.

## ✅ Webhook Server Status

The webhook server should be starting. Check if it's running:

```bash
curl http://localhost:5000/health
```

If you see `{"status":"ok"}`, the server is running!

## Step 1: Get Public URL (ngrok)

You need ngrok to expose your local server to HubSpot.

### Install ngrok (if needed):

```bash
# macOS
brew install ngrok

# Or download from: https://ngrok.com/download
```

### Start ngrok:

```bash
ngrok http 5000
```

**Copy the HTTPS URL** - it looks like:
```
https://abc123-def456.ngrok.io
```

## Step 2: Create Workflow in HubSpot

**Go to**: HubSpot → Automation → Workflows → **Create workflow**

### Exact Configuration:

**Workflow Name**: `Campaign Creation Webhook`

**Enrollment Trigger**:
1. Click **"Add enrollment trigger"**
2. Select: **"Contact submits form"**
3. Choose: **"Campaign Automation Form"**
4. Save

**Add Webhook Action**:
1. Click **"Add action"**
2. Search: **"Send webhook"**
3. Click it

**Webhook Settings**:
- **Webhook URL**: 
  ```
  https://YOUR-NGROK-URL.ngrok.io/webhook/campaign-create
  ```
  (Replace `YOUR-NGROK-URL` with your ngrok URL)

- **HTTP Method**: `POST`

- **Request Body Type**: `JSON`

- **Request Body**: Copy this EXACTLY:
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

**Activate**: Toggle "Activate" in top right

## Step 3: Test It!

1. **Go to your landing page**
2. **Fill out form**:
   - Campaign Name: `1PEvent_Test Campaign_San Francisco_02072026`
   - Start Date: `2026-02-07`
   - End Date: `2026-02-07`
   - Member Statuses:
     ```
     Registered
     Waitlist
     Attended
     No Show
     ```
3. **Submit**
4. **Watch the magic!** ✨

## What Should Happen

1. Form submits → Workflow triggers
2. Webhook sends data to your server
3. Server creates:
   - ✅ HubSpot campaign
   - ✅ Salesforce campaign
   - ✅ HubSpot lists/segments
   - ✅ Salesforce campaign member statuses
   - ✅ HubSpot workflows
4. You see campaigns appear in both systems!

## Check Results

- **Webhook server terminal**: Should show logs of campaign creation
- **HubSpot** → Marketing → Campaigns: New campaign
- **Salesforce** → Campaigns: New campaign
- **HubSpot** → Automation → Workflows: New workflows created

## Next: Configure Workflow Enrollment

After campaigns are created, configure the workflows to sync to Salesforce (see `CONFIGURE_WORKFLOWS.md`)
