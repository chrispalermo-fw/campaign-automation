#!/usr/bin/env python3
"""
Create workflow directly using known list ID and Salesforce campaign ID.
"""
import os
import sys
from dotenv import load_dotenv
from src.hubspot_client import get_client as get_hubspot

load_dotenv()

def main():
    if len(sys.argv) < 5:
        print("Usage: python create_workflow_direct.py <workflow_name> <list_id> <salesforce_campaign_id> <status> [wait_minutes]")
        print("\nExample:")
        print("  python create_workflow_direct.py 'Campaign - Booth Visit' 1204 701PY00001RqXcuYAF 'Booth Visit' 10")
        sys.exit(1)
    
    workflow_name = sys.argv[1]
    list_id = sys.argv[2]
    salesforce_campaign_id = sys.argv[3]
    status = sys.argv[4]
    wait_minutes = int(sys.argv[5]) if len(sys.argv) > 5 else 10
    
    # Extract campaign name from workflow name (remove " - Status" part)
    campaign_name = workflow_name.rsplit(" - ", 1)[0] if " - " in workflow_name else workflow_name
    
    print(f"🚀 Creating workflow:")
    print(f"   Workflow Name: {workflow_name}")
    print(f"   List ID: {list_id}")
    print(f"   Salesforce Campaign ID: {salesforce_campaign_id}")
    print(f"   Status: {status}")
    print(f"   Wait Minutes: {wait_minutes}")
    print()
    
    hs = get_hubspot()
    
    try:
        workflow = hs.create_workflow_with_enrollment(
            workflow_name=workflow_name,
            list_id=list_id,
            salesforce_campaign_id=salesforce_campaign_id,
            salesforce_status=status,
            wait_minutes=wait_minutes,
            webhook_url=None,
            salesforce_campaign_name=campaign_name,
        )
        workflow_id = workflow.get("id")
        print(f"\n✅ Successfully created workflow!")
        print(f"   Workflow ID: {workflow_id}")
        print(f"   Workflow Name: {workflow_name}")
        print(f"\n⚠️  Next steps:")
        print(f"   1. Go to HubSpot → Automation → Workflows")
        print(f"   2. Open '{workflow_name}' (ID: {workflow_id})")
        print(f"   3. Verify enrollment trigger is set (should be automatic)")
        print(f"   4. Verify/configure Salesforce action if needed")
        print(f"   5. Activate the workflow")
        
    except Exception as e:
        print(f"\n❌ Failed to create workflow: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
