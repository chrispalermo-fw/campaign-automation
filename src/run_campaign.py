"""
Run campaign creation from a YAML config.
Creates campaign in HubSpot (name, taxonomy, list associations) and Salesforce (name, type, status),
then optionally triggers a workflow webhook (e.g. Zapier).
"""
import os
import sys
from pathlib import Path
from typing import Union

import yaml
from dotenv import load_dotenv

from .hubspot_client import get_client as get_hubspot
from .salesforce_client import (
    get_client as get_salesforce,
    create_campaign as sf_create_campaign,
    find_parent_campaign,
    create_campaign_member_statuses,
)

load_dotenv()


def load_config(path: Union[str, Path]) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def run(config_path: Union[str, Path]) -> dict:
    """
    Load YAML config, create campaign in HubSpot and Salesforce, associate lists, trigger workflows.
    Returns dict with hubspot_campaign_id, salesforce_campaign_id, and any workflow result.
    """
    config = load_config(config_path)
    name = config["name"]
    start_date = config.get("start_date")
    end_date = config.get("end_date")
    taxonomy = config.get("taxonomy") or {}
    hubspot_cfg = config.get("hubspot") or {}
    salesforce_cfg = config.get("salesforce") or {}
    workflows_cfg = config.get("workflows") or {}

    # --- HubSpot ---
    hs = get_hubspot()
    hs_props = hs.build_properties(
        name=name,
        start_date=start_date,
        end_date=end_date,
        taxonomy=taxonomy.get("hubspot"),
        tags=config.get("tags"),
        extra=hubspot_cfg.get("extra_properties"),
    )
    hubspot_campaign = hs.create_campaign(hs_props)
    hubspot_id = hubspot_campaign["id"]
    print(f"Created HubSpot campaign: {name} (id={hubspot_id})")

    # Create segments for each member status if auto_create_segments is enabled
    member_statuses = hubspot_cfg.get("auto_create_segments", [])
    created_list_ids = []
    list_status_map = {}  # Map list_id to status name for workflow creation
    
    if member_statuses:
        for status in member_statuses:
            list_name = f"{name} - {status}"
            list_id = hs.create_list(list_name, name, campaign_id=hubspot_id)
            if list_id:
                created_list_ids.append(list_id)
                list_status_map[list_id] = status
                # Always try to associate, even if list existed before
                try:
                    hs.associate_list(hubspot_id, list_id)
                    print(f"  ✓ Associated list '{list_name}' (id={list_id}) with campaign")
                except Exception as e:
                    # List might already be associated, that's okay
                    error_str = str(e).lower()
                    if any(keyword in error_str for keyword in ["already", "409", "duplicate", "conflict"]):
                        print(f"  ✓ List '{list_name}' (id={list_id}) already associated with campaign")
                    else:
                        print(f"  ⚠️  Warning: Could not associate list '{list_name}': {e}")
            else:
                # List exists but we couldn't find its ID - try to find it one more time
                # by checking campaign assets after all lists are processed
                print(f"  ⚠️  List '{list_name}' exists but ID not found - will retry after processing other lists")

    # Also associate any manually provided list IDs
    manual_list_ids = hubspot_cfg.get("list_ids") or []
    manual_list_status_map = hubspot_cfg.get("list_status_map", {})  # Map list_id to status
    for list_id in manual_list_ids:
        list_id_str = str(list_id)
        try:
            hs.associate_list(hubspot_id, list_id_str)
            created_list_ids.append(list_id_str)
            # Try to find status for this list ID
            if list_id_str in manual_list_status_map:
                list_status_map[list_id_str] = manual_list_status_map[list_id_str]
            else:
                # Try to infer status from list name if not explicitly mapped
                # This is a fallback - ideally user should provide list_status_map
                pass
            print(f"  ✓ Associated list id={list_id_str}")
        except Exception as e:
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ["already", "409", "duplicate", "conflict"]):
                print(f"  ✓ List id={list_id_str} already associated with campaign")
                created_list_ids.append(list_id_str)
                if list_id_str in manual_list_status_map:
                    list_status_map[list_id_str] = manual_list_status_map[list_id_str]
            else:
                print(f"  ⚠️  Warning: Could not associate list id={list_id_str}: {e}")
    
    # Try to find any missing list IDs by checking campaign assets
    if member_statuses:
        try:
            assets = hs.get_campaign_assets(hubspot_id)
            for asset in assets:
                asset_name = asset.get("name", "")
                asset_id = str(asset.get("id", ""))
                # Check if this asset matches any of our expected list names
                for status in member_statuses:
                    expected_name = f"{name} - {status}"
                    if asset_name == expected_name:
                        # Add to created_list_ids if not already there
                        if asset_id not in created_list_ids:
                            created_list_ids.append(asset_id)
                        # Map to status if not already mapped
                        if asset_id not in list_status_map:
                            list_status_map[asset_id] = status
                            print(f"  ✓ Found and mapped existing list '{asset_name}' (id={asset_id})")
        except Exception as e:
            # Assets endpoint might not be available or might fail
            print(f"  ⚠️  Could not check campaign assets: {e}")
    
    # Final fallback: Try to map any unmapped list IDs by searching for their names
    if member_statuses and created_list_ids:
        unmapped_ids = [lid for lid in created_list_ids if lid not in list_status_map]
        if unmapped_ids:
            print(f"  🔍 Found {len(unmapped_ids)} unmapped list IDs, attempting to map by name...")
            for list_id in unmapped_ids:
                # Try to get list details to find its name
                try:
                    # Search all lists to find this one
                    for status in member_statuses:
                        list_name = f"{name} - {status}"
                        found_id = hs.find_list_by_name(list_name)
                        if found_id == list_id:
                            list_status_map[list_id] = status
                            print(f"  ✓ Mapped list ID {list_id} to status '{status}'")
                            break
                except Exception as e:
                    print(f"  ⚠️  Could not map list ID {list_id}: {e}")

    # --- Salesforce ---
    sf = get_salesforce()
    desc = salesforce_cfg.get("description") or salesforce_cfg.get("Description")
    
    # Required fields: IsActive=True, StartDate, EndDate
    sf_fields = {
        "IsActive": True,
    }
    if start_date:
        sf_fields["StartDate"] = start_date
    if end_date:
        sf_fields["EndDate"] = end_date
    
    # Optional fields
    sf_fields["Status"] = salesforce_cfg.get("status") or "Planned"
    if desc:
        sf_fields["Description"] = desc
    if taxonomy.get("salesforce"):
        sf_fields.update(taxonomy["salesforce"])
    if salesforce_cfg.get("custom_fields"):
        sf_fields.update(salesforce_cfg["custom_fields"])
    
    # Handle parent campaign lookup
    parent_name = salesforce_cfg.get("parent_campaign")
    if parent_name:
        parent_id = find_parent_campaign(sf, parent_name)
        if parent_id:
            sf_fields["ParentId"] = parent_id
            print(f"  Found parent campaign '{parent_name}' (id={parent_id})")
        else:
            print(f"  Warning: Parent campaign '{parent_name}' not found in Salesforce")
    
    salesforce_id = sf_create_campaign(sf, name, **sf_fields)
    print(f"Created Salesforce campaign: {name} (id={salesforce_id})")
    
    # Create campaign member statuses
    member_statuses = salesforce_cfg.get("member_statuses") or hubspot_cfg.get("auto_create_segments", [])
    if member_statuses:
        print(f"Creating campaign member statuses: {', '.join(member_statuses)}")
        create_campaign_member_statuses(sf, salesforce_id, member_statuses)

    # --- HubSpot Workflows: Create workflows to sync list enrollments to Salesforce ---
    create_workflows = hubspot_cfg.get("create_workflows", True)  # Default to True
    workflow_webhook_url = workflows_cfg.get("zapier_webhook_url") or os.environ.get("ZAPIER_CAMPAIGN_CREATED_WEBHOOK")
    wait_minutes = workflows_cfg.get("wait_minutes", 10)  # Default 10 minutes
    
    created_workflows = []
    if create_workflows and member_statuses and salesforce_id:
        print(f"\nCreating HubSpot workflows to sync list enrollments to Salesforce...")
        print(f"  List status map: {list_status_map}")
        print(f"  Created list IDs: {created_list_ids}")
        print(f"  Member statuses: {member_statuses}")
        
        # Final attempt: Match unmapped list IDs to statuses by checking list names
        unmapped_ids = [lid for lid in created_list_ids if lid not in list_status_map]
        if unmapped_ids:
            print(f"  🔍 Found {len(unmapped_ids)} unmapped list IDs, attempting to map by name...")
            for list_id in unmapped_ids:
                for status in member_statuses:
                    list_name = f"{name} - {status}"
                    found_id = hs.find_list_by_name(list_name)
                    if found_id == list_id or found_id == str(list_id):
                        list_status_map[list_id] = status
                        print(f"  ✓ Mapped list ID {list_id} to status '{status}' via name search")
                        break
        
        for status in member_statuses:
            # Find the list ID for this status
            list_id = None
            list_name = f"{name} - {status}"
            
            # Check if we have the list ID from created lists
            for lid, stat in list_status_map.items():
                if stat == status:
                    list_id = lid
                    break
            
            # If not found, try to find it by searching for the list by name
            if not list_id:
                print(f"  🔍 List ID not in map, searching for list: '{list_name}'")
                list_id = hs.find_list_by_name(list_name)
                if list_id:
                    print(f"  ✓ Found list '{list_name}' (id={list_id})")
                    list_status_map[list_id] = status
                else:
                    # Try exact name search as fallback
                    list_id = hs.find_list_by_exact_name(list_name)
                    if list_id:
                        print(f"  ✓ Found list '{list_name}' via exact search (id={list_id})")
                        list_status_map[list_id] = status
            
            # If still not found, try to find it from manual list_ids
            if not list_id and manual_list_ids:
                # Try to match by checking if we can find the list
                # For now, we'll create workflow even if list_id is not found
                # User will need to configure enrollment trigger manually
                pass
            
            if list_id:
                workflow_name = list_name  # Same name as segment
                try:
                    print(f"  🚀 Creating workflow '{workflow_name}' with list_id={list_id}, status={status}")
                    workflow = hs.create_workflow_with_enrollment(
                        workflow_name=workflow_name,
                        list_id=list_id,
                        salesforce_campaign_id=salesforce_id,
                        salesforce_status=status,
                        wait_minutes=wait_minutes,
                        webhook_url=workflow_webhook_url,
                        salesforce_campaign_name=name,
                    )
                    created_workflows.append({
                        "name": workflow_name,
                        "id": workflow.get("id"),
                        "status": status,
                        "list_id": list_id,
                    })
                    print(f"  ✅ Created workflow '{workflow_name}' (id={workflow.get('id')})")
                except Exception as e:
                    print(f"  ❌ Failed to create workflow for '{workflow_name}': {e}")
                    import traceback
                    print(f"     Traceback: {traceback.format_exc()}")
                    print(f"     You may need to create this workflow manually in HubSpot UI")
            else:
                print(f"  ⚠️  Skipped workflow creation for '{list_name}' (list ID not found)")
                print(f"     Create workflow manually: Name='{list_name}', Trigger='Contact added to list', Wait={wait_minutes}min, Update Salesforce CampaignMember status='{status}'")

    # --- Workflows (e.g. Zapier webhook) ---
    webhook = workflows_cfg.get("zapier_webhook_url") or os.environ.get("ZAPIER_CAMPAIGN_CREATED_WEBHOOK")
    workflow_result = {}
    if webhook:
        import requests
        r = requests.post(
            webhook,
            json={
                "hubspot_campaign_id": hubspot_id,
                "salesforce_campaign_id": salesforce_id,
                "campaign_name": name,
            },
        )
        workflow_result["webhook_status"] = r.status_code
        print(f"Triggered workflow webhook: {r.status_code}")

    return {
        "hubspot_campaign_id": hubspot_id,
        "salesforce_campaign_id": salesforce_id,
        "campaign_name": name,
        "hubspot_list_ids": created_list_ids,
        "hubspot_workflows": created_workflows,
        "workflow": workflow_result,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.run_campaign <path-to-campaign.yaml>")
        sys.exit(1)
    path = Path(sys.argv[1]).resolve()
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)
    result = run(path)
    print("\nDone.", result)


if __name__ == "__main__":
    main()
