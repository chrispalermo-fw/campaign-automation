#!/usr/bin/env python3
"""
Test script to verify HubSpot Automation API access.
Run this after adding Automation scope to your Private App.
"""
import os
from dotenv import load_dotenv
from src.hubspot_client import get_client

load_dotenv()

def test_automation_access():
    """Test if we can access the HubSpot Automation API."""
    print("Testing HubSpot Automation API access...")
    print("-" * 50)
    
    hs = get_client()
    
    # Test 1: Try to list workflows
    print("\n1. Testing GET /automation/v3/workflows...")
    try:
        url = "https://api.hubapi.com/automation/v3/workflows"
        r = hs._session.get(url)
        
        if r.status_code == 200:
            workflows = r.json()
            count = len(workflows) if isinstance(workflows, list) else 0
            print(f"   ✓ SUCCESS! Found {count} existing workflow(s)")
            if workflows and isinstance(workflows, list) and len(workflows) > 0:
                print(f"   Sample workflow: {workflows[0].get('name', 'N/A')}")
            test_automation_access._read_works = True  # Mark read as working
        elif r.status_code == 403:
            print(f"   ❌ FAILED: Missing Automation scope!")
            print(f"   Error: {r.json().get('message', 'Unknown error')}")
            print(f"\n   → Please add Automation scope to your Private App:")
            print(f"     1. Go to HubSpot Settings > Integrations > Private Apps")
            print(f"     2. Edit your 'Campaign Automation Tool' app")
            print(f"     3. Add scopes: Automation → Read, Automation → Write")
            print(f"     4. Save and regenerate token if needed")
            return False
        else:
            print(f"   ⚠️  Unexpected status: {r.status_code}")
            print(f"   Response: {r.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test 2: Try to create a test workflow
    print("\n2. Testing POST /automation/v3/workflows (creating test workflow)...")
    try:
        test_workflow_name = "TEST - Delete Me - Automation API Test"
        url = "https://api.hubapi.com/automation/v3/workflows"
        payload = {
            "name": test_workflow_name,
            "type": "DRIP_DELAY",
            "onlyEnrollsManually": True,  # Manual enrollment for test
            "actions": [
                {
                    "type": "DELAY",
                    "delayMillis": 60000,  # 1 minute
                }
            ],
        }
        
        r = hs._session.post(url, json=payload)
        
        if r.status_code in [200, 201]:  # Both 200 and 201 indicate success
            workflow = r.json()
            # Handle different response formats
            if isinstance(workflow, dict):
                workflow_id = workflow.get("id") or workflow.get("workflowId")
            else:
                workflow_id = None
            print(f"   ✓ SUCCESS! Created test workflow (id={workflow_id})")
            print(f"   → You can delete this workflow in HubSpot UI if needed")
            
            # Try to delete it immediately (cleanup)
            if workflow_id:
                try:
                    delete_url = f"{url}/{workflow_id}"
                    delete_r = hs._session.delete(delete_url)
                    if delete_r.status_code in [200, 204]:
                        print(f"   ✓ Cleaned up test workflow")
                except:
                    pass  # Ignore cleanup errors
                    
            return True
        elif r.status_code == 403:
            print(f"   ❌ FAILED: Missing Automation write scope!")
            print(f"   Error: {r.json().get('message', 'Unknown error')}")
            return False
        else:
            print(f"   ⚠️  Unexpected status: {r.status_code}")
            print(f"   Response: {r.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_automation_access()
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! Your Automation scope is configured correctly.")
        print("   You can now run: python -m src.run_campaign config/campaigns/gtc-nvidia-afterparty.yaml")
    else:
        print("❌ Tests failed. Please add Automation scope to your Private App.")
        print("   See ADD_AUTOMATION_SCOPE.md for detailed instructions.")
    print("=" * 50)
