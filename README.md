# Campaign Automation: HubSpot → Salesforce

Create campaigns in **HubSpot** and **Salesforce** from a single YAML config. Use the same definition to set campaign name, taxonomy, tags, list/segment associations, and to trigger workflows (e.g. Zapier) that move data between the two systems.

## What it does

1. **Creates the campaign name in both systems** – One config field, two campaigns (HubSpot + Salesforce).
2. **Applies taxonomy & tags** – Map to your custom properties in each system via `taxonomy.hubspot` and `taxonomy.salesforce`.
3. **Adds lists/segments in HubSpot** – Associates static lists (and optionally segments) with the HubSpot campaign as assets.
4. **Salesforce campaign** – Creates the campaign with Type, Status, Description; your sync workflow can add Campaign Members from HubSpot list data.
5. **Workflows** – Optionally calls a Zapier webhook (or similar) with the new campaign IDs so your Zaps can turn on or run (e.g. “when campaign created, sync list to SF campaign members”).

## Setup

### 1. Install dependencies

```bash
cd /Users/chris/Documents/campaign-automation
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Environment variables

Copy `.env.example` to `.env` and fill in:

- **HubSpot**: Create a [Private App](https://developers.hubspot.com/docs/api/private-apps) with scopes `marketing.campaigns.read` and `marketing.campaigns.write`. Put the access token in `HUBSPOT_ACCESS_TOKEN`.
- **Salesforce**: Use a Connected App or username/password + security token. Set `SALESFORCE_USERNAME`, `SALESFORCE_PASSWORD`, `SALESFORCE_SECURITY_TOKEN`.
- **Zapier (optional)**: Set `ZAPIER_CAMPAIGN_CREATED_WEBHOOK` to the webhook URL that should run when a campaign is created (e.g. a Zap trigger).

### 3. Get HubSpot list IDs

In HubSpot: **Marketing > Lead Management > Lists**. Open a list; the ID is in the URL (`.../list/12345678`) or use the [Lists API](https://developers.hubspot.com/docs/api/crm/lists) to list them. Put those IDs in `hubspot.list_ids` in your YAML.

## Usage

1. Copy the example campaign and edit it:

   ```bash
   cp config/campaigns/example-campaign.yaml config/campaigns/my-campaign.yaml
   ```

2. Edit `my-campaign.yaml`:
   - Set `name`, `start_date`, `end_date`.
   - Set `taxonomy.hubspot` and `taxonomy.salesforce` to match your property/field names.
   - Set `hubspot.list_ids` to the HubSpot list IDs to associate.
   - Set `salesforce.status` and `description` as needed.
   - Optionally set `workflows.zapier_webhook_url` (or use env `ZAPIER_CAMPAIGN_CREATED_WEBHOOK`).

3. Run the automation:

   ```bash
   python -m src.run_campaign config/campaigns/my-campaign.yaml
   ```

4. The script prints HubSpot campaign ID and Salesforce campaign ID. Use these in Zapier or HubSpot workflows to:
   - Sync the HubSpot list to Salesforce Campaign Members.
   - Turn on or trigger other workflows that move data between the two systems.

## Config reference

| Section | Purpose |
|--------|---------|
| `name` | Campaign name (used in both HubSpot and Salesforce). |
| `start_date` / `end_date` | YYYY-MM-DD; applied in HubSpot (and SF if you map them). |
| `taxonomy.hubspot` | Key-value of HubSpot campaign property internal names. |
| `taxonomy.salesforce` | Key-value of Salesforce Campaign field names (e.g. `Type`, `Region__c`). |
| `tags` | List of tags; map to a HubSpot property via `hubspot.extra_properties` if needed. |
| `hubspot.list_ids` | List of HubSpot list IDs to associate as OBJECT_LIST assets. |
| `hubspot.extra_properties` | Any other HubSpot campaign properties (e.g. `hs_notes`, `hs_campaign_status`). |
| `salesforce.status` | Campaign status (e.g. Planned, Active). |
| `salesforce.description` | Campaign description. |
| `workflows.zapier_webhook_url` | Webhook URL to call after creation (payload includes both campaign IDs). |

## Turning on workflows (Zapier)

- **Webhook trigger**: Create a Zap with trigger “Webhooks by Zapier > Catch Hook”. Use that URL as `ZAPIER_CAMPAIGN_CREATED_WEBHOOK` or in `workflows.zapier_webhook_url`. The payload will include `hubspot_campaign_id`, `salesforce_campaign_id`, and `campaign_name` so the Zap can add members or enable other Zaps.
- **Campaign members in Salesforce**: In the Zap, add a step that uses the HubSpot list (or “Contacts in list”) and creates Campaign Members in Salesforce for the created `salesforce_campaign_id`.

## Project layout

```
campaign-automation/
├── config/campaigns/     # One YAML per campaign
├── src/
│   ├── hubspot_client.py
│   ├── salesforce_client.py
│   └── run_campaign.py
├── .env.example
├── requirements.txt
└── README.md
```
