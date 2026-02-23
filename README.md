# Campaign Automation

Automation workflows for managing campaigns across HubSpot and Salesforce.

## Overview

This project provides two main workflows:

1. **Campaign Form Automation** - Automates campaign creation from HubSpot landing page forms
2. **List Upload Automation** - Uploads CSV contacts to HubSpot segments

Both workflows integrate with HubSpot and Salesforce to streamline campaign management.

## Quick Start

### 1. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in:

**Required:**
- `HUBSPOT_ACCESS_TOKEN` - HubSpot Private App token
- `SALESFORCE_USERNAME` - Salesforce username
- `SALESFORCE_PASSWORD` - Salesforce password
- `SALESFORCE_SECURITY_TOKEN` - Salesforce security token (if needed)

**Optional:**
- `ZAPIER_CAMPAIGN_CREATED_WEBHOOK` - Zapier webhook URL for campaign creation events

### 3. Set Up HubSpot Private App

Create a [HubSpot Private App](https://developers.hubspot.com/docs/api/private-apps) with these scopes:

**For Campaign Form Automation:**
- `marketing.campaigns.read`
- `marketing.campaigns.write`
- `crm.lists.read`
- `crm.lists.write`
- `automation.read` (optional, for workflow creation)
- `automation.write` (optional, for workflow creation)

**For List Upload:**
- `crm.objects.contacts.read`
- `crm.objects.contacts.write`
- `crm.lists.read`
- `crm.lists.write`

## Workflows

### Workflow 1: Campaign Form Automation

Automates campaign creation in HubSpot and Salesforce from a HubSpot landing page form submission.

**How it works:**
1. User fills out form on HubSpot landing page
2. JavaScript intercepts form submission
3. Webhook sends data to backend server
4. Backend creates campaigns in HubSpot and Salesforce
5. User receives confirmation with campaign IDs

**Setup:**
- See `workflows/campaign-form/README.md` for detailed setup instructions
- Copy `workflows/campaign-form/frontend/form-interceptor.js` to your HubSpot landing page
- Deploy `workflows/campaign-form/backend/webhook_server.py` (or use `webhook_server.py` in root)

**Usage:**
- Form submission automatically triggers campaign creation
- No manual steps required after initial setup

### Workflow 2: List Upload Automation

Uploads contacts from CSV files to HubSpot static segments (lists).

**How it works:**
1. Read CSV file with contact information
2. Create or update contacts in HubSpot (batch processing)
3. Find or create segment (static list) by name
4. Add contacts to segment in batches
5. Report results with summary statistics

**Usage:**
```bash
# Upload to segment by name
python workflows/list-upload/upload_contacts.py "attendees.csv" "Event Attendees - Registered"

# Upload to segment by list ID
python workflows/list-upload/upload_contacts.py "attendees.csv" --list-id 12345678
```

**Helper Scripts:**
```bash
# Find lists by pattern
python workflows/list-upload/scripts/find_list_ids.py "Event"

# List all HubSpot lists
python workflows/list-upload/scripts/list_lists.py
```

**Setup:**
- See `workflows/list-upload/README.md` for detailed instructions

## Project Structure

```
campaign-automation/
├── workflows/                  # Organized workflow scripts
│   ├── campaign-form/          # Workflow 1: Form automation
│   │   ├── frontend/
│   │   │   └── form-interceptor.js
│   │   ├── backend/
│   │   │   └── webhook_server.py
│   │   └── README.md
│   └── list-upload/           # Workflow 2: List upload
│       ├── upload_contacts.py
│       ├── scripts/
│       │   ├── find_list_ids.py
│       │   └── list_lists.py
│       └── README.md
├── src/                        # Core shared logic
│   ├── hubspot_client.py       # HubSpot API client
│   ├── salesforce_client.py    # Salesforce API client
│   └── run_campaign.py         # Campaign creation logic
├── config/                     # Campaign configurations
│   └── campaigns/
│       └── example-campaign.yaml
├── archive/                    # Archived files (reference only)
├── webhook_server.py           # Webhook server (backward compatibility)
├── requirements.txt           # Python dependencies
├── Procfile                   # Railway deployment config
├── runtime.txt                # Python version
└── README.md                  # This file
```

## Manual Campaign Creation (YAML)

You can also create campaigns manually using YAML configs:

1. Copy example campaign:
   ```bash
   cp config/campaigns/example-campaign.yaml config/campaigns/my-campaign.yaml
   ```

2. Edit `my-campaign.yaml` with your campaign details

3. Run campaign creation:
   ```bash
   python -m src.run_campaign config/campaigns/my-campaign.yaml
   ```

## Deployment

### Railway Deployment

The webhook server is configured for Railway deployment:

1. Connect your GitHub repository to Railway
2. Railway will detect `Procfile` and deploy automatically
3. Set environment variables in Railway dashboard
4. Update `WEBHOOK_URL` in `form-interceptor.js` with your Railway URL

**Note:** `webhook_server.py` in root is kept for backward compatibility. The production version is in `workflows/campaign-form/backend/webhook_server.py`.

## Configuration Reference

### Campaign YAML Structure

```yaml
name: "Campaign Name"
start_date: "2025-01-01"
end_date: "2025-01-31"
taxonomy:
  hubspot:
    channel: "Webinar"
  salesforce:
    Type: "Webinar"
hubspot:
  auto_create_segments: ["Registered", "Attended"]
  create_workflows: true
salesforce:
  status: "Planned"
  description: "Campaign description"
workflows:
  zapier_webhook_url: "https://hooks.zapier.com/..."
```

## Troubleshooting

### Common Issues

**"HUBSPOT_ACCESS_TOKEN required"**
- Set token in `.env` file or environment variables
- Verify token has required scopes

**"Form not detected"**
- Check browser console for detection attempts
- Verify form selectors match your HubSpot form structure

**"List ID not found"**
- Use `list_lists.py` to find correct list ID
- Or use `find_list_ids.py` to search by pattern

**Webhook errors**
- Check Railway deployment logs
- Verify `WEBHOOK_URL` is correct in JavaScript
- Ensure environment variables are set in Railway

### Getting Help

- Check workflow-specific READMEs:
  - `workflows/campaign-form/README.md`
  - `workflows/list-upload/README.md`
- Review archived documentation in `archive/docs/` if needed
- Check HubSpot and Salesforce API documentation

## Contributing

When adding new workflows:
1. Create new directory under `workflows/`
2. Include README.md with setup and usage instructions
3. Use consistent naming conventions
4. Update this README with workflow overview

## License

Internal use only - Fireworks Marketing Operations
