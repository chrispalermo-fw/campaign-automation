#!/usr/bin/env python3
"""
Helper script to find HubSpot list IDs by name.
This helps when lists exist but we can't find their IDs automatically.
"""
import os
import sys
from dotenv import load_dotenv
from src.hubspot_client import get_client

load_dotenv()

def find_lists_by_name_pattern(pattern: str):
    """Find lists that match a name pattern."""
    print(f"Searching for lists matching: '{pattern}'")
    print("-" * 60)
    
    hs = get_client()
    
    # Try to get all lists with pagination
    url = "https://api.hubapi.com/crm/v3/lists"
    all_lists = []
    offset = None
    
    try:
        while True:
            params = {"limit": 100}
            if offset:
                params["after"] = offset
            
            r = hs._session.get(url, params=params)
            r.raise_for_status()
            result = r.json()
            lists = result.get("lists", [])
            all_lists.extend(lists)
            
            # Check pagination
            paging = result.get("paging", {})
            if paging.get("next"):
                offset = paging["next"].get("after")
            else:
                break
        
        # Search for matching lists
        matches = []
        for list_obj in all_lists:
            name = list_obj.get("name", "")
            if pattern.lower() in name.lower():
                matches.append({
                    "name": name,
                    "id": str(list_obj.get("listId", "")),
                    "createdAt": list_obj.get("createdAt", ""),
                })
        
        if matches:
            print(f"\n✓ Found {len(matches)} matching list(s):\n")
            for match in matches:
                print(f"  Name: {match['name']}")
                print(f"  ID:   {match['id']}")
                print(f"  Created: {match['createdAt']}")
                print()
            
            print("\n" + "=" * 60)
            print("Add these to your YAML config:")
            print("=" * 60)
            print("hubspot:")
            print("  list_ids:")
            for match in matches:
                print(f"    - {match['id']}  # {match['name']}")
            print("\n  list_status_map:")
            for match in matches:
                # Try to extract status from name
                name = match['name']
                if " - " in name:
                    status = name.split(" - ")[-1]
                    print(f"    \"{match['id']}\": \"{status}\"")
        else:
            print(f"\n⚠️  No lists found matching '{pattern}'")
            print("\nPossible reasons:")
            print("  1. Lists API doesn't have read permissions")
            print("  2. Lists don't exist yet")
            print("  3. List names don't match the pattern")
            print("\nTo find list IDs manually:")
            print("  1. Go to HubSpot → Contacts → Lists")
            print("  2. Open each list")
            print("  3. The ID is in the URL: .../list/12345678")
            print("  4. Or check the list settings page")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nThe Lists API might not have read permissions.")
        print("You'll need to find list IDs manually in HubSpot UI:")
        print("  1. Go to HubSpot → Contacts → Lists")
        print("  2. Open each list")
        print("  3. Check the URL or list settings for the ID")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        pattern = "1PEvent_ GTC Nvidia Afterparty_San Jose_03162026"
        print("No pattern provided, using default:")
        print(f"  Pattern: '{pattern}'")
        print()
    else:
        pattern = sys.argv[1]
    
    find_lists_by_name_pattern(pattern)
