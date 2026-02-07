#!/usr/bin/env python3
"""
Create HubSpot landing page with the existing Campaign Automation Form embedded.
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


def find_form_id():
    """Find the Campaign Automation Form ID."""
    print("🔍 Finding Campaign Automation Form...")
    url = f"{HUBSPOT_BASE}/marketing/v3/forms/"
    headers = get_headers()
    response = requests.get(url, headers=headers, params={"name": "Campaign Automation Form"})
    
    if response.status_code == 200:
        forms = response.json().get("results", [])
        for form in forms:
            if form.get("name") == "Campaign Automation Form":
                form_id = form.get("id")
                print(f"✅ Found form! Form ID: {form_id}")
                return form_id
    
    # Try searching all forms
    response = requests.get(url, headers=headers, params={"limit": 100})
    if response.status_code == 200:
        forms = response.json().get("results", [])
        print(f"Found {len(forms)} forms. Searching for 'Campaign Automation Form'...")
        for form in forms:
            name = form.get("name", "")
            if "Campaign Automation" in name or "campaign automation" in name.lower():
                form_id = form.get("id")
                print(f"✅ Found form: '{name}' (ID: {form_id})")
                return form_id
    
    raise Exception("Could not find 'Campaign Automation Form'. Make sure it's published.")


def create_landing_page(form_id):
    """Create the landing page with the form embedded."""
    print("📄 Creating HubSpot landing page...")
    
    url = f"{HUBSPOT_BASE}/cms/v3/pages/landing-pages"
    
    # Simplified page structure - HubSpot CMS API can be complex
    # We'll create a basic page structure
    page_data = {
        "name": "Campaign Automation Tool",
        "slug": "campaign-automation",
        "htmlTitle": "Campaign Automation Tool - Create Campaigns in HubSpot & Salesforce",
        "metaDescription": "Create campaigns in HubSpot and Salesforce with automated workflows and segments",
        "state": "DRAFT",  # Create as draft, user can publish manually
        "publishImmediately": False,
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
        print(f"Response: {response.text[:500]}")
        raise Exception(f"Failed to create landing page: {response.text}")


def main():
    """Main function to create landing page."""
    print("=" * 60)
    print("Creating HubSpot Landing Page")
    print("=" * 60)
    print()
    
    try:
        # Find the form
        form_id = find_form_id()
        print()
        
        # Create landing page
        page_id, page_url = create_landing_page(form_id)
        print()
        
        print("=" * 60)
        print("✅ Landing Page Created!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Go to HubSpot → Marketing → Landing Pages")
        print("2. Find 'Campaign Automation Tool'")
        print("3. Click to edit")
        print("4. Add your form:")
        print("   - Drag 'Form' module onto the page")
        print("   - Select 'Campaign Automation Form'")
        print("5. Add heading/content above the form:")
        print("   - Heading: '🚀 Campaign Automation Tool'")
        print("   - Description explaining what it does")
        print("6. Publish when ready")
        print()
        
        if page_url:
            print(f"Preview/edit your page: {page_url}")
        else:
            print("Find your page: Marketing → Landing Pages → Campaign Automation Tool")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nAlternative: Create landing page manually:")
        print("1. HubSpot → Marketing → Landing Pages → Create landing page")
        print("2. Name: 'Campaign Automation Tool'")
        print("3. Add form module → Select 'Campaign Automation Form'")
        print("4. Publish")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
