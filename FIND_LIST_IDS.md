# How to Find HubSpot List IDs

Since the Lists API doesn't have read permissions, you need to find the list IDs manually. Here's how:

## Method 1: From HubSpot UI (Easiest)

1. **Go to HubSpot**: https://app.hubspot.com
2. **Navigate to Lists**: 
   - Click **Contacts** in the top menu
   - Click **Lists** in the left sidebar
3. **Find your lists**:
   - Search for: `1PEvent_ GTC Nvidia Afterparty_San Jose_03162026`
   - You should see 4 lists:
     - `1PEvent_ GTC Nvidia Afterparty_San Jose_03162026 - Registered`
     - `1PEvent_ GTC Nvidia Afterparty_San Jose_03162026 - Waitlist`
     - `1PEvent_ GTC Nvidia Afterparty_San Jose_03162026 - Attended`
     - `1PEvent_ GTC Nvidia Afterparty_San Jose_03162026 - No Show`

4. **Get the List ID**:
   - Click on each list to open it
   - Look at the URL in your browser
   - The URL will look like: `https://app.hubspot.com/contacts/44215135/lists/827`
   - The number after `/lists/` is the List ID (e.g., `827`)

## Method 2: From List Settings

1. Open a list
2. Click the **Settings** tab (gear icon)
3. Scroll down - the List ID is usually shown there

## Method 3: From Campaign Assets

1. Go to **Marketing** → **Campaigns**
2. Open your campaign: `1PEvent_ GTC Nvidia Afterparty_San Jose_03162026`
3. Click on the **Assets** tab
4. You should see the associated lists with their IDs

## After Finding the IDs

Once you have all 4 list IDs, update your YAML config file:

```yaml
hubspot:
  list_ids:
    - 827   # Registered (replace with actual ID)
    - 828   # Waitlist (replace with actual ID)
    - 829   # Attended (replace with actual ID)
    - 830   # No Show (replace with actual ID)
  
  list_status_map:
    "827": "Registered"
    "828": "Waitlist"
    "829": "Attended"
    "830": "No Show"
```

Then run the campaign script again:
```bash
python -m src.run_campaign config/campaigns/gtc-nvidia-afterparty.yaml
```

The workflows will be created automatically!
