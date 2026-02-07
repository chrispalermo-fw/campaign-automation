# Create Properties - Step-by-Step Visual Guide

Since the Properties scope isn't available, let's create them manually. This takes about 3 minutes!

## Quick Method: Create All 4 Required Properties

### Property 1: Campaign Name

1. **HubSpot** → **Settings** (gear icon) → **Properties** → **Contact properties**
2. Click **"Create property"** (top right)
3. Fill in:
   - **Label**: `Campaign Name`
   - **Internal name**: Type `campaign_name` (or verify it auto-fills correctly)
   - **Field type**: Select **"Single-line text"**
   - **Group**: Select **"Contact information"** (or leave default)
   - **Description** (optional): "Campaign name from automation form"
4. Click **"Create"**

### Property 2: Campaign Start Date

1. Click **"Create property"** again
2. Fill in:
   - **Label**: `Campaign Start Date`
   - **Internal name**: Type `start_date` (or verify auto-fill)
   - **Field type**: Select **"Date picker"**
   - **Group**: **"Contact information"**
3. Click **"Create"**

### Property 3: Campaign End Date

1. Click **"Create property"** again
2. Fill in:
   - **Label**: `Campaign End Date`
   - **Internal name**: Type `end_date` (or verify auto-fill)
   - **Field type**: Select **"Date picker"**
   - **Group**: **"Contact information"**
3. Click **"Create"**

### Property 4: Campaign Member Statuses

1. Click **"Create property"** again
2. Fill in:
   - **Label**: `Campaign Member Statuses`
   - **Internal name**: Type `member_statuses` (or verify auto-fill)
   - **Field type**: Select **"Multi-line text"**
   - **Group**: **"Contact information"**
3. Click **"Create"**

## Connect Form Fields to Properties

Now go back to your form:

1. **HubSpot** → **Marketing** → **Forms** → **Campaign Automation Form**
2. **Click on "Campaign Name" field** → Click **"Connect to property"**
   - Select: **"Campaign Name"** (the property you just created)
3. **Click on "Start Date" field** → **"Connect to property"**
   - Select: **"Campaign Start Date"**
4. **Click on "End Date" field** → **"Connect to property"**
   - Select: **"Campaign End Date"**
5. **Click on "Member Statuses" field** → **"Connect to property"**
   - Select: **"Campaign Member Statuses"**
6. **Click "Save"** on the form

## Done! ✅

Your form should now save successfully!

## Optional: Create Additional Properties

If you want to add the optional fields later, create these properties the same way:

- `salesforce_status` - Single-line text
- `salesforce_description` - Multi-line text
- `salesforce_type` - Single-line text
- `parent_campaign` - Single-line text
- `hubspot_notes` - Multi-line text
- `wait_minutes` - Number
- `webhook_url` - Single-line text

## Tips

- **Internal name** is what matters - make sure it matches (or close to):
  - `campaign_name`
  - `start_date`
  - `end_date`
  - `member_statuses`

- If HubSpot auto-generates a different internal name (like `campaign_start_date`), that's okay! Just use that name when connecting the form field.

- You can create all 4 properties in about 2-3 minutes by repeating the same steps.
