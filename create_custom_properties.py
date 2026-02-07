#!/usr/bin/env python3
"""
Create custom HubSpot contact properties for campaign automation form fields.
This script creates all the required properties so you can connect your form fields.
"""
import os
from dotenv import load_dotenv
import requests

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


def create_property(name, label, field_type, description=""):
    """Create a custom contact property in HubSpot."""
    url = f"{HUBSPOT_BASE}/crm/v3/properties/contacts"
    
    # Map our field types to HubSpot property types
    hubspot_type_map = {
        "single_line_text": "string",
        "multi_line_text": "string",  # Use string for textarea, can be long
        "date": "date",
        "datepicker": "date",
        "number": "number",
        "textarea": "string",
        "text": "string",
    }
    
    property_type = hubspot_type_map.get(field_type, "string")
    
    # Build property data based on type
    property_data = {
        "name": name,
        "label": label,
        "type": property_type,
        "groupName": "contactinformation",
        "description": description,
        "formField": True,
        "hasUniqueValue": False,
        "hidden": False,
    }
    
    # Set fieldType based on property type
    if property_type == "date":
        property_data["fieldType"] = "date"
    elif property_type == "number":
        property_data["fieldType"] = "number"
        property_data["numberDisplayHint"] = "unformatted"
    else:
        # For string/text types, use textarea for multi-line, text for single-line
        if field_type in ["multi_line_text", "textarea"]:
            property_data["fieldType"] = "textarea"
        else:
            property_data["fieldType"] = "text"
    
    headers = get_headers()
    response = requests.post(url, json=property_data, headers=headers)
    
    if response.status_code in [200, 201]:
        prop = response.json()
        print(f"  ✅ Created: {label} ({name})")
        return True
    elif response.status_code == 409:
        print(f"  ⚠️  Already exists: {label} ({name})")
        return True  # Property already exists, that's okay
    else:
        print(f"  ❌ Error creating {label}: {response.status_code}")
        print(f"     Response: {response.text[:200]}")
        return False


def main():
    """Create all required custom properties."""
    print("=" * 60)
    print("Creating Custom HubSpot Contact Properties")
    print("=" * 60)
    print()
    
    properties = [
        # Required fields
        {
            "name": "campaign_name",
            "label": "Campaign Name",
            "type": "single_line_text",
            "description": "Campaign name from automation form"
        },
        {
            "name": "start_date",
            "label": "Campaign Start Date",
            "type": "date",
            "description": "Campaign start date from automation form"
        },
        {
            "name": "end_date",
            "label": "Campaign End Date",
            "type": "date",
            "description": "Campaign end date from automation form"
        },
        {
            "name": "member_statuses",
            "label": "Campaign Member Statuses",
            "type": "multi_line_text",
            "description": "Member statuses for campaign automation (one per line)"
        },
        # Optional fields
        {
            "name": "salesforce_status",
            "label": "Salesforce Campaign Status",
            "type": "single_line_text",
            "description": "Salesforce campaign status from automation form"
        },
        {
            "name": "salesforce_description",
            "label": "Salesforce Campaign Description",
            "type": "multi_line_text",
            "description": "Campaign description for Salesforce"
        },
        {
            "name": "salesforce_type",
            "label": "Salesforce Campaign Type",
            "type": "single_line_text",
            "description": "Campaign type (e.g., Event, Webinar)"
        },
        {
            "name": "parent_campaign",
            "label": "Parent Campaign Name",
            "type": "single_line_text",
            "description": "Parent campaign name if this is a child campaign"
        },
        {
            "name": "hubspot_notes",
            "label": "Campaign HubSpot Notes",
            "type": "multi_line_text",
            "description": "Notes for HubSpot campaign"
        },
        {
            "name": "wait_minutes",
            "label": "Campaign Wait Minutes",
            "type": "number",
            "description": "Wait time in minutes before syncing to Salesforce"
        },
        {
            "name": "webhook_url",
            "label": "Campaign Webhook URL",
            "type": "single_line_text",
            "description": "Custom webhook URL for campaign automation"
        },
    ]
    
    print("Creating properties...")
    print()
    
    success_count = 0
    for prop in properties:
        if create_property(prop["name"], prop["label"], prop["type"], prop["description"]):
            success_count += 1
    
    print()
    print("=" * 60)
    if success_count == len(properties):
        print("✅ All properties created successfully!")
    else:
        print(f"⚠️  Created {success_count} out of {len(properties)} properties")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Go back to your form in HubSpot")
    print("2. Connect each form field to its corresponding property:")
    print("   - Campaign Name → campaign_name")
    print("   - Start Date → start_date")
    print("   - End Date → end_date")
    print("   - Member Statuses → member_statuses")
    print("   - (and so on for optional fields)")
    print("3. Save the form")
    print()
    print("Note: These properties will store data on contacts when the form")
    print("      is submitted. This is required for HubSpot forms to work.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure HUBSPOT_ACCESS_TOKEN is set in .env")
        print("2. Verify your Private App has 'Contacts' → 'Read' and 'Write' scopes")
        print("3. Check that property names don't conflict with existing properties")
