# Salesforce API Setup Guide - OAuth with Connected App

This guide walks you through setting up OAuth authentication with Salesforce using a Connected App.

## Why OAuth?

- ✅ More secure than security tokens
- ✅ Works with IP restrictions
- ✅ No need to reset security tokens when password changes
- ✅ Standard OAuth flow you're already familiar with
- ✅ Better for production environments

---

## Step-by-Step Setup

### Step 1: Create a Connected App in Salesforce

This method is more secure and doesn't require security tokens.

1. **Log into Salesforce** → Click the gear icon (⚙️) → **Setup**

2. **Navigate to Connected Apps:**
   - In Quick Find, type: `App Manager`
   - Click **App Manager**
   - Click **New Connected App** (top right)

3. **Fill in Connected App details:**
   - **Connected App Name**: `Campaign Automation Tool`
   - **API Name**: `Campaign_Automation_Tool` (auto-filled)
   - **Contact Email**: Your email
   - **Enable OAuth Settings**: ✅ Check this box
   - **Callback URL**: `http://localhost:8080/oauth/callback` (required but not used for username-password flow)
   - **Selected OAuth Scopes**: Move these to the right:
     - `Access and manage your data (api)` - **Required**
     - `Perform requests on your behalf at any time (refresh_token, offline_access)` - **Required**
   - **Require Secret for Web Server Flow**: ✅ Check this box
   - Click **Save**

4. **Get your credentials:**
   - After saving, you'll see a page with:
     - **Consumer Key** (Client ID) - Copy this!
     - **Consumer Secret** (Client Secret) - Click **Click to reveal** and copy this!
   - **Important:** Save these values securely - you'll need them for your `.env` file

5. **Wait for activation (if needed):**
   - Sometimes Connected Apps take 2-10 minutes to activate
   - If you get authentication errors, wait a few minutes and try again

### Step 2: Set up your `.env` file

1. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

2. **Fill in your OAuth credentials:**
   ```
   SALESFORCE_CONSUMER_KEY=3MVG9...your-consumer-key-here
   SALESFORCE_CONSUMER_SECRET=ABC123...your-consumer-secret-here
   SALESFORCE_USERNAME=your-email@company.com
   SALESFORCE_PASSWORD=YourPassword123
   ```

3. **If using a Salesforce Sandbox:**
   ```
   SALESFORCE_DOMAIN=test
   ```
   (For production, use `login` or leave it blank)

### Step 3: Test the connection

Run the campaign creation script:
```bash
python -m src.run_campaign config/campaigns/gtc-nvidia-afterparty.yaml
```

If authentication succeeds, you'll see the campaigns being created!

---

## Testing Your Connection

After setting up your `.env` file, test the connection:

```bash
python -m src.run_campaign config/campaigns/gtc-nvidia-afterparty.yaml
```

If you see authentication errors, check:
1. Your username/password are correct
2. Your security token is correct (if using Option 1)
3. Your IP address is whitelisted (if your org requires it)
4. Your user has API access enabled (System Administrator profile usually has this)

---

## Troubleshooting

### "INVALID_CLIENT: Invalid client credentials"
- Double-check your Consumer Key and Consumer Secret
- Make sure there are no extra spaces when copying
- Wait 2-10 minutes after creating the Connected App (it needs to activate)

### "INVALID_LOGIN: Invalid username, password"
- Double-check your username and password
- If your org uses SSO, you may need to use your actual Salesforce username (not email)
- Check if your org requires IP whitelisting (see below)

### "INSUFFICIENT_ACCESS: Insufficient access rights"
- Your user needs API access enabled
- Check your profile/permission set has "API Enabled" permission
- You need read/write access to Campaign object
- Go to Setup → Users → Your User → Profile → Check "API Enabled"

### "IP_RESTRICTION: IP restriction"
- Your Connected App may have IP restrictions
- Go to Setup → App Manager → Find your Connected App → Edit Policies
- Under "IP Relaxation", set to "Relax IP restrictions" (or add your IP to allowed list)
- Under "Permitted Users", set to "All users may self-authorize" (or manage user access)

### "Error: invalid_grant"
- Your Connected App might not be activated yet (wait a few minutes)
- Check that OAuth scopes include "Access and manage your data (api)"
- Verify "Require Secret for Web Server Flow" is checked

### "Error: invalid_client_id"
- Consumer Key is incorrect
- Make sure you copied the full Consumer Key (they're usually long strings)
- Check for any extra spaces or characters
