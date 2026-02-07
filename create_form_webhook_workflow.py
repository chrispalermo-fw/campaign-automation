#!/usr/bin/env python3
"""
Create HubSpot workflow that triggers on form submission and sends webhook.
"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

HUBSPOT_BASE = "https://api.hubapi.com"
WEBHOOK_URL = "https://nonobligatory-defamatorily-lonnie.ngrok-free.dev/webhook/campaign-create"
FORM_ID = "87a36d71-6aac-47e5-8231-46cb27a417f2"  # Campaign Automation Form


def get_headers():
    """Get API headers with authentication."""
    token = os.environ.get("HUBSPOT_ACCESS_TOKEN")
    if not token:
        raise ValueError("HUBSPOT_ACCESS_TOKEN not found in environment")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def create_form_webhook_workflow():
    """Create workflow that triggers on form submission and sends webhook."""
    print("🔧 Creating HubSpot workflow for form submission...")
    
    url = f"{HUBSPOT_BASE}/automation/v3/workflows"
    
    # Create workflow with webhook action
    workflow_data = {
        "name": "Campaign Creation Webhook",
        "type": "DRIP_DELAY",
        "onlyEnrollsManually": False,  # Allow automatic enrollment
        "actions": [
            {
                "type": "WEBHOOK",
                "url": WEBHOOK_URL,
                "method": "POST",
                "body": {
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
                    "webhook_url": "{{ form.webhook_url }}",
                }
            }
        ]
    }
    
    headers = get_headers()
    response = requests.post(url, json=workflow_data, headers=headers)
    
    if response.status_code in [200, 201]:
        workflow = response.json()
        workflow_id = workflow.get("id")
        print(f"✅ Workflow created successfully! Workflow ID: {workflow_id}")
        print()
        print("⚠️  IMPORTANT: Set enrollment trigger manually:")
        print("   1. Go to HubSpot → Automation → Workflows")
        print(f"   2. Open 'Campaign Creation Webhook' (ID: {workflow_id})")
        print("   3. Click 'Enrollment' tab")
        print("   4. Add trigger: 'Contact submits form'")
        print(f"   5. Select form: 'Campaign Automation Form' (ID: {FORM_ID})")
        print("   6. Activate the workflow")
        print()
        return workflow_id
    else:
        print(f"❌ Error creating workflow: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        raise Exception(f"Failed to create workflow: {response.text}")


def main():
    """Main function."""
    print("=" * 60)
    print("Creating Form Submission Webhook Workflow")
    print("=" * 60)
    print()
    print(f"Webhook URL: {WEBHOOK_URL}")
    print(f"Form ID: {FORM_ID}")
    print()
    
    try:
        workflow_id = create_form_webhook_workflow()
        print()
        print("=" * 60)
        print("✅ Workflow Created!")
        print("=" * 60)
        print()
        print("Next: Set enrollment trigger in HubSpot UI (see instructions above)")
        print("Then: Test by submitting the form on your landing page!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
