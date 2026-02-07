#!/usr/bin/env python3
"""
Create HubSpot landing page and form for campaign automation.
This script creates the form and landing page programmatically via HubSpot API.
"""
import os
import json
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

HUBSPOT_BASE = "https://api.hubapi.com"


def get_headers():
    """Get API headers with authentication."""
    token = os.environ.get("HUBSPOT_ACCESS_TOKEN")
    if not token:
        raise ValueError("HUBSPOT_ACCESS_TOKEN not found in environment")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def create_form():
    """Create the campaign automation form in HubSpot using Forms v2 API."""
    print("📝 Creating HubSpot form...")
    
    # Try Forms v2 API first (more stable)
    url = f"{HUBSPOT_BASE}/forms/v2/forms"
    
    # Use Forms v2 API format (simpler and more stable)
    form_data = {
        "name": "Campaign Automation Form",
        "action": "",
        "method": "POST",
        "cssClass": "",
        "redirect": "",
        "submitText": "Create Campaign",
        "followUpId": "",
        "leadNurturingCampaignId": "",
        "notifyRecipients": [],
        "formFieldGroups": [
            {
                "groupType": "default_group",
                "fields": [
                    {
                        "objectTypeId": "0-1",
                        "name": "campaign_name",
                        "label": "Campaign Name",
                        "fieldType": "single_line_text",
                        "required": True,
                        "placeholder": "e.g., 1PEvent_GTC Nvidia Afterparty_San Jose_03162026",
                        "description": "Format: Type_name_Location_Date"
                    },
                    {
                        "objectTypeId": "0-1",
                        "name": "start_date",
                        "label": "Start Date",
                        "fieldType": "datepicker",
                        "required": True
                    },
                    {
                        "objectTypeId": "0-1",
                        "name": "end_date",
                        "label": "End Date",
                        "fieldType": "datepicker",
                        "required": True
                    }
                ]
            },
            {
                "groupType": "default_group",
                "fields": [
                    {
                        "objectTypeId": "0-1",
                        "name": "member_statuses",
                        "label": "Member Statuses",
                        "fieldType": "multi_line_text",
                        "required": True,
                        "placeholder": "Registered\nWaitlist\nAttended\nNo Show",
                        "description": "Enter one status per line"
                    },
                    {
                        "objectTypeId": "0-1",
                        "name": "salesforce_status",
                        "label": "Salesforce Campaign Status",
                        "fieldType": "single_line_text",
                        "required": False,
                        "placeholder": "Planned (default), In Progress, Completed, Cancelled",
                        "defaultValue": "Planned"
                    },
                    {
                        "objectTypeId": "0-1",
                        "name": "salesforce_description",
                        "label": "Campaign Description",
                        "fieldType": "multi_line_text",
                        "required": False
                    }
                ]
            },
            {
                "groupType": "default_group",
                "fields": [
                    {
                        "objectTypeId": "0-1",
                        "name": "salesforce_type",
                        "label": "Campaign Type",
                        "fieldType": "single_line_text",
                        "required": False,
                        "placeholder": "e.g., Event, Webinar, Email"
                    },
                    {
                        "objectTypeId": "0-1",
                        "name": "parent_campaign",
                        "label": "Parent Campaign Name (Optional)",
                        "fieldType": "single_line_text",
                        "required": False,
                        "description": "Name of parent campaign if this is a child campaign"
                    },
                    {
                        "objectTypeId": "0-1",
                        "name": "hubspot_notes",
                        "label": "HubSpot Campaign Notes",
                        "fieldType": "multi_line_text",
                        "required": False
                    }
                ]
            },
            {
                "groupType": "default_group",
                "fields": [
                    {
                        "objectTypeId": "0-1",
                        "name": "wait_minutes",
                        "label": "Wait Time Before Sync (minutes)",
                        "fieldType": "number",
                        "required": False,
                        "defaultValue": "10"
                    },
                    {
                        "objectTypeId": "0-1",
                        "name": "webhook_url",
                        "label": "Custom Webhook URL (Optional)",
                        "fieldType": "single_line_text",
                        "required": False,
                        "placeholder": "https://hooks.zapier.com/..."
                    }
                ]
            }
        ],
        "submitButtonText": "Create Campaign",
        "configuration": {},
        "postSubmitAction": {
            "type": "redirect",
            "url": "https://app.hubspot.com"
        },
        "notifyRecipients": [],
        "recaptchaEnabled": False
    }
    
    headers = get_headers()
    response = requests.post(url, json=form_data, headers=headers)
    
    if response.status_code in [200, 201]:
        form = response.json()
        form_id = form.get("id")
        print(f"✅ Form created successfully! Form ID: {form_id}")
        return form_id
    else:
        print(f"❌ Error creating form: {response.status_code}")
        print(f"Response: {response.text}")
        # Try to find existing form
        if response.status_code == 409:
            print("⚠️  Form may already exist. Searching for existing form...")
            search_url = f"{HUBSPOT_BASE}/marketing/v3/forms/"
            search_response = requests.get(search_url, headers=headers, params={"name": "Campaign Automation Form"})
            if search_response.status_code == 200:
                forms = search_response.json().get("results", [])
                if forms:
                    form_id = forms[0].get("id")
                    print(f"✅ Found existing form! Form ID: {form_id}")
                    return form_id
        raise Exception(f"Failed to create form: {response.text}")


