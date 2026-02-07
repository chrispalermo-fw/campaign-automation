# Add CRM Properties Scope to HubSpot Private App

To create properties programmatically, you need to add the CRM Properties scope.

## Quick Steps

1. **Go to HubSpot Settings**
   - Click the **gear icon (⚙️)** in the top right
   - Go to **Integrations** → **Private Apps**

2. **Edit Your Private App**
   - Find **"Campaign Automation Tool"**
   - Click on it to edit

3. **Add CRM Properties Scope**
   - Go to the **Scopes** tab
   - Look for **CRM** section
   - Check:
     - ✅ **Properties** → **Read**
     - ✅ **Properties** → **Write**

4. **Save Changes**
   - Click **Save** or **Update app**
   - You may need to regenerate your access token

5. **Regenerate Token (if needed)**
   - Go to the **Auth** tab
   - Click **Regenerate token** or **Show token**
   - Copy the new token
   - Update your `.env` file:
     ```
     HUBSPOT_ACCESS_TOKEN=<your_new_token>
     ```

## Run the Script

After adding the scope:

```bash
python create_custom_properties.py
```

This will create all 11 properties automatically!

## What Gets Created

The script will create these properties:

**Required:**
- `campaign_name` - Campaign Name
- `start_date` - Campaign Start Date  
- `end_date` - Campaign End Date
- `member_statuses` - Campaign Member Statuses

**Optional:**
- `salesforce_status` - Salesforce Campaign Status
- `salesforce_description` - Salesforce Campaign Description
- `salesforce_type` - Salesforce Campaign Type
- `parent_campaign` - Parent Campaign Name
- `hubspot_notes` - Campaign HubSpot Notes
- `wait_minutes` - Campaign Wait Minutes
- `webhook_url` - Campaign Webhook URL

## After Properties Are Created

1. Go back to your form
2. Connect each form field to its property
3. Save the form
