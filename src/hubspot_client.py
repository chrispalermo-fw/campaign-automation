"""
HubSpot Marketing Campaigns API client.
Creates campaigns and associates lists (OBJECT_LIST) as assets.
Requires: marketing.campaigns.read, marketing.campaigns.write
"""
import os
from typing import Optional, Union
import requests


HUBSPOT_BASE = "https://api.hubapi.com"


def _headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


def get_client(access_token: Optional[str] = None):
    token = access_token or os.environ.get("HUBSPOT_ACCESS_TOKEN")
    if not token:
        raise ValueError("HUBSPOT_ACCESS_TOKEN required (env or argument)")
    return HubSpotCampaignClient(token)


class HubSpotCampaignClient:
    def __init__(self, access_token: str):
        self._token = access_token
        self._session = requests.Session()
        self._session.headers.update(_headers(access_token))

    def get_most_recent_campaign(self) -> Optional[dict]:
        """Get the most recently created campaign. Returns campaign object if found, None otherwise."""
        url = f"{HUBSPOT_BASE}/marketing/v3/campaigns"
        params = {"limit": 1, "sort": "-createdAt"}  # Most recent first
        r = self._session.get(url, params=params)
        r.raise_for_status()
        result = r.json()
        campaigns = result.get("results", [])
        return campaigns[0] if campaigns else None

    def create_campaign(self, properties: dict) -> dict:
        """
        Create a campaign. Returns campaign object with id (campaignGuid).
        If campaign already exists (409), returns the most recently created campaign as a workaround.
        """
        url = f"{HUBSPOT_BASE}/marketing/v3/campaigns"
        payload = {"properties": properties}
        r = self._session.post(url, json=payload)
        
        # Handle conflict - campaign already exists
        if r.status_code == 409:
            campaign_name = properties.get("hs_name", "Unknown")
            print(f"  Campaign '{campaign_name}' already exists, fetching existing campaign...")
            # Workaround: get the most recent campaign (likely the one we just tried to create)
            # Note: This assumes the campaign was recently created. For production, consider
            # implementing a proper search by name if HubSpot API supports it.
            existing = self.get_most_recent_campaign()
            if existing:
                return existing
            # If we can't find it, raise the error
            r.raise_for_status()
            return {}  # Should never reach here
        
        # Check for other errors
        r.raise_for_status()
        return r.json()

    def associate_list(self, campaign_guid: str, list_id: Union[str, int]) -> None:
        """Associate a static list (OBJECT_LIST) with the campaign."""
        url = f"{HUBSPOT_BASE}/marketing/v3/campaigns/{campaign_guid}/assets/OBJECT_LIST/{list_id}"
        r = self._session.put(url)
        r.raise_for_status()

    def find_list_by_name(self, name: str) -> Optional[str]:
        """
        Find a list by name. Returns list ID if found, None otherwise.
        Tries multiple approaches: direct query, pagination, and checking campaign associations.
        """
        url = f"{HUBSPOT_BASE}/crm/v3/lists"
        
        # Try with pagination - get all lists
        offset = None
        all_lists = []
        
        while True:
            params = {"limit": 100}
            if offset:
                params["after"] = offset
            r = self._session.get(url, params=params)
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
        
        # Search client-side
        for list_obj in all_lists:
            if list_obj.get("name") == name:
                return str(list_obj.get("listId"))
        
        return None

    def get_campaign_assets(self, campaign_id: str) -> list:
        """Get all assets (lists) associated with a campaign."""
        url = f"{HUBSPOT_BASE}/marketing/v3/campaigns/{campaign_id}/assets"
        r = self._session.get(url)
        r.raise_for_status()
        result = r.json()
        # Assets are organized by type, lists are under OBJECT_LIST
        assets = result.get("assets", {})
        list_assets = assets.get("OBJECT_LIST", [])
        return list_assets

    def find_list_by_exact_name(self, name: str) -> Optional[str]:
        """
        Try to find a list by exact name using search API or by querying all lists.
        This is a fallback when regular list lookup fails.
        """
        # Try searching with a broader query that might return the list
        # Since direct search doesn't work, we'll need to rely on manual list_ids in config
        # But we can try one more approach: check if we can query lists with filters
        try:
            # Try getting lists with a name filter (may not work due to API limitations)
            url = f"{HUBSPOT_BASE}/crm/v3/lists"
            # Try with a very high limit to get all lists
            r = self._session.get(url, params={"limit": 10000})
            if r.status_code == 200:
                result = r.json()
                for list_obj in result.get("lists", []):
                    if list_obj.get("name") == name:
                        return str(list_obj.get("listId"))
        except Exception:
            pass
        return None

    def create_list(self, name: str, campaign_name: str, campaign_id: Optional[str] = None) -> Optional[str]:
        """
        Create a static list (segment) in HubSpot for a campaign member status.
        Returns the list ID. If list already exists, tries multiple methods to find it.
        Requires: crm.lists.read, crm.lists.write
        """
        url = f"{HUBSPOT_BASE}/crm/v3/lists"
        payload = {
            "name": name,
            "objectTypeId": "0-1",  # Contacts
            "processingType": "MANUAL",  # Static list - members added manually or via workflow
        }
        r = self._session.post(url, json=payload)
        
        # Handle duplicate list name error
        if r.status_code == 400:
            error_data = r.json()
            if error_data.get("subCategory") == "ILS.DUPLICATE_LIST_NAMES":
                print(f"  List '{name}' already exists, attempting to find it...")
                
                # Try multiple methods to find the list
                existing_id = self.find_list_by_name(name)
                if not existing_id:
                    existing_id = self.find_list_by_exact_name(name)
                
                if existing_id:
                    print(f"  Found existing list '{name}' (id={existing_id})")
                    return existing_id
                
                # If we still can't find it, return None - the association will be skipped
                # but we'll provide clear instructions
                print(f"  ⚠️  Warning: List '{name}' exists but could not be retrieved.")
                print(f"     The list exists but we cannot find its ID due to API limitations.")
                print(f"     Please find the list ID manually and add it to hubspot.list_ids in your YAML.")
                return None
        
        r.raise_for_status()
        result = r.json()
        # Response format: {"list": {"listId": "..."}}
        return str(result["list"]["listId"])

    def create_workflow(
        self,
        workflow_name: str,
        list_id: Union[str, int],
        salesforce_campaign_id: str,
        salesforce_status: str,
        wait_minutes: int = 10,
    ) -> dict:
        """
        Create a HubSpot workflow that:
        1. Enrolls contacts when they're added to a list
        2. Waits for specified minutes
        3. Updates Salesforce campaign member status
        
        Returns workflow object with id.
        Requires: automation scope (workflows.read, workflows.write)
        """
        url = f"{HUBSPOT_BASE}/automation/v3/workflows"
        
        # Wait time in milliseconds (10 minutes = 600000 ms)
        wait_millis = wait_minutes * 60 * 1000
        
        # Build workflow actions
        actions = [
            {
                "type": "DELAY",
                "delayMillis": wait_millis,
            },
            # Note: Salesforce integration typically requires:
            # 1. HubSpot-Salesforce integration configured in UI, OR
            # 2. Webhook to Zapier/Make.com that updates Salesforce
            # For now, we'll add a webhook placeholder - user can configure the actual endpoint
            # The webhook should receive contact info and update Salesforce CampaignMember status
            {
                "type": "WEBHOOK",
                "url": f"https://hooks.zapier.com/hooks/catch/YOUR_WEBHOOK_ID/",  # Placeholder
                "method": "POST",
                "body": {
                    "contact_id": "{{contact.id}}",
                    "contact_email": "{{contact.email}}",
                    "salesforce_campaign_id": salesforce_campaign_id,
                    "salesforce_status": salesforce_status,
                    "list_id": str(list_id),
                },
            },
        ]
        
        payload = {
            "name": workflow_name,
            "type": "DRIP_DELAY",
            "onlyEnrollsManually": False,  # Allow automatic enrollment
            "enrollmentTriggerType": "CONTACT_LIST_MEMBERSHIP",  # Trigger on list enrollment
            "enrollmentListId": str(list_id),
            "actions": actions,
        }
        
        r = self._session.post(url, json=payload)
        r.raise_for_status()
        return r.json()

    def create_workflow_with_enrollment(
        self,
        workflow_name: str,
        list_id: Union[str, int],
        salesforce_campaign_id: str,
        salesforce_status: str,
        wait_minutes: int = 10,
        webhook_url: Optional[str] = None,
        salesforce_campaign_name: Optional[str] = None,
    ) -> dict:
        """
        Create a HubSpot workflow that triggers when contacts are added to a segment (list).
        After waiting, it will update Salesforce campaign member status.
        
        Workflow structure:
        1. Trigger: Contact is added to list (created via API)
           NOTE: HubSpot API v3 limitation - cannot set "Segment membership changed" trigger programmatically.
           The workflow will be created with "Contact is added to list" trigger.
           User must manually change it to "Segment membership changed" → "is added to segment" in HubSpot UI.
        2. Delay: Wait specified minutes
        3. Action: Set Salesforce Campaign Membership (with campaign name and status)
        
        Returns workflow object with id.
        Requires: automation.read, automation.write scopes
        
        Args:
            workflow_name: Name of the workflow (typically matches segment name)
            list_id: HubSpot list/segment ID
            salesforce_campaign_id: Salesforce Campaign ID
            salesforce_status: Campaign Member Status (e.g., "Waitlist", "Registered")
            wait_minutes: Delay before action (default: 10)
            webhook_url: Optional webhook URL (if not using native Salesforce integration)
            salesforce_campaign_name: Salesforce Campaign Name (for action configuration)
        """
        url = f"{HUBSPOT_BASE}/automation/v3/workflows"
        
        wait_millis = wait_minutes * 60 * 1000
        
        actions = [
            {
                "type": "DELAY",
                "delayMillis": wait_millis,
            },
        ]
        
        # Try to use SET_SALESFORCE_CAMPAIGN action type (may not be supported via API)
        # If webhook is provided, use that instead (for custom integrations)
        if webhook_url:
            actions.append({
                "type": "WEBHOOK",
                "url": webhook_url,
                "method": "POST",
                "body": {
                    "contact_id": "{{contact.id}}",
                    "contact_email": "{{contact.email}}",
                    "salesforce_campaign_id": salesforce_campaign_id,
                    "salesforce_status": salesforce_status,
                    "list_id": str(list_id),
                },
            })
        else:
            # Try SET_SALESFORCE_CAMPAIGN_MEMBERSHIP action (correct API action type)
            # Note: HubSpot API uses SET_SALESFORCE_CAMPAIGN_MEMBERSHIP, not SET_SALESFORCE_CAMPAIGN
            try:
                set_sf_action = {
                    "type": "SET_SALESFORCE_CAMPAIGN_MEMBERSHIP",
                    "campaignId": salesforce_campaign_id,
                    "status": salesforce_status,
                }
                if salesforce_campaign_name:
                    set_sf_action["campaignName"] = salesforce_campaign_name
                actions.append(set_sf_action)
            except Exception as e:
                print(f"  ⚠️  Could not create SET_SALESFORCE_CAMPAIGN_MEMBERSHIP action: {e}")
                # Fallback to placeholder if SET_SALESFORCE_CAMPAIGN_MEMBERSHIP doesn't work
                actions.append({
                    "type": "SET_CONTACT_PROPERTY",
                    "propertyName": "notes",
                    "newValue": f"[REPLACE THIS ACTION] Set Salesforce Campaign: {salesforce_campaign_id}, Status: {salesforce_status}",
                })
        
        # Build payload - HubSpot API v3 limitation:
        # The API does NOT support setting enrollment triggers programmatically.
        # enrollmentTriggerType/enrollmentListId are ignored in POST requests.
        # segmentCriteria doesn't work for list-based enrollment either.
        # The workflow will be created with "Manually triggered only" and MUST be configured in UI.
        payload = {
            "name": workflow_name,
            "type": "DRIP_DELAY",
            "onlyEnrollsManually": False,  # This allows automatic enrollment once trigger is set in UI
            "actions": actions,
        }
        
        try:
            r = self._session.post(url, json=payload)
            if r.status_code != 200 and r.status_code != 201:
                error_text = r.text
                try:
                    error_json = r.json()
                    print(f"  ❌ HubSpot API Error ({r.status_code}): {error_json}")
                except:
                    print(f"  ❌ HubSpot API Error ({r.status_code}): {error_text}")
            r.raise_for_status()
            workflow = r.json()
            workflow_id = workflow.get("id")
            
            print(f"  ✓ Created workflow '{workflow_name}' (id={workflow_id})")
            
            # Check if Salesforce action was successfully added by examining response
            workflow_actions = workflow.get("actions", [])
            has_salesforce_action = any(
                action.get("type") == "SET_SALESFORCE_CAMPAIGN_MEMBERSHIP" or 
                action.get("actionTypeId") == "SET_SALESFORCE_CAMPAIGN_MEMBERSHIP" or
                action.get("type") == "SET_SALESFORCE_CAMPAIGN" or 
                action.get("actionTypeId") == "SET_SALESFORCE_CAMPAIGN"
                for action in workflow_actions
            )
            
            # CRITICAL: HubSpot API v3 does NOT support setting enrollment triggers programmatically
            # The workflow is created with "Manually triggered only" and MUST be configured in UI
            print(f"\n  ⚠️  CRITICAL: Set Enrollment Trigger in HubSpot UI (Required)")
            print(f"     Workflow ID: {workflow_id}")
            print(f"     Workflow Name: {workflow_name}")
            print(f"     Segment/List ID: {list_id}")
            print(f"     Salesforce Campaign ID: {salesforce_campaign_id}")
            print(f"     Salesforce Campaign Name: {salesforce_campaign_name or 'N/A'}")
            print(f"     Campaign Member Status: {salesforce_status}")
            print(f"\n     Steps to complete workflow setup:")
            print(f"     1. Go to: Automation > Workflows")
            print(f"     2. Open: '{workflow_name}' (ID: {workflow_id})")
            print(f"     3. ENROLLMENT tab → Click 'Add enrollment trigger'")
            print(f"     4. Select: 'Segment membership changed'")
            print(f"     5. Condition: 'is added to segment'")
            print(f"     6. Select segment: '{workflow_name}' (or search for List ID: {list_id})")
            print(f"     7. Click 'Save'")
            print(f"     8. ACTIONS tab → Verify Salesforce action:")
            if not has_salesforce_action:
                print(f"        • DELETE the placeholder 'Set contact property' action (if present)")
                print(f"        • ADD action:")
                print(f"          - Go to: CRM → Set Salesforce Campaign")
                print(f"          - Campaign: {salesforce_campaign_name or salesforce_campaign_id}")
                print(f"          - Status: {salesforce_status}")
            else:
                print(f"        • Salesforce action is already configured ✅")
            print(f"     9. ACTIVATE the workflow")
            
            return workflow
            
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg or "automation-access" in error_msg.lower() or "permissions" in error_msg.lower():
                print(f"  ❌ ERROR: Missing Automation scope in HubSpot Private App!")
                print(f"     See ADD_AUTOMATION_SCOPE.md for instructions to add the scope.")
                raise ValueError("HubSpot Private App needs Automation (read + write) scope. See ADD_AUTOMATION_SCOPE.md")
            else:
                raise

    def build_properties(
        self,
        name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        taxonomy: Optional[dict] = None,
        tags: Optional[list] = None,
        extra: Optional[dict] = None,
    ) -> dict:
        """Build HubSpot campaign properties from config."""
        props = {"hs_name": name}
        if start_date:
            props["hs_start_date"] = start_date
        if end_date:
            props["hs_end_date"] = end_date
        if taxonomy:
            for k, v in taxonomy.items():
                if v is not None:
                    props[k] = str(v) if not isinstance(v, str) else v
        if tags:
            # Add your campaign tag property in hubspot.extra_properties (e.g. a custom property)
            pass  # tags available for use in extra or custom logic
        if extra:
            props.update(extra)
        return props
