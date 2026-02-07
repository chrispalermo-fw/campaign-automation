# Create Custom HubSpot Properties for Form Fields

HubSpot requires form fields to be connected to contact properties. Here's how to create the custom properties you need.

## Step 1: Create Custom Contact Properties

Go to **HubSpot** → **Settings** → **Properties** → **Contact properties** → **Create property**

Create these properties one by one:

### 1. Campaign Name

- **Label**: `Campaign Name`
- **Internal name**: `campaign_name` (auto-generated, but verify it matches)
- **Field type**: Single-line text
- **Group**: Contact information (or create new group "Campaign Automation")
- **Description**: "Campaign name for automation form"
- **Options**: 
  - ✅ Show on contact record: No (optional - we won't use this on contacts)
  - ✅ Searchable: No (optional)

### 2. Start Date

- **Label**: `Campaign Start Date`
- **Internal name**: `campaign_start_date` (or `start_date` if allowed)
- **Field type**: Date picker
- **Group**: Contact information (or "Campaign Automation")
- **Description**: "Campaign start date from automation form"

### 3. End Date

- **Label**: `Campaign End Date`
- **Internal name**: `campaign_end_date` (or `end_date` if allowed)
- **Field type**: Date picker
- **Group**: Contact information (or "Campaign Automation")
- **Description**: "Campaign end date from automation form"

### 4. Member Statuses

- **Label**: `Campaign Member Statuses`
- **Internal name**: `member_statuses`
- **Field type**: Multi-line text
- **Group**: Contact information (or "Campaign Automation")
- **Description**: "Member statuses for campaign automation"

### Optional Properties:

### 5. Salesforce Status

- **Label**: `Salesforce Campaign Status`
- **Internal name**: `salesforce_status`
- **Field type**: Single-line text
- **Group**: Contact information (or "Campaign Automation")

### 6. Salesforce Description

- **Label**: `Salesforce Campaign Description`
- **Internal name**: `salesforce_description`
- **Field type**: Multi-line text
- **Group**: Contact information (or "Campaign Automation")

### 7. Salesforce Type

- **Label**: `Salesforce Campaign Type`
- **Internal name**: `salesforce_type`
- **Field type**: Single-line text
- **Group**: Contact information (or "Campaign Automation")

### 8. Parent Campaign

- **Label**: `Parent Campaign Name`
- **Internal name**: `parent_campaign`
- **Field type**: Single-line text
- **Group**: Contact information (or "Campaign Automation")

### 9. HubSpot Notes

- **Label**: `Campaign HubSpot Notes`
- **Internal name**: `hubspot_notes`
- **Field type**: Multi-line text
- **Group**: Contact information (or "Campaign Automation")

### 10. Wait Minutes

- **Label**: `Campaign Wait Minutes`
- **Internal name**: `wait_minutes`
- **Field type**: Number
- **Group**: Contact information (or "Campaign Automation")

### 11. Webhook URL

- **Label**: `Campaign Webhook URL`
- **Internal name**: `webhook_url`
- **Field type**: Single-line text
- **Group**: Contact information (or "Campaign Automation")

## Step 2: Connect Form Fields to Properties

After creating the properties:

1. **Go back to your form** (Marketing → Forms → Campaign Automation Form)
2. **For each field**, click on it to edit
3. **Connect to property**: Select the corresponding property you just created
   - Campaign Name → `campaign_name`
   - Start Date → `campaign_start_date` (or `start_date`)
   - End Date → `campaign_end_date` (or `end_date`)
   - Member Statuses → `member_statuses`
   - etc.
4. **Save the form**

## Important Notes

- **These properties will store data on contacts** when the form is submitted
- **This is okay** - the data will be there for the webhook to read
- **You can hide these properties** from the contact record view if you don't want to see them
- **The webhook will still receive the form data** via the workflow

## Alternative: Use Hidden Fields

If you don't want to store this data on contacts, you can:
1. Create the properties (required for form to save)
2. Set them as "Hidden" in the form
3. The webhook will still receive the data, but it won't be visible on contact records

## Quick Property Creation Script

If you have many properties to create, you can use the HubSpot API to create them programmatically. Would you like me to create a script for that?

## Troubleshooting

### "Property name already exists"
- Check if the property already exists
- Use a slightly different name if needed
- The internal name must be unique

### "Can't find property in dropdown"
- Make sure you created it as a **Contact** property (not Company, Deal, etc.)
- Refresh the form builder page
- Check the property group you created it in

### Form still won't save
- Make sure ALL required fields are connected to properties
- Check that property internal names match what you're trying to use
- Try saving with just the 4 required fields first, then add optional ones
