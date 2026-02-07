# Quick Guide: Create Properties in HubSpot UI

## Fastest Method - Create Properties Manually

Since HubSpot requires form fields to be connected to properties, create these custom contact properties:

## Step-by-Step

### 1. Go to Properties

**HubSpot** → **Settings** → **Properties** → **Contact properties** → **Create property**

### 2. Create These 4 Required Properties

#### Property 1: Campaign Name
- **Label**: `Campaign Name`
- **Internal name**: Will auto-generate as `campaign_name` (verify this!)
- **Field type**: Single-line text
- **Group**: Contact information
- Click **Create**

#### Property 2: Campaign Start Date
- **Label**: `Campaign Start Date`
- **Internal name**: Should be `campaign_start_date` or `start_date`
- **Field type**: Date picker
- **Group**: Contact information
- Click **Create**

#### Property 3: Campaign End Date
- **Label**: `Campaign End Date`
- **Internal name**: Should be `campaign_end_date` or `end_date`
- **Field type**: Date picker
- **Group**: Contact information
- Click **Create**

#### Property 4: Campaign Member Statuses
- **Label**: `Campaign Member Statuses`
- **Internal name**: Should be `campaign_member_statuses` or `member_statuses`
- **Field type**: Multi-line text
- **Group**: Contact information
- Click **Create**

### 3. Connect Form Fields to Properties

1. **Go back to your form**: Marketing → Forms → Campaign Automation Form
2. **Click on each field** to edit it
3. **"Connect to property"** dropdown → Select the property you just created
   - Campaign Name field → Connect to `campaign_name` property
   - Start Date field → Connect to `start_date` (or `campaign_start_date`) property
   - End Date field → Connect to `end_date` (or `campaign_end_date`) property
   - Member Statuses field → Connect to `member_statuses` property
4. **Save the form**

## Important: Check Internal Names

When creating properties, HubSpot auto-generates an internal name. Make sure it matches:

- ✅ `campaign_name` (or close)
- ✅ `start_date` or `campaign_start_date`
- ✅ `end_date` or `campaign_end_date`
- ✅ `member_statuses` or `campaign_member_statuses`

**If the internal name is different**, you have two options:
1. Use whatever internal name HubSpot created (and update your webhook to match)
2. Or manually type the exact name you want in the "Internal name" field (if HubSpot allows editing it)

## Quick Tip

You can create all 4 properties in about 2 minutes:
1. Create property → Fill form → Create
2. Repeat 3 more times
3. Go back to form → Connect fields → Save

## After Properties Are Created

Once you connect the form fields to properties, the form will save successfully!

Then you can:
1. Create the landing page
2. Add the form to the landing page
3. Set up the workflow
