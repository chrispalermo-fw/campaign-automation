"""
Salesforce Campaign (and optional CampaignMember) client.
Uses simple_salesforce for auth and REST.
"""
import os
from typing import Optional
from simple_salesforce import Salesforce


def get_client():
    """
    Build Salesforce client using username/password + security token method.
    Requires: SALESFORCE_USERNAME, SALESFORCE_PASSWORD, SALESFORCE_SECURITY_TOKEN
    Optional: SALESFORCE_DOMAIN (defaults to 'login' for production, use 'test' for sandbox)
    """
    username = os.environ.get("SALESFORCE_USERNAME")
    password = os.environ.get("SALESFORCE_PASSWORD")
    security_token = os.environ.get("SALESFORCE_SECURITY_TOKEN", "")
    domain = os.environ.get("SALESFORCE_DOMAIN", "login")
    
    if not username or not password:
        raise ValueError("Set SALESFORCE_USERNAME and SALESFORCE_PASSWORD")
    
    # Use security_token parameter if provided, otherwise assume it's appended to password
    if security_token:
        return Salesforce(username=username, password=password, security_token=security_token, domain=domain)
    else:
        # Fallback: assume token is appended to password
        return Salesforce(username=username, password=password, domain=domain)


def create_campaign(sf: Salesforce, name: str, **fields) -> str:
    """
    Create a Campaign. Returns the new Campaign Id.
    Pass any Campaign standard/custom fields as kwargs (e.g. Type, Status, Description).
    """
    payload = {"Name": name, **{k: v for k, v in fields.items() if v is not None}}
    result = sf.Campaign.create(payload)
    if not result.get("success"):
        raise RuntimeError(f"Salesforce Campaign.create failed: {result}")
    return result["id"]


def find_parent_campaign(sf: Salesforce, parent_name: str) -> Optional[str]:
    """
    Find a parent Campaign by name. Returns the Campaign Id if found, None otherwise.
    """
    # Escape single quotes in the name for SOQL (double them)
    escaped_name = parent_name.replace("'", "''")
    query = f"SELECT Id FROM Campaign WHERE Name = '{escaped_name}' LIMIT 1"
    result = sf.query(query)
    if result.get("records"):
        return result["records"][0]["Id"]
    return None


def create_campaign_member_status(
    sf: Salesforce, 
    campaign_id: str, 
    label: str, 
    sort_order: int,
    is_default: bool = False,
    has_responded: bool = False
) -> str:
    """
    Create a CampaignMemberStatus for a campaign.
    Returns the CampaignMemberStatus Id.
    Requires: Marketing User permissions
    """
    payload = {
        "CampaignId": campaign_id,
        "Label": label,
        "SortOrder": sort_order,
        "IsDefault": is_default,
        "HasResponded": has_responded,
    }
    result = sf.CampaignMemberStatus.create(payload)
    if not result.get("success"):
        raise RuntimeError(f"Salesforce CampaignMemberStatus.create failed: {result}")
    return result["id"]


def create_campaign_member_statuses(
    sf: Salesforce, 
    campaign_id: str, 
    statuses: list[str],
    default_status: Optional[str] = None
) -> dict[str, str]:
    """
    Create multiple CampaignMemberStatus records for a campaign.
    Returns dict mapping status label to CampaignMemberStatus Id.
    """
    created_statuses = {}
    # Default statuses "Sent" and "Responded" typically use sort orders 1 and 2
    # Start our custom statuses at 3
    start_sort_order = 3
    
    for idx, status_label in enumerate(statuses):
        sort_order = start_sort_order + idx
        is_default = (status_label == default_status) if default_status else False
        # Mark "Attended" and "Responded" as having responded
        has_responded = status_label.lower() in ["attended", "responded"]
        
        try:
            status_id = create_campaign_member_status(
                sf, campaign_id, status_label, sort_order, is_default, has_responded
            )
            created_statuses[status_label] = status_id
            print(f"  Created campaign member status '{status_label}' (id={status_id})")
        except Exception as e:
            # Check if status already exists
            error_msg = str(e).lower()
            if "duplicate" in error_msg or "already exists" in error_msg:
                print(f"  Campaign member status '{status_label}' already exists")
                # Try to find existing status
                escaped_label = status_label.replace("'", "''")
                query = f"SELECT Id, Label FROM CampaignMemberStatus WHERE CampaignId = '{campaign_id}' AND Label = '{escaped_label}' LIMIT 1"
                result = sf.query(query)
                if result.get("records"):
                    created_statuses[status_label] = result["records"][0]["Id"]
            else:
                print(f"  Warning: Failed to create status '{status_label}': {e}")
    
    return created_statuses


def add_campaign_members(sf: Salesforce, campaign_id: str, contact_ids: list[str]) -> list:
    """
    Add CampaignMembers (Contacts) to a campaign.
    contact_ids: list of Salesforce Contact Ids.
    Returns list of created CampaignMember ids.
    """
    created = []
    for cid in contact_ids:
        r = sf.CampaignMember.create(
            {"CampaignId": campaign_id, "ContactId": cid, "Status": "Sent"}
        )
        if r.get("success"):
            created.append(r["id"])
    return created
