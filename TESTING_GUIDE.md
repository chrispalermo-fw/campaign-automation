# Testing the Campaign Automation Web App

## Quick Start

### Option 1: Using the Startup Script (Easiest)

```bash
./start_web_app.sh
```

### Option 2: Manual Start

```bash
# Activate virtual environment
source .venv/bin/activate

# Start the app
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

## Step-by-Step Testing

### 1. Start the Web App

Run one of the commands above. The app will start on `http://localhost:5000`

### 2. Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

You should see a form with a purple gradient header saying "Campaign Automation Tool"

### 3. Fill Out the Form

#### Required Fields:

**Campaign Name:**
```
1PEvent_Test Campaign_San Francisco_02072026
```

**Start Date:**
- Click the date picker and select a future date
- Example: `2026-02-07`

**End Date:**
- Click the date picker and select the same or later date
- Example: `2026-02-07`

**Member Statuses:**
Enter one per line:
```
Registered
Waitlist
Attended
No Show
```

#### Optional Fields (you can leave these blank for testing):

- **HubSpot Notes**: "Test campaign created via web app"
- **Salesforce Status**: Leave as "Planned" (default)
- **Salesforce Description**: "Test campaign"
- **Salesforce Type**: "Event"
- **Parent Campaign**: Leave blank
- **Wait Time**: Leave as 10 (default)
- **Webhook URL**: Leave blank

### 4. Submit the Form

Click the **"🚀 Create Campaign"** button at the bottom.

### 5. What Happens Next

The app will:
1. Validate your inputs
2. Create the campaign in HubSpot
3. Create the campaign in Salesforce
4. Create segments/lists in HubSpot
5. Create campaign member statuses in Salesforce
6. Create workflows in HubSpot
7. Show you a results page

### 6. Check the Results Page

You should see:
- ✅ Success message
- HubSpot Campaign ID
- Salesforce Campaign ID
- List of created lists
- List of created workflows
- Next steps instructions

## Troubleshooting

### "Connection refused" or can't connect

**Problem:** The app isn't running or wrong port

**Solution:**
1. Make sure you started the app (`python app.py`)
2. Check the terminal for the URL (should be `http://localhost:5000`)
3. Try `http://127.0.0.1:5000` instead

### "Missing environment variables" error

**Problem:** `.env` file not configured

**Solution:**
1. Make sure `.env` file exists in the project root
2. Check that it contains:
   - `HUBSPOT_ACCESS_TOKEN`
   - `SALESFORCE_USERNAME`
   - `SALESFORCE_PASSWORD`
   - `SALESFORCE_SECURITY_TOKEN`

### "ModuleNotFoundError: No module named 'flask'"

**Problem:** Flask not installed

**Solution:**
```bash
source .venv/bin/activate
pip install Flask
```

### Campaign creation fails

**Problem:** API credentials or permissions issue

**Solution:**
1. Check your `.env` file has correct credentials
2. Verify HubSpot Private App has Automation scope
3. Check Salesforce credentials are correct
4. Look at the error message in the browser for details

### Form validation errors

**Problem:** Missing required fields

**Solution:**
- Make sure Campaign Name, Start Date, End Date, and Member Statuses are filled
- Member Statuses should be one per line

## Testing Checklist

- [ ] App starts without errors
- [ ] Form page loads correctly
- [ ] Can fill out all form fields
- [ ] Form validation works (try submitting empty form)
- [ ] Campaign creation succeeds
- [ ] Results page shows campaign IDs
- [ ] Results page shows workflow information
- [ ] Can create multiple campaigns

## Example Test Data

Here's a complete example you can copy-paste:

**Campaign Name:**
```
1PEvent_Test Campaign_San Francisco_02072026
```

**Start Date:** `2026-02-07`

**End Date:** `2026-02-07`

**Member Statuses:**
```
Registered
Waitlist
Attended
No Show
```

**HubSpot Notes:** `Test campaign created via web app`

**Salesforce Description:** `Test campaign for web app`

**Salesforce Type:** `Event`

## Advanced Testing

### Test Error Handling

1. **Submit empty form** - Should show validation errors
2. **Submit with invalid dates** - Should show date errors
3. **Submit without member statuses** - Should show error

### Test with Different Configurations

1. **With parent campaign** - Add a parent campaign name
2. **With webhook** - Add a Zapier webhook URL
3. **Different wait times** - Try 5, 15, 30 minutes
4. **Different member statuses** - Try custom statuses

### Check Created Resources

After creating a campaign:

1. **HubSpot:**
   - Go to Marketing → Campaigns
   - Find your campaign
   - Check lists/segments were created
   - Check workflows were created

2. **Salesforce:**
   - Go to Campaigns tab
   - Find your campaign
   - Check campaign member statuses were created

## Stopping the App

Press `Ctrl+C` in the terminal where the app is running.

## Next Steps After Testing

Once testing is successful:

1. Configure workflow enrollment triggers (see `CONFIGURE_WORKFLOWS.md`)
2. Add "Set Salesforce Campaign" actions to workflows
3. Activate workflows
4. Test with a real contact by adding them to a list
