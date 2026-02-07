"""
Webhook server for HubSpot form submissions.
HubSpot landing page form → Webhook → Campaign creation
"""
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from src.run_campaign import run as run_campaign
import tempfile
import yaml
import logging

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS support
from flask_cors import CORS
CORS(app)


def hubspot_form_to_config(form_data):
    """Convert HubSpot form submission data to campaign config dictionary."""
    # HubSpot sends form data in different formats depending on setup
    # Handle both direct form fields and nested data
    
    # Extract form fields (HubSpot may send as form_data or nested)
    if isinstance(form_data, dict):
        # Direct field access
        # Support both naming conventions: campaign_* and standard names
        campaign_name = form_data.get("campaign_name") or form_data.get("campaignname")
        start_date = (form_data.get("campaign_start_date") or 
                     form_data.get("start_date") or 
                     form_data.get("startdate"))
        end_date = (form_data.get("campaign_end_date") or 
                   form_data.get("end_date") or 
                   form_data.get("enddate"))
        member_statuses_raw = (form_data.get("campaign_member_statuses") or 
                              form_data.get("member_statuses") or 
                              form_data.get("memberstatuses") or "")
        salesforce_status = form_data.get("salesforce_status") or form_data.get("salesforcestatus") or "Planned"
        salesforce_description = form_data.get("salesforce_description") or form_data.get("salesforcedescription") or ""
        salesforce_type = form_data.get("salesforce_type") or form_data.get("salesforcetype") or ""
        parent_campaign = form_data.get("parent_campaign") or form_data.get("parentcampaign") or ""
        hubspot_notes = form_data.get("hubspot_notes") or form_data.get("hubspotnotes") or ""
        wait_minutes = form_data.get("wait_minutes") or form_data.get("waitminutes") or "10"
        webhook_url = form_data.get("webhook_url") or form_data.get("webhookurl") or ""
    else:
        # Handle as form data object
        # Support both naming conventions: campaign_* and standard names
        campaign_name = getattr(form_data, "campaign_name", None) or getattr(form_data, "campaignname", None)
        start_date = (getattr(form_data, "campaign_start_date", None) or 
                     getattr(form_data, "start_date", None) or 
                     getattr(form_data, "startdate", None))
        end_date = (getattr(form_data, "campaign_end_date", None) or 
                   getattr(form_data, "end_date", None) or 
                   getattr(form_data, "enddate", None))
        member_statuses_raw = (getattr(form_data, "campaign_member_statuses", None) or 
                               getattr(form_data, "member_statuses", None) or 
                               getattr(form_data, "memberstatuses", None) or "")
        salesforce_status = getattr(form_data, "salesforce_status", None) or getattr(form_data, "salesforcestatus", None) or "Planned"
        salesforce_description = getattr(form_data, "salesforce_description", None) or getattr(form_data, "salesforcedescription", None) or ""
        salesforce_type = getattr(form_data, "salesforce_type", None) or getattr(form_data, "salesforcetype", None) or ""
        parent_campaign = getattr(form_data, "parent_campaign", None) or getattr(form_data, "parentcampaign", None) or ""
        hubspot_notes = getattr(form_data, "hubspot_notes", None) or getattr(form_data, "hubspotnotes", None) or ""
        wait_minutes = getattr(form_data, "wait_minutes", None) or getattr(form_data, "waitminutes", None) or "10"
        webhook_url = getattr(form_data, "webhook_url", None) or getattr(form_data, "webhookurl", None) or ""
    
    # Clean and validate
    campaign_name = (campaign_name or "").strip()
    start_date = (start_date or "").strip()
    end_date = (end_date or "").strip()
    
    if not campaign_name or not start_date or not end_date:
        raise ValueError("Missing required fields: campaign_name, campaign_start_date (or start_date), campaign_end_date (or end_date)")
    
    # Parse member statuses (handle newlines, commas, or semicolons)
    member_statuses = []
    if member_statuses_raw:
        # Replace various separators with newlines, then split
        cleaned = member_statuses_raw.replace(",", "\n").replace(";", "\n")
        member_statuses = [s.strip() for s in cleaned.split("\n") if s.strip()]
    
    if not member_statuses:
        raise ValueError("Missing required field: campaign_member_statuses (or member_statuses)")
    
    # Build config
    config = {
        "name": campaign_name,
        "start_date": start_date,
        "end_date": end_date,
        "taxonomy": {
            "hubspot": {},
            "salesforce": {},
        },
        "hubspot": {
            "auto_create_segments": member_statuses,
            "create_workflows": True,
            "extra_properties": {},
        },
        "salesforce": {
            "status": salesforce_status.strip() if salesforce_status else "Planned",
            "description": salesforce_description.strip() if salesforce_description else "",
            "member_statuses": member_statuses,
        },
        "workflows": {
            "wait_minutes": int(wait_minutes) if wait_minutes.isdigit() else 10,
        },
    }
    
    # Add optional fields
    if salesforce_type:
        config["taxonomy"]["salesforce"]["Type"] = salesforce_type.strip()
    
    if parent_campaign:
        config["salesforce"]["parent_campaign"] = parent_campaign.strip()
    
    if hubspot_notes:
        config["hubspot"]["extra_properties"]["hs_notes"] = hubspot_notes.strip()
    
    if webhook_url:
        config["workflows"]["zapier_webhook_url"] = webhook_url.strip()
    
    return config


@app.route("/webhook/campaign-create", methods=["POST"])
def webhook_campaign_create():
    """
    Webhook endpoint for HubSpot form submissions.
    Expects JSON or form data with campaign creation fields.
    """
    try:
        # Get data from request
        if request.is_json:
            data = request.json
        else:
            data = request.form.to_dict()
        
        logger.info(f"Received webhook request: {data}")
        
        # Convert to config
        config = hubspot_form_to_config(data)
        
        # Create temporary YAML file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            temp_path = f.name
        
        try:
            # Run campaign creation
            result = run_campaign(temp_path)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            logger.info(f"Campaign created successfully: {result}")
            
            # Return success response
            return jsonify({
                "status": "success",
                "message": "Campaign created successfully",
                "data": {
                    "campaign_name": result.get("campaign_name"),
                    "hubspot_campaign_id": result.get("hubspot_campaign_id"),
                    "salesforce_campaign_id": result.get("salesforce_campaign_id"),
                    "hubspot_list_ids": result.get("hubspot_list_ids", []),
                    "hubspot_workflows": result.get("hubspot_workflows", []),
                }
            }), 200
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e
            
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
        
    except Exception as e:
        logger.exception("Campaign creation failed")
        return jsonify({
            "status": "error",
            "message": f"Failed to create campaign: {str(e)}"
        }), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Check required environment variables
    required_vars = ["HUBSPOT_ACCESS_TOKEN", "SALESFORCE_USERNAME", "SALESFORCE_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
    
    port = int(os.environ.get("PORT", 5000))
    # Disable debug in production
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)
