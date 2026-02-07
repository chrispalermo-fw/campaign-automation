# HubSpot Form Field Setup - Detailed Instructions

## Important: Use Custom Fields (Not Connected Properties)

**You do NOT need to connect these to HubSpot contact properties.** These are custom form fields that will be sent directly to your webhook.

## How to Add Fields in HubSpot Form Builder

When you click "Add field" in the HubSpot form builder:

### For Each Field:

1. **Select field type** (text, date, textarea, etc.)
2. **Field name**: Enter the exact name (e.g., `campaign_name`)
   - This is the "Internal name" or "Field name" field
   - NOT the label that users see
   - Use underscores, no spaces
3. **Label**: Enter the user-friendly label (e.g., "Campaign Name")
4. **Required**: Check if it's required
5. **DO NOT** connect to a HubSpot property (leave "Connect to property" empty/unselected)

## Field-by-Field Setup

### 1. Campaign Name

- **Field type**: Single-line text
- **Field name**: `campaign_name` ← **This is what matters!**
- **Label**: "Campaign Name"
- **Required**: ✅ Yes
- **Placeholder**: "e.g., 1PEvent_GTC Nvidia Afterparty_San Jose_03162026"
- **Help text**: "Format: Type_name_Location_Date"
- **Connect to property**: ❌ Leave empty (custom field)

### 2. Start Date

- **Field type**: Date picker
- **Field name**: `start_date` ← **This is what matters!**
- **Label**: "Start Date"
- **Required**: ✅ Yes
- **Connect to property**: ❌ Leave empty (custom field)

### 3. End Date

- **Field type**: Date picker
- **Field name**: `end_date` ← **This is what matters!**
- **Label**: "End Date"
- **Required**: ✅ Yes
- **Connect to property**: ❌ Leave empty (custom field)

### 4. Member Statuses

- **Field type**: Multi-line text (textarea)
- **Field name**: `member_statuses` ← **This is what matters!**
- **Label**: "Member Statuses"
- **Required**: ✅ Yes
- **Placeholder**: "Registered\nWaitlist\nAttended\nNo Show"
- **Help text**: "Enter one status per line"
- **Connect to property**: ❌ Leave empty (custom field)

## Visual Guide

In HubSpot form builder, when you add a field, you'll see:

```
┌─────────────────────────────────────┐
│ Field Type: [Single-line text ▼]   │
│                                      │
│ Field name: [campaign_name]         │ ← Enter exact name here
│                                      │
│ Label: [Campaign Name]              │ ← User-friendly label
│                                      │
│ Connect to property: [None ▼]      │ ← Leave as "None"
│                                      │
│ Required: ☑                         │
└─────────────────────────────────────┘
```

## Why Custom Fields?

These fields are **not** stored as contact properties in HubSpot. They're:
- Only used to collect data from the form
- Sent directly to your webhook
- Used to create campaigns (not stored on contacts)

## Testing

After creating the form:
1. **Preview the form** to make sure fields appear correctly
2. **Submit a test entry** 
3. **Check the workflow** (if set up) to see if data is received
4. **Verify field names** match exactly what's in your webhook mapping

## Common Mistakes

❌ **Wrong**: Connecting fields to HubSpot properties (like "First Name", "Email")
✅ **Right**: Using custom field names that match your webhook

❌ **Wrong**: Field name with spaces: `campaign name`
✅ **Right**: Field name with underscores: `campaign_name`

❌ **Wrong**: Different field names than what webhook expects
✅ **Right**: Exact match: `campaign_name`, `start_date`, `end_date`, `member_statuses`

## Quick Checklist

- [ ] Field name: `campaign_name` (not connected to property)
- [ ] Field name: `start_date` (not connected to property)
- [ ] Field name: `end_date` (not connected to property)
- [ ] Field name: `member_statuses` (not connected to property)
- [ ] All field names use underscores (no spaces)
- [ ] Required fields are marked as required
- [ ] Form is saved

## Next Steps

After creating the form:
1. Create the landing page and add this form
2. Set up the workflow to send form data to your webhook
3. Test by submitting the form

See `CREATE_LANDING_PAGE_MANUAL.md` for complete setup instructions.
