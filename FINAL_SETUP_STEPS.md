# Final Setup Steps - Make It Work! 🚀

You're so close! Here's exactly what to do to make everything work end-to-end.

## Current Status ✅

- [x] Form created and published
- [x] Properties created
- [x] Landing page created with form

## Final Steps 🎯

### Step 1: Start Your Webhook Server

**Terminal 1: Start the server**

```bash
cd /Users/chris/Documents/campaign-automation
./start_webhook_server.sh
```

You should see:
```
🔗 Starting HubSpot Webhook Server...
✅ Starting webhook server...
📍 Webhook endpoint: http://localhost:5000/webhook/campaign-create
```

**Terminal 2: Expose with ngrok (for HubSpot to reach it)**

```bash
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`) - you'll need this for the workflow!

### Step 2: Create HubSpot Workflow

This connects your form to the webhook server.

1. **Go to HubSpot** → **Automation** → **Workflows** → **Create workflow**

2. **Workflow Name**: `Campaign Creation Webhook`

3. **Set Enrollment Trigger:**
   - Click **"Add enrollment trigger"**
   - Select: **"Contact submits form"**
   - Choose: **"Campaign Automation Form"**

4. **Add Action: Send webhook**

   Click **"Add action"** → **"Send webhook"**
   
   **Configure:**
   - **Webhook URL**: `https://your-ngrok-url.ngrok.io/webhook/campaign-create`
     - Replace `your-ngrok-url` with your actual ngrok URL
   
   - **HTTP Method**: POST
   
   - **Request Body Type**: JSON
   
   - **Request Body**: Copy this EXACTLY (including the curly braces):
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

5. **Activate the workflow** (toggle in top right)

### Step 3: Test It! 🧪

1. **Go to your landing page** (HubSpot → Marketing → Landing Pages → Campaign Automation Tool)

2. **Fill out the form:**
   - **Campaign Name**: `1PEvent_Test Campaign_San Francisco_02072026`
   - **Start Date**: `2026-02-07`
   - **End Date**: `2026-02-07`
   - **Member Statuses**:
     ```
     Registered
     Waitlist
     Attended
     No Show
     ```
   - Leave other fields as defaults

3. **Submit the form**

4. **Watch the magic happen!** ✨
   - Check webhook server terminal - you should see logs
   - Check HubSpot → Marketing → Campaigns (new campaign should appear)
   - Check Salesforce → Campaigns (new campaign should appear)
   - Check HubSpot → Automation → Workflows (new workflows created)

### Step 4: Configure Workflow Enrollment Triggers

After campaigns are created, configure the workflows that sync to Salesforce:

1. **Go to HubSpot** → **Automation** → **Workflows**
2. **Find workflows** named like:
   - `1PEvent_Test Campaign_San Francisco_02072026 - Registered`
   - `1PEvent_Test Campaign_San Francisco_02072026 - Waitlist`
   - etc.

3. **For each workflow:**
   - Open it
   - **Enrollment tab** → Add trigger: "Contact is added to list"
   - Select the corresponding list (e.g., "Registered" list)
   - **Actions tab** → Delete the placeholder action
   - **Actions tab** → Add: "Set Salesforce Campaign"
     - Campaign: (the Salesforce campaign ID from the results)
     - Status: (match the status: Registered, Waitlist, etc.)
   - **Activate**

See `CONFIGURE_WORKFLOWS.md` for detailed instructions.

## 🎉 You're Done!

Now you can:
1. Go to your landing page anytime
2. Fill out the form
3. Submit
4. Watch campaigns, lists, and workflows appear automatically!

## Quick Test Checklist

- [ ] Webhook server running (`./start_webhook_server.sh`)
- [ ] ngrok running and URL copied
- [ ] HubSpot workflow created and activated
- [ ] Webhook URL set correctly in workflow
- [ ] Form submitted on landing page
- [ ] Campaigns created in HubSpot and Salesforce
- [ ] Workflows created
- [ ] Workflow enrollment triggers configured
- [ ] "Set Salesforce Campaign" actions added
- [ ] All workflows activated

## Troubleshooting

### "Webhook failed" in HubSpot workflow
- Check webhook server is running
- Verify ngrok URL is correct
- Check webhook server logs for errors
- Test webhook manually (see below)

### Campaigns not created
- Check `.env` file has all credentials
- Verify API scopes are correct
- Check webhook server error logs

### Test Webhook Manually

```bash
curl -X POST http://localhost:5000/webhook/campaign-create \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Test Campaign",
    "start_date": "2026-02-07",
    "end_date": "2026-02-07",
    "member_statuses": "Registered\nWaitlist\nAttended\nNo Show"
  }'
```

## Next: Production Deployment

For production use:
1. Deploy webhook server to cloud (Heroku, AWS, etc.)
2. Update workflow webhook URL to production URL
3. Set up monitoring/alerting
4. Document for your team
