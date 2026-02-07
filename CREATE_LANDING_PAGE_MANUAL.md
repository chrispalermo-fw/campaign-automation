# Create HubSpot Landing Page - Manual Setup Guide

Since the HubSpot Forms API has limitations with custom fields, here's a step-by-step guide to create the landing page manually in HubSpot UI. This is actually faster and more reliable!

## Step 1: Create the Form in HubSpot UI

1. **Go to HubSpot** → **Marketing** → **Forms** → **Create form**

2. **Form Settings:**
   - **Form name**: `Campaign Automation Form`
   - **Form type**: Standard form

3. **Add Form Fields** (click "Add field" for each):

   ### Required Fields:

   **Campaign Name** (Single-line text)
   - Field name: `campaign_name` (use "Custom field" option)
   - Label: "Campaign Name"
   - Required: ✅ Yes
   - Placeholder: "e.g., 1PEvent_GTC Nvidia Afterparty_San Jose_03162026"
   - Help text: "Format: Type_name_Location_Date"

   **Start Date** (Date picker)
   - Field name: `start_date`
   - Label: "Start Date"
   - Required: ✅ Yes

   **End Date** (Date picker)
   - Field name: `end_date`
   - Label: "End Date"
   - Required: ✅ Yes

   **Member Statuses** (Multi-line text)
   - Field name: `member_statuses`
   - Label: "Member Statuses"
   - Required: ✅ Yes
   - Placeholder: "Registered\nWaitlist\nAttended\nNo Show"
   - Help text: "Enter one status per line"

   ### Optional Fields:

   **Salesforce Campaign Status** (Single-line text)
   - Field name: `salesforce_status`
   - Label: "Salesforce Campaign Status"
   - Required: No
   - Placeholder: "Planned (default), In Progress, Completed, Cancelled"
   - Default value: "Planned"

   **Campaign Description** (Multi-line text)
   - Field name: `salesforce_description`
   - Label: "Campaign Description"
   - Required: No

   **Campaign Type** (Single-line text)
   - Field name: `salesforce_type`
   - Label: "Campaign Type"
   - Required: No
   - Placeholder: "e.g., Event, Webinar, Email"

   **Parent Campaign** (Single-line text)
   - Field name: `parent_campaign`
   - Label: "Parent Campaign Name (Optional)"
   - Required: No

   **HubSpot Notes** (Multi-line text)
   - Field name: `hubspot_notes`
   - Label: "HubSpot Campaign Notes"
   - Required: No

   **Wait Minutes** (Number)
   - Field name: `wait_minutes`
   - Label: "Wait Time Before Sync (minutes)"
   - Required: No
   - Default value: 10

   **Webhook URL** (Single-line text)
   - Field name: `webhook_url`
   - Label: "Custom Webhook URL (Optional)"
   - Required: No

4. **Form Options:**
   - Submit button text: "Create Campaign"
   - Thank you message: "Campaign creation in progress..."

5. **Save the form**

## Step 2: Create the Landing Page

1. **Go to HubSpot** → **Marketing** → **Landing Pages** → **Create landing page**

2. **Choose a template** or start from scratch

3. **Page Settings:**
   - **Page name**: `Campaign Automation Tool`
   - **URL slug**: `campaign-automation`
   - **Page title**: "Campaign Automation Tool - Create Campaigns in HubSpot & Salesforce"

4. **Add Content:**
   - Add a heading: "🚀 Campaign Automation Tool"
   - Add description:
     ```
     Create campaigns in HubSpot and Salesforce with automated workflows and segments.
     
     Fill out the form below to automatically create:
     • Campaign in HubSpot
     • Campaign in Salesforce
     • Segments/Lists for each member status
     • Campaign member statuses in Salesforce
     • Workflows to sync list enrollments to Salesforce
     ```

5. **Add the Form:**
   - Drag the "Form" module onto the page
   - Select "Campaign Automation Form" (the form you just created)

6. **Customize styling** to match your brand

7. **Save and publish** the page

## Step 3: Create the Workflow

1. **Go to HubSpot** → **Automation** → **Workflows** → **Create workflow**

2. **Set Enrollment Trigger:**
   - Trigger: **"Contact submits form"**
   - Select: **"Campaign Automation Form"**

3. **Add Action: Send webhook**

   **Webhook Configuration:**
   - **Webhook URL**: Your webhook server URL
     - Local testing: `http://your-ngrok-url.ngrok.io/webhook/campaign-create`
     - Production: `https://your-domain.com/webhook/campaign-create`
   
   - **HTTP Method**: POST
   
   - **Request Body Type**: JSON
   
   - **Request Body**: Map form fields:
   ```json
   {
     "campaign_name": "{{ form.campaign_name }}",
     "start_date": "{{ form.start_date }}",
     "end_date": "{{ form.end_date }}",
     "member_statuses": "{{ form.member_statuses }}",
     "salesforce_status": "{{ form.salesforce_status }}",
     "salesforce_description": "{{ form.salesforce_description }}",
     "salesforce_type": "{{ form.salesforce_type }}",
     "parent_campaign": "{{ form.parent_campaign }}",
     "hubspot_notes": "{{ form.hubspot_notes }}",
     "wait_minutes": "{{ form.wait_minutes }}",
     "webhook_url": "{{ form.webhook_url }}"
   }
   ```

4. **Add Action: Send email notification** (Optional)
   - Send yourself an email with campaign creation results
   - Include webhook response data

5. **Activate the workflow**

## Step 4: Test

1. **Go to your landing page**
2. **Fill out and submit the form**
3. **Check the workflow activity** to see if webhook was triggered
4. **Verify campaigns** were created in HubSpot and Salesforce

## Quick Reference: Form Field Names

Make sure these field names match exactly in your HubSpot form:

- `campaign_name` (required)
- `start_date` (required)
- `end_date` (required)
- `member_statuses` (required)
- `salesforce_status` (optional)
- `salesforce_description` (optional)
- `salesforce_type` (optional)
- `parent_campaign` (optional)
- `hubspot_notes` (optional)
- `wait_minutes` (optional)
- `webhook_url` (optional)

## Troubleshooting

### Form fields not showing in workflow
- Make sure field names use underscores (not spaces or hyphens)
- Check that fields are saved in the form

### Webhook not receiving data
- Verify webhook URL is correct
- Check workflow is activated
- Test webhook URL directly with curl

### Campaign creation fails
- Check webhook server logs
- Verify environment variables are set
- Check API credentials

---

**Note**: Creating the form manually in HubSpot UI is actually faster and more reliable than using the API, since you can see exactly what you're creating and test it immediately!
