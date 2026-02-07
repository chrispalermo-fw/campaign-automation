# Add Forms & CMS Scopes to HubSpot Private App

To create the landing page and form programmatically, you need to add these scopes to your HubSpot Private App.

## Quick Steps

1. **Go to HubSpot Settings**
   - Click the **gear icon (⚙️)** in the top right
   - Go to **Integrations** → **Private Apps**

2. **Edit Your Private App**
   - Find **"Campaign Automation Tool"** (or whatever you named it)
   - Click on it to edit

3. **Add Missing Scopes**

   Go to the **Scopes** tab and add:

   ### Marketing Scopes:
   - ✅ **Marketing forms** → **Read**
   - ✅ **Marketing forms** → **Write**

   ### CMS Scopes:
   - ✅ **CMS pages** → **Read**
   - ✅ **CMS pages** → **Write**

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

## Run the Script Again

After adding the scopes:

```bash
python create_hubspot_landing_page.py
```

This will create:
- ✅ The form with all required fields
- ✅ The landing page with the form embedded

## What Gets Created

### Form Fields Created:
- Campaign Name (required)
- Start Date (required)
- End Date (required)
- Member Statuses (required)
- Salesforce Status (optional)
- Salesforce Description (optional)
- Salesforce Type (optional)
- Parent Campaign (optional)
- HubSpot Notes (optional)
- Wait Minutes (optional)
- Webhook URL (optional)

### Landing Page:
- Title: "Campaign Automation Tool"
- Description explaining what it does
- Form embedded on the page
- Ready to publish

## After Running the Script

1. **Go to HubSpot** → **Marketing** → **Landing Pages**
2. **Find** "Campaign Automation Tool"
3. **Click to edit** and customize if needed
4. **Publish** when ready

Then set up the workflow to connect the form to your webhook server (see `HUBSPOT_LANDING_PAGE_SETUP.md`).