def create_landing_page(form_id):
    """Create the landing page with the form embedded."""
    print("📄 Creating HubSpot landing page...")
    
    url = f"{HUBSPOT_BASE}/cms/v3/pages/landing-pages"
    
    # Get portal ID from environment or API
    portal_id = os.environ.get("HUBSPOT_PORTAL_ID")
    if not portal_id:
        # Try to get it from account info
        try:
            account_url = f"{HUBSPOT_BASE}/integrations/v1/me"
            headers = get_headers()
            account_response = requests.get(account_url, headers=headers)
            if account_response.status_code == 200:
                account_data = account_response.json()
                portal_id = str(account_data.get("portalId", ""))
        except:
            pass
    
    if not portal_id:
        print("⚠️  Warning: Could not determine portal ID. You may need to set HUBSPOT_PORTAL_ID in .env")
        portal_id = "0"  # Will use default
    
    page_data = {
        "name": "Campaign Automation Tool",
        "slug": "campaign-automation",
        "htmlTitle": "Campaign Automation Tool - Create Campaigns in HubSpot & Salesforce",
        "metaDescription": "Create campaigns in HubSpot and Salesforce with automated workflows and segments",
        "publishImmediately": False,  # Set to True if you want to publish immediately
        "contentGroups": [],
        "campaign": "",
        "featuredImage": "",
        "headHtml": "",
        "footerHtml": "",
        "domain": "",
        "folderId": "",
        "categoryId": "",
        "state": "DRAFT",  # DRAFT, PUBLISHED, SCHEDULED
        "templatePath": None,
        "isDraft": True,
        "widgets": {
            "rows": [
                {
                    "columns": [
                        {
                            "width": 12,
                            "widgets": [
                                {
                                    "label": "Rich Text",
                                    "name": "rich_text",
                                    "type": "rich_text",
                                    "display": "CONTENT",
                                    "data": {
                                        "body": "<h1>🚀 Campaign Automation Tool</h1><p>Create campaigns in HubSpot and Salesforce with automated workflows and segments.</p><p>Fill out the form below to automatically create:</p><ul><li>Campaign in HubSpot</li><li>Campaign in Salesforce</li><li>Segments/Lists for each member status</li><li>Campaign member statuses in Salesforce</li><li>Workflows to sync list enrollments to Salesforce</li></ul>"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "columns": [
                        {
                            "width": 12,
                            "widgets": [
                                {
                                    "label": "Form",
                                    "name": "form",
                                    "type": "form",
                                    "display": "CONTENT",
                                    "data": {
                                        "formId": form_id,
                                        "formType": "hubspot"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
    
    headers = get_headers()
    response = requests.post(url, json=page_data, headers=headers)
    
    if response.status_code in [200, 201]:
        page = response.json()
        page_id = page.get("id")
        page_url = page.get("url")
        print(f"✅ Landing page created successfully!")
        print(f"   Page ID: {page_id}")
        if page_url:
            print(f"   Preview URL: {page_url}")
        return page_id, page_url
    else:
        print(f"❌ Error creating landing page: {response.status_code}")
        print(f"Response: {response.text}")
        raise Exception(f"Failed to create landing page: {response.text}")


def main():
    """Main function to create form and landing page."""
    print("=" * 60)
    print("Creating HubSpot Landing Page for Campaign Automation")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Create form
        form_id = create_form()
        print()
        
        # Step 2: Create landing page with form
        page_id, page_url = create_landing_page(form_id)
        print()
        
        print("=" * 60)
        print("✅ Setup Complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        print(f"1. Go to HubSpot → Marketing → Landing Pages")
        print(f"2. Find 'Campaign Automation Tool'")
        print(f"3. Click to edit and customize the page")
        print(f"4. Publish when ready")
        print()
        print("To connect the webhook:")
        print("1. Go to Automation → Workflows → Create workflow")
        print("2. Set trigger: 'Contact submits form' → Select 'Campaign Automation Form'")
        print("3. Add action: 'Send webhook'")
        print("4. URL: Your webhook server URL (e.g., https://your-domain.com/webhook/campaign-create)")
        print("5. See HUBSPOT_LANDING_PAGE_SETUP.md for detailed webhook configuration")
        print()
        
        if page_url:
            print(f"Preview your page: {page_url}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure HUBSPOT_ACCESS_TOKEN is set in .env")
        print("2. Verify your Private App has these scopes:")
        print("   - Marketing forms (read + write)")
        print("   - CMS pages (read + write)")
        print("3. Check that the form/landing page doesn't already exist")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
