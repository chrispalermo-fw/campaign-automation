#!/usr/bin/env python3
"""
Create workflows for an existing campaign.
Finds the campaign in HubSpot and Salesforce, then creates workflows for specified segments.
"""
import os
import sys
from dotenv import load_dotenv
from src.hubspot_client import get_client as get_hubspot
from src.salesforce_client import get_client as get_salesforce

load_dotenv()

def find_hubspot_campaign(hs, campaign_name):
    """Find HubSpot campaign by name."""
    print(f"🔍 Searching for HubSpot campaign: {campaign_name}")
    
    # Try to get recent campaigns
    url = "https://api.hubapi.com/marketing/v3/campaigns"
    params = {"limit": 100, "sort": "-createdAt"}
    r = hs._session.get(url, params=params)
    r.raise_for_status()
    result = r.json()
    
    campaigns = result.get("results", [])
    
    # Try exact match first
    for campaign in campaigns:
        props = campaign.get("properties", {})
        name = props.get("hs_name", "")
        if name == campaign_name:
            campaign_id = campaign.get("id")
            print(f"✅ Found HubSpot campaign: {campaign_name} (id={campaign_id})")
            return campaign_id
    
    # Try partial match (in case of slight name differences)
    print(f"   Exact match not found, trying partial match...")
    for campaign in campaigns:
        props = campaign.get("properties", {})
        name = props.get("hs_name", "")
        # Check if campaign_name is contained in name or vice versa
        if campaign_name.lower() in name.lower() or name.lower() in campaign_name.lower():
            campaign_id = campaign.get("id")
            print(f"✅ Found HubSpot campaign (partial match): {name} (id={campaign_id})")
            print(f"   Using this campaign...")
            return campaign_id
    
    # Show recent campaigns for debugging
    print(f"\n❌ HubSpot campaign '{campaign_name}' not found")
    print(f"   Recent campaigns found:")
    for campaign in campaigns[:5]:
        props = campaign.get("properties", {})
        name = props.get("hs_name", "")
        campaign_id = campaign.get("id")
        print(f"     - {name} (id={campaign_id})")
    
    return None

def find_salesforce_campaign(sf, campaign_name):
    """Find Salesforce campaign by name."""
    print(f"🔍 Searching for Salesforce campaign: {campaign_name}")
    
    # Escape single quotes in campaign name
    escaped_name = campaign_name.replace("'", "''")
    query = f"SELECT Id, Name FROM Campaign WHERE Name = '{escaped_name}' LIMIT 1"
    result = sf.query(query)
    
    if result.get("records"):
        campaign_id = result["records"][0]["Id"]
        print(f"✅ Found Salesforce campaign: {campaign_name} (id={campaign_id})")
        return campaign_id
    
    print(f"❌ Salesforce campaign '{campaign_name}' not found")
    return None

def find_list_by_name(hs, list_name, campaign_id=None):
    """Find HubSpot list/segment by name."""
    print(f"🔍 Searching for list/segment: {list_name}")
    
    list_id = hs.find_list_by_name(list_name)
    if list_id:
        print(f"✅ Found list '{list_name}' (id={list_id})")
        return list_id
    
    # Try exact name search
    list_id = hs.find_list_by_exact_name(list_name)
    if list_id:
        print(f"✅ Found list '{list_name}' via exact search (id={list_id})")
        return list_id
    
    # If campaign_id provided, check campaign assets
    if campaign_id:
        print(f"   Checking campaign assets for list...")
        try:
            assets = hs.get_campaign_assets(campaign_id)
            print(f"   Found {len(assets)} assets associated with campaign")
            for asset in assets:
                asset_name = asset.get("name", "")
                asset_id = str(asset.get("id", ""))
                if list_name.lower() in asset_name.lower() or asset_name.lower() in list_name.lower():
                    print(f"✅ Found list in campaign assets: {asset_name} (id={asset_id})")
                    return asset_id
        except Exception as e:
            print(f"   Could not check campaign assets: {e}")
    
    # Show recent lists for debugging
    print(f"❌ List '{list_name}' not found")
    print(f"   Searching all lists for similar names...")
    try:
        url = "https://api.hubapi.com/crm/v3/lists"
        params = {"limit": 100}
        r = hs._session.get(url, params=params)
        if r.status_code == 200:
            result = r.json()
            lists = result.get("lists", [])
            matching_lists = []
            search_terms = list_name.lower().split()
            for lst in lists:
                lst_name = lst.get("name", "").lower()
                # Check if any search term matches
                if any(term in lst_name for term in search_terms if len(term) > 3):
                    matching_lists.append((lst.get("name"), lst.get("listId")))
            
            if matching_lists:
                print(f"   Found {len(matching_lists)} similar lists:")
                for name, lid in matching_lists[:10]:
                    print(f"     - {name} (id={lid})")
                    # If it's a close match, use it
                    if list_name.lower().replace(" ", "").replace("_", "") in name.lower().replace(" ", "").replace("_", ""):
                        print(f"   ✅ Using close match: {name} (id={lid})")
                        return str(lid)
    except Exception as e:
        print(f"   Could not search all lists: {e}")
    
    print(f"   Tip: Check HubSpot → Marketing → Campaigns → Your Campaign → Lists tab")
    return None

