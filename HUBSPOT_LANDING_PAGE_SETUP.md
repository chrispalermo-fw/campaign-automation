# HubSpot Landing Page Setup Guide

This guide will help you create a HubSpot landing page with a form that triggers campaign creation.

## Overview

The flow works like this:
1. **HubSpot Landing Page** → Form submission
2. **HubSpot Workflow** → Triggers webhook
3. **Webhook Server** → Creates campaign in HubSpot & Salesforce
4. **Response** → Returns campaign IDs

## Step 1: Set Up the Webhook Server

### Option A: Run Locally (for testing)

```bash
# Start the webhook server
source .venv/bin/activate
python webhook_server.py
```

The server will run on `http://localhost:5000`

**For production**, you'll need to:
- Deploy to a cloud service (Heroku, AWS, Google Cloud, etc.)
- Use a service like ngrok to expose localhost (for testing)
- Or use a service like Zapier/Make.com as a proxy

### Option B: Use ngrok (for local testing with HubSpot)

```bash
# Install ngrok: https://ngrok.com/download
# Start webhook server
python webhook_server.py

# In another terminal, expose it
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) - you'll use this in HubSpot.

### Option C: Deploy to Production

Deploy `webhook_server.py` to:
- **Heroku**: `git push heroku main`
- **AWS Lambda**: Use Serverless Framework
- **Google Cloud Run**: `gcloud run deploy`
- **Any cloud provider** that supports Python/Flask

## Step 2: Create HubSpot Form Fields

Go to **HubSpot** → **Marketing** → **Forms** → **Create form**

Create these form fields:

### Required Fields:

1. **Campaign Name** (Single-line text)
   - Field name: `campaign_name`
   - Label: "Campaign Name"
   - Required: Yes
   - Help text: "Format: Type_name_Location_Date (e.g., 1PEvent_GTC Nvidia Afterparty_San Jose_03162026)"

2. **Start Date** (Date picker)
   - Field name: `start_date`
   - Label: "Start Date"
   - Required: Yes

3. **End Date** (Date picker)
   - Field name: `end_date`
   - Label: "End Date"
   - Required: Yes

4. **Member Statuses** (Multi-line text)
   - Field name: `member_statuses`
   - Label: "Member Statuses"
   - Required: Yes
   - Help text: "Enter one status per line: Registered, Waitlist, Attended, No Show"

### Optional Fields:

5. **Salesforce Status** (Dropdown)
   - Field name: `salesforce_status`
   - Label: "Salesforce Campaign Status"
   - Options: Planned, In Progress, Completed, Cancelled
   - Default: Planned

6. **Salesforce Description** (Multi-line text)
   - Field name: `salesforce_description`
   - Label: "Campaign Description"

7. **Salesforce Type** (Single-line text)
   - Field name: `salesforce_type`
   - Label: "Campaign Type"
   - Help text: "e.g., Event, Webinar, Email"

8. **Parent Campaign** (Single-line text)
   - Field name: `parent_campaign`
   - Label: "Parent Campaign Name (Optional)"

9. **HubSpot Notes** (Multi-line text)
   - Field name: `hubspot_notes`
   - Label: "HubSpot Campaign Notes"

10. **Wait Minutes** (Number)
    - Field name: `wait_minutes`
    - Label: "Wait Time Before Sync (minutes)"
    - Default: 10

11. **Webhook URL** (Single-line text)
    - Field name: `webhook_url`
    - Label: "Custom Webhook URL (Optional)"

## Step 3: Create HubSpot Landing Page

1. Go to **Marketing** → **Landing Pages** → **Create landing page**

2. **Choose a template** or start from scratch

3. **Add your form**:
   - Drag the form module onto the page
   - Select the form you created in Step 2

4. **Customize the page**:
   - Add a title: "Campaign Automation Tool"
   - Add description explaining what the form does
   - Style it to match your brand

5. **Publish the page**

## Step 4: Create HubSpot Workflow

1. Go to **Automation** → **Workflows** → **Create workflow**

2. **Set Enrollment Trigger**:
   - Trigger: "Contact submits form"
   - Select your campaign creation form

3. **Add Action: Send webhook**

   - **Webhook URL**: Your webhook server URL
     - Local testing: `http://your-ngrok-url.ngrok.io/webhook/campaign-create`
     - Production: `https://your-domain.com/webhook/campaign-create`
   
   - **HTTP Method**: POST
   
   - **Request Body Type**: JSON
   
   - **Request Body**: Map form fields to JSON:
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

