# Add Automation Scope to HubSpot Private App

Your HubSpot Private App needs the **Automation** scope to create workflows. Follow these steps:

## Step 1: Go to Your Private App

1. Log into HubSpot: https://app.hubspot.com
2. Click the **gear icon (⚙️)** in the top right
3. Go to **Integrations** → **Private Apps**
4. Find and click on **"Campaign Automation Tool"** (or whatever you named it)

## Step 2: Edit Scopes

1. Click the **"Scopes"** tab (or **"Auth"** tab, depending on your HubSpot version)
2. Look for the **"Automation"** section
3. Check these boxes:
   - ✅ **Automation** → **Read**
   - ✅ **Automation** → **Write**

## Step 3: Save Changes

1. Click **"Save"** or **"Update app"**
2. You may need to regenerate your access token after adding scopes

## Step 4: Regenerate Token (if needed)

If HubSpot asks you to regenerate the token:
1. Go to the **"Auth"** tab
2. Click **"Regenerate token"** or **"Show token"**
3. Copy the new token
4. Update your `.env` file with the new token:
   ```
   HUBSPOT_ACCESS_TOKEN=<your_new_token>
   ```

## Step 5: Test

After updating the scopes, run the campaign script again:
```bash
python -m src.run_campaign config/campaigns/gtc-nvidia-afterparty.yaml
```

The workflows should now be created successfully!

---

**Note:** If you don't see the "Automation" scope option, make sure you have:
- A HubSpot account with Automation/Workflows enabled
- Admin or appropriate permissions to modify Private Apps
- The correct HubSpot subscription tier (some scopes require Professional/Enterprise)