def create_workflow_for_segment(hs, campaign_name, segment_name, status, salesforce_campaign_id, hubspot_campaign_id=None, wait_minutes=10):
    """Create a workflow for a specific segment."""
    print(f"\n🚀 Creating workflow for segment: {segment_name}")
    print(f"   Status: {status}")
    print(f"   Salesforce Campaign ID: {salesforce_campaign_id}")
    
    # Find the list ID
    list_id = find_list_by_name(hs, segment_name, campaign_id=hubspot_campaign_id)
    if not list_id:
        print(f"❌ Cannot create workflow - list not found")
        return None
    
    # Create workflow
    try:
        workflow = hs.create_workflow_with_enrollment(
            workflow_name=segment_name,
            list_id=list_id,
            salesforce_campaign_id=salesforce_campaign_id,
            salesforce_status=status,
            wait_minutes=wait_minutes,
            webhook_url=None,
            salesforce_campaign_name=campaign_name,
        )
        workflow_id = workflow.get("id")
        print(f"✅ Successfully created workflow '{segment_name}' (id={workflow_id})")
        return workflow_id
    except Exception as e:
        print(f"❌ Failed to create workflow: {e}")
        import traceback
        print(traceback.format_exc())
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_workflows_for_existing_campaign.py <campaign_name> [status1] [status2] ...")
        print("\nExample:")
        print("  python create_workflows_for_existing_campaign.py '3PEvent_ HumanX_ San Francisco_04062026' 'Booth Visit' 'Hot Lead' 'Demo'")
        sys.exit(1)
    
    campaign_name = sys.argv[1]
    statuses = sys.argv[2:] if len(sys.argv) > 2 else []
    
    if not statuses:
        print("⚠️  No statuses provided. Please specify at least one status.")
        print("Example: python create_workflows_for_existing_campaign.py 'Campaign Name' 'Booth Visit'")
        sys.exit(1)
    
    print(f"📋 Campaign: {campaign_name}")
    print(f"📋 Statuses: {', '.join(statuses)}")
    print()
    
    # Initialize clients
    hs = get_hubspot()
    sf = get_salesforce()
    
    # Find campaigns
    hubspot_campaign_id = find_hubspot_campaign(hs, campaign_name)
    salesforce_campaign_id = find_salesforce_campaign(sf, campaign_name)
    
    if not hubspot_campaign_id:
        print("\n❌ Cannot proceed - HubSpot campaign not found")
        sys.exit(1)
    
    if not salesforce_campaign_id:
        print("\n❌ Cannot proceed - Salesforce campaign not found")
        sys.exit(1)
    
    # Create workflows for each status
    created_workflows = []
    for status in statuses:
        segment_name = f"{campaign_name} - {status}"
        workflow_id = create_workflow_for_segment(
            hs, campaign_name, segment_name, status, salesforce_campaign_id, hubspot_campaign_id=hubspot_campaign_id
        )
        if workflow_id:
            created_workflows.append({
                "segment": segment_name,
                "status": status,
                "workflow_id": workflow_id
            })
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ Summary: Created {len(created_workflows)} workflow(s)")
    for wf in created_workflows:
        print(f"   - {wf['segment']} → {wf['status']} (Workflow ID: {wf['workflow_id']})")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