4. **Add Action: Send email notification** (Optional)
   - Send yourself an email with the campaign creation results
   - Include: `{{ workflow.webhook_response }}`

5. **Activate the workflow**

## Step 5: Test the Integration

1. **Fill out the form** on your landing page
2. **Submit the form**
3. **Check the workflow**:
   - Go to Automation → Workflows
   - Open your workflow
   - Check the "Activity" tab for the webhook response
4. **Verify campaigns**:
   - Check HubSpot → Marketing → Campaigns
   - Check Salesforce → Campaigns

## Troubleshooting

### Webhook not receiving data

**Check:**
- Webhook server is running
- URL is correct (no typos)
- HubSpot workflow is activated
- Form submission is triggering the workflow

**Debug:**
- Check webhook server logs
- Check HubSpot workflow activity logs
- Test webhook URL with curl:
  ```bash
  curl -X POST http://your-webhook-url/webhook/campaign-create \
    -H "Content-Type: application/json" \
    -d '{"campaign_name":"Test","start_date":"2026-02-07","end_date":"2026-02-07","member_statuses":"Registered\nWaitlist"}'
  ```

### Form fields not mapping correctly

**Check:**
- Field names in HubSpot form match the webhook JSON
- Field names use underscores (not spaces)
- Required fields are filled

### Campaign creation fails

**Check:**
- Environment variables are set (`.env` file)
- HubSpot API token has correct scopes
- Salesforce credentials are correct
- Check webhook server error logs

## Field Name Reference

Make sure your HubSpot form field names match these:

| HubSpot Field Name | Description |
|-------------------|-------------|
| `campaign_name` | Campaign name (required) |
| `start_date` | Start date (required) |
| `end_date` | End date (required) |
| `member_statuses` | Member statuses, one per line (required) |
| `salesforce_status` | Salesforce campaign status (optional) |
| `salesforce_description` | Campaign description (optional) |
| `salesforce_type` | Campaign type (optional) |
| `parent_campaign` | Parent campaign name (optional) |
| `hubspot_notes` | HubSpot notes (optional) |
| `wait_minutes` | Wait time in minutes (optional) |
| `webhook_url` | Custom webhook URL (optional) |

## Example Webhook Request Body

```json
{
  "campaign_name": "1PEvent_Test Campaign_San Francisco_02072026",
  "start_date": "2026-02-07",
  "end_date": "2026-02-07",
  "member_statuses": "Registered\nWaitlist\nAttended\nNo Show",
  "salesforce_status": "Planned",
  "salesforce_description": "Test campaign",
  "salesforce_type": "Event",
  "parent_campaign": "",
  "hubspot_notes": "Created via HubSpot landing page",
  "wait_minutes": "10",
  "webhook_url": ""
}
```

## Next Steps

After setting up:

1. ✅ Test form submission
2. ✅ Verify campaigns are created
3. ✅ Configure workflow enrollment triggers (see `CONFIGURE_WORKFLOWS.md`)
4. ✅ Add "Set Salesforce Campaign" actions to workflows
5. ✅ Activate all workflows

## Security Considerations

For production:

1. **Add authentication** to webhook endpoint
2. **Use HTTPS** (required for production)
3. **Validate webhook signature** (HubSpot can sign webhooks)
4. **Rate limiting** to prevent abuse
5. **Error logging** and monitoring
