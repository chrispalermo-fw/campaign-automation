# Quick Start: HubSpot Landing Page Setup

## The Fastest Way

Since HubSpot's Forms API has limitations, **creating the form manually in HubSpot UI is actually faster and easier**. Here's the quickest path:

## 5-Minute Setup

### 1. Create Form (2 minutes)

1. HubSpot → **Marketing** → **Forms** → **Create form**
2. Name: `Campaign Automation Form`
3. Add these 4 required fields:
   - **Campaign Name** (text) - name: `campaign_name`
   - **Start Date** (date) - name: `start_date`
   - **End Date** (date) - name: `end_date`
   - **Member Statuses** (textarea) - name: `member_statuses`
4. Save form

### 2. Create Landing Page (1 minute)

1. HubSpot → **Marketing** → **Landing Pages** → **Create landing page**
2. Name: `Campaign Automation Tool`
3. Add heading: "🚀 Campaign Automation Tool"
4. Drag form module → Select "Campaign Automation Form"
5. Publish

### 3. Create Workflow (2 minutes)

1. HubSpot → **Automation** → **Workflows** → **Create workflow**
2. Trigger: "Contact submits form" → Select your form
3. Action: "Send webhook"
   - URL: `http://your-webhook-url/webhook/campaign-create`
   - Method: POST
   - Body: See `HUBSPOT_LANDING_PAGE_SETUP.md` for JSON mapping
4. Activate

## Done! 🎉

Your landing page is ready. Go to **Marketing** → **Landing Pages** → Find "Campaign Automation Tool"

## Need Help?

- **Detailed form setup**: See `CREATE_LANDING_PAGE_MANUAL.md`
- **Webhook configuration**: See `HUBSPOT_LANDING_PAGE_SETUP.md`
- **Webhook server**: Run `./start_webhook_server.sh`
