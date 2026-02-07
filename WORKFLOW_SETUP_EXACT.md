# Exact Workflow Setup Instructions

Copy and paste these exact steps to set up your workflow.

## Step 1: Get Your Webhook URL

**Run these commands:**

```bash
# Terminal 1: Start webhook server
cd /Users/chris/Documents/campaign-automation
./start_webhook_server.sh
```

```bash
# Terminal 2: Start ngrok (in a new terminal)
ngrok http 5000
```

**Copy the HTTPS URL** from ngrok (looks like `https://abc123.ngrok.io`)

## Step 2: Create Workflow in HubSpot

### Exact Steps:

1. **Go to**: HubSpot → Automation → Workflows → **Create workflow**

2. **Workflow Name**: `Campaign Creation Webhook`

3. **Enrollment Trigger**:
   - Click **"Add enrollment trigger"**
   - Select: **"Contact submits form"**
   - Choose: **"Campaign Automation Form"**
   - Click **"Save"**

4. **Add Webhook Action**:
   - Click **"Add action"**
   - Search for: **"Send webhook"**
   - Click **"Send webhook"**

5. **Configure Webhook**:
   
   **Webhook URL**: 
   ```
   https://YOUR-NGROK-URL.ngrok.io/webhook/campaign-create
   ```
   (Replace `YOUR-NGROK-URL` with your actual ngrok URL)
   
   **HTTP Method**: `POST`
   
   **Request Body Type**: `JSON`
   
   **Request Body**: Copy this EXACTLY (all of it):
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

6. **Save and Activate**:
   - Click **"Save"** on the webhook action
   - Toggle **"Activate"** in the top right
   - Confirm activation

## Step 3: Test

1. Go to your landing page
2. Fill out and submit the form
3. Check:
   - Webhook server terminal (should show logs)
   - HubSpot → Marketing → Campaigns (new campaign)
   - Salesforce → Campaigns (new campaign)

## Troubleshooting

### Webhook URL Format
Make sure it's exactly:
```
https://abc123.ngrok.io/webhook/campaign-create
```
(No trailing slash, use `/webhook/campaign-create` endpoint)

### Form Field Names
HubSpot workflow uses `{{ form.field_name }}` syntax. Make sure field names match:
- `campaign_name`
- `start_date`
- `end_date`
- `member_statuses`
- etc.

### Test Webhook Manually
If workflow isn't working, test webhook directly:
```bash
curl -X POST http://localhost:5000/webhook/campaign-create \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Test",
    "start_date": "2026-02-07",
    "end_date": "2026-02-07",
    "member_statuses": "Registered\nWaitlist"
  }'
```
