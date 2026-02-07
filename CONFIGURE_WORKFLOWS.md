# Configure HubSpot Workflows - Set Salesforce Campaign Action

The workflows have been created automatically, but you **MUST** configure the "Set Salesforce Campaign" action in HubSpot UI for each workflow. This action updates the Salesforce CampaignMember status.

## Quick Reference

| Workflow Name | Workflow ID | List ID | Status | Salesforce Campaign ID |
|--------------|-------------|---------|--------|----------------------|
| Waitlist | 27947696 | 828 | Waitlist | 701PY00001Pf7k7YAB |
| Attended | (check output) | 829 | Attended | 701PY00001Pf7k7YAB |
| No Show | (check output) | 830 | No Show | 701PY00001Pf7k7YAB |
| Registered | (create manually) | (find ID) | Registered | 701PY00001Pf7k7YAB |

## Step-by-Step Instructions

### For Each Workflow:

1. **Go to HubSpot Workflows**
   - Navigate to: **Automation** → **Workflows**
   - Find your workflow (e.g., `1PEvent_ GTC Nvidia Afterparty_San Jose_03162026 - Waitlist`)

2. **Configure Enrollment Trigger**
   - Click the **"Enrollment"** tab
   - Click **"Add enrollment trigger"**
   - Select: **"Contact is added to list"**
   - Choose the appropriate list:
     - Waitlist → List ID: **828**
     - Attended → List ID: **829**
     - No Show → List ID: **830**
     - Registered → (find the list ID)

3. **Configure Actions (CRITICAL STEP)**
   - Click the **"Actions"** tab
   - You should see:
     - ✅ **Delay** action (10 minutes) - Keep this!
     - ❌ **Set contact property** action - **DELETE THIS** (it's a placeholder)
   
   - Click **"Add action"**
   - Search for: **"Set Salesforce Campaign"**
   - Select: **"Set Salesforce Campaign"**
   - Configure:
     - **Campaign**: `701PY00001Pf7k7YAB` (your Salesforce Campaign ID)
     - **Status**: Select the correct status:
       - Waitlist workflow → **Waitlist**
       - Attended workflow → **Attended**
       - No Show workflow → **No Show**
       - Registered workflow → **Registered**

4. **Verify Action Order**
   - The actions should be in this order:
     1. **Delay** (10 minutes)
     2. **Set Salesforce Campaign** (with correct status)

5. **Activate the Workflow**
   - Click **"Activate"** in the top right
   - Confirm activation

## Testing

After configuring all workflows:

1. **Test with a contact**:
   - Add a test contact to one of the lists (e.g., Waitlist)
   - Wait 10+ minutes
   - Check Salesforce → Campaigns → Your Campaign → Campaign Members
   - Verify the contact appears with the correct status

2. **Monitor workflow runs**:
   - In HubSpot, go to the workflow
   - Check the "Activity" tab to see enrolled contacts
   - Verify contacts are flowing through

## Troubleshooting

### "Set Salesforce Campaign" action not available?
- Make sure HubSpot-Salesforce integration is connected
- Go to: **Settings** → **Integrations** → **Salesforce**
- Verify the connection is active

### Wrong status being set?
- Double-check the status name matches exactly (case-sensitive)
- Verify the Salesforce Campaign Member Status exists in Salesforce
- Check: Salesforce → Campaigns → Your Campaign → Campaign Member Statuses

### Workflow not triggering?
- Verify the enrollment trigger is set correctly
- Check that contacts are actually being added to the list
- Ensure the workflow is activated (not draft)

## Next Steps

Once all workflows are configured:
1. ✅ All 4 workflows created and activated
2. ✅ Enrollment triggers set (Contact added to list)
3. ✅ "Set Salesforce Campaign" action configured with correct status
4. ✅ Test with a sample contact
5. ✅ Monitor for a few days to ensure sync is working

---

**Note**: The "Set Salesforce Campaign" action cannot be automated via API, which is why manual configuration is required. Once configured, the workflows will run automatically whenever contacts are added to the respective lists.
