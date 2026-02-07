# Step-by-Step: Create Salesforce Connected App

Follow these steps exactly to create your Connected App.

## Step 1: Log into Salesforce

1. Go to your Salesforce org (production or sandbox)
2. Log in with your work email/username

## Step 2: Navigate to App Manager

1. Click the **gear icon (⚙️)** in the top right corner
2. Click **Setup**
3. In the **Quick Find** box (left sidebar, near the top), type: `App Manager`
4. Click **App Manager** from the results

## Step 3: Create New Connected App

1. Click the **New Connected App** button (top right, next to "View" dropdown)

## Step 4: Fill in Basic Information

Fill in these fields:

- **Connected App Name**: `Campaign Automation Tool`
  - (This is just a label - you'll see it in your app list)
  
- **API Name**: `Campaign_Automation_Tool`
  - (This auto-fills when you tab out of the name field)
  - This is the internal name Salesforce uses

- **Contact Email**: `your-email@company.com`
  - (Your work email)

- **Description** (optional): `API access for campaign automation tool`

## Step 5: Enable OAuth Settings

1. Scroll down to the **API (Enable OAuth Settings)** section
2. Check the box: **Enable OAuth Settings**

## Step 6: Configure OAuth Settings

Once you check "Enable OAuth Settings", more fields will appear:

### Callback URL
- **Callback URL**: `http://localhost:8080/oauth/callback`
  - (This is required but won't actually be used for our username-password flow)
  - You can also use: `https://localhost:8080/oauth/callback`

### Selected OAuth Scopes
Move these scopes from **Available OAuth Scopes** (left) to **Selected OAuth Scopes** (right):

1. **Access and manage your data (api)**
   - This gives API access to read/write data
   - **Required!**

2. **Perform requests on your behalf at any time (refresh_token, offline_access)**
   - This allows the app to work without user interaction
   - **Required!**

### Require Secret for Web Server Flow
- Check the box: **Require Secret for Web Server Flow**
  - This ensures you get a Consumer Secret (which we need)

## Step 7: Set Permitted Users (Important!)

Scroll down to find **Permitted Users** section:

- Select: **All users may self-authorize**
  - OR if you want to restrict it: **Admin approved users are pre-authorized**
  - For testing, "All users may self-authorize" is easiest

## Step 8: Set IP Relaxation (Important!)

Find **IP Relaxation**:

- Select: **Relax IP restrictions**
  - This allows the app to work from any IP address
  - If your org has strict IP policies, you may need to add your IP to an allowed list instead

## Step 9: Save

1. Scroll to the bottom
2. Click **Save**
3. **Wait 2-10 minutes** for Salesforce to activate the Connected App
   - You'll see a message saying it may take a few minutes

## Step 10: Get Your Credentials

After saving, you'll be on the Connected App detail page:

1. **Consumer Key** (also called Client ID)
   - This is visible on the page
   - It's a long string like: `3MVG9fMtCkV6eLheIEZplMqWfnGlf3Y.BcWdOf1qytXo9zxgbsrUbS.xxx`
   - **Copy this entire string**

2. **Consumer Secret** (also called Client Secret)
   - Click the link that says **Click to reveal**
   - Copy the entire string
   - **Important:** This is only shown once! Save it immediately.

## Step 11: Save Your Credentials

Save both values somewhere safe (you'll need them for your `.env` file):
- Consumer Key: `_____________________________`
- Consumer Secret: `_____________________________`

---

## What to Tell Me

After you complete these steps, let me know:

1. ✅ "I've created the Connected App"
2. Your **Consumer Key** (I'll help you verify it's correct)
3. Whether you're using **Production** or **Sandbox**
4. Your Salesforce **username/email**

Then I'll help you set up the `.env` file and test it!
