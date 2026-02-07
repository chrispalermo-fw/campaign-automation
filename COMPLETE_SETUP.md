# Complete Setup Guide - Final Steps

You're almost there! Here's what's left to make everything work end-to-end.

## ✅ What You've Done

- [x] Created form with all fields
- [x] Created custom properties
- [x] Connected form fields to properties
- [x] Created landing page
- [x] Added form to landing page

## 🎯 What's Left

### Step 1: Start Your Webhook Server

The webhook server receives form submissions and creates campaigns automatically.

**Option A: Local Testing (with ngrok)**

```bash
# Terminal 1: Start webhook server
./start_webhook_server.sh

# Terminal 2: Expose it with ngrok
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)

**Option B: Production Deployment**

Deploy `webhook_server.py` to:
- Heroku
- AWS Lambda
- Google Cloud Run
- Any cloud service

### Step 2: Create HubSpot Workflow

This connects your form to the webhook server.

1. **Go to HubSpot** → **Automation** → **Workflows** → **Create workflow**

2. **Set Enrollment Trigger:**
   - Trigger: **"Contact submits form"**
   - Select: **"Campaign Automation Form"**

3. **Add Action: Send webhook**

   **Webhook Configuration:**
   - **Webhook URL**: 
     - Local: `https://your-ngrok-url.ngrok.io/webhook/campaign-create`
     - Production: `https://your-domain.com/webhook/campaign-create`
   
   - **HTTP Method**: POST
   
   - **Request Body Type**: JSON
   
   - **Request Body**: Copy this exactly:
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
   - Send yourself an email when campaigns are created
   - Include: `{{ workflow.webhook_response }}`

5. **Activate the workflow**

### Step 3: Test Everything

1. **Go to your landing page**
2. **Fill out the form**:
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
3. **Submit the form**
4. **Check results**:
   - HubSpot → Marketing → Campaigns (should see new campaign)
   - Salesforce → Campaigns (should see new campaign)
   - HubSpot → Automation → Workflows → Check activity
   - Check webhook server logs for any errors

### Step 4: Configure Workflow Enrollment Triggers

After campaigns are created, you need to configure the workflows that sync list enrollments to Salesforce:

1. **Go to HubSpot** → **Automation** → **Workflows**
2. **For each workflow** (Registered, Waitlist, Attended, No Show):
   - Open the workflow
   - **Enrollment tab** → Add trigger: "Contact is added to list"
   - Select the corresponding list
   - **Actions tab** → Delete placeholder action
   - **Actions tab** → Add: "Set Salesforce Campaign"
     - Campaign: (your Salesforce campaign ID)
     - Status: (match the workflow status)
   - **Activate**

See `CONFIGURE_WORKFLOWS.md` for detailed instructions.

## 🎉 You're Done!

Once everything is set up:
1. ✅ Fill out form on landing page
2. ✅ Campaigns created automatically
3. ✅ Lists/segments created
4. ✅ Workflows created
5. ✅ When contacts are added to lists → Synced to Salesforce after 10 minutes

## Troubleshooting

### Webhook not receiving data
- Check webhook server is running
- Verify URL is correct (no typos)
- Check workflow is activated
- Test webhook URL with curl (see below)

### Campaign creation fails
- Check `.env` file has all credentials
- Verify HubSpot API token has correct scopes
- Check Salesforce credentials
- Look at webhook server error logs

### Test Webhook Manually

```bash
curl -X POST http://localhost:5000/webhook/campaign-create \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Test Campaign",
    "start_date": "2026-02-07",
    "end_date": "2026-02-07",
    "member_statuses": "Registered\nWaitlist"
  }'
```

## Next Steps After Testing

1. ✅ Test with real campaign data
2. ✅ Configure all workflow enrollment triggers
3. ✅ Add "Set Salesforce Campaign" actions to workflows
4. ✅ Activate all workflows
5. ✅ Test end-to-end: Add contact to list → Check Salesforce
