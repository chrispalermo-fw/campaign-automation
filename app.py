"""
Flask web application for campaign automation.
Provides a user-friendly form interface for creating campaigns in HubSpot and Salesforce.
"""
import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from dotenv import load_dotenv
from src.run_campaign import run as run_campaign
import tempfile
import yaml
from pathlib import Path

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")


def form_to_config(form_data):
    """Convert form data to campaign config dictionary."""
    config = {
        "name": form_data.get("campaign_name", "").strip(),
        "start_date": form_data.get("start_date", "").strip(),
        "end_date": form_data.get("end_date", "").strip(),
        "taxonomy": {
            "hubspot": {},
            "salesforce": {},
        },
        "hubspot": {
            "auto_create_segments": [],
            "create_workflows": form_data.get("create_workflows") == "true",
            "extra_properties": {},
        },
        "salesforce": {
            "status": form_data.get("salesforce_status", "Planned").strip(),
            "description": form_data.get("salesforce_description", "").strip(),
            "member_statuses": [],
        },
        "workflows": {
            "wait_minutes": int(form_data.get("wait_minutes", 10)),
        },
    }
    
    # Parse member statuses (comma-separated or checkboxes)
    member_statuses_input = form_data.get("member_statuses", "")
    if member_statuses_input:
        # Handle comma-separated or newline-separated
        statuses = [s.strip() for s in member_statuses_input.replace("\n", ",").split(",") if s.strip()]
        config["hubspot"]["auto_create_segments"] = statuses
        config["salesforce"]["member_statuses"] = statuses
    
    # Parse Salesforce taxonomy fields
    sf_type = form_data.get("salesforce_type", "").strip()
    if sf_type:
        config["taxonomy"]["salesforce"]["Type"] = sf_type
    
    # Parse parent campaign
    parent_campaign = form_data.get("parent_campaign", "").strip()
    if parent_campaign:
        config["salesforce"]["parent_campaign"] = parent_campaign
    
    # Parse HubSpot extra properties
    hs_notes = form_data.get("hubspot_notes", "").strip()
    if hs_notes:
        config["hubspot"]["extra_properties"]["hs_notes"] = hs_notes
    
    # Parse webhook URL
    webhook_url = form_data.get("webhook_url", "").strip()
    if webhook_url:
        config["workflows"]["zapier_webhook_url"] = webhook_url
    
    return config


@app.route("/")
def index():
    """Render the main campaign creation form."""
    return render_template("index.html")


@app.route("/create", methods=["POST"])
def create_campaign():
    """Process the form submission and create the campaign."""
    try:
        # Validate required fields
        required_fields = ["campaign_name", "start_date", "end_date"]
        missing_fields = [field for field in required_fields if not request.form.get(field)]
        
        if missing_fields:
            flash(f"Missing required fields: {', '.join(missing_fields)}", "error")
            return redirect(url_for("index"))
        
        # Convert form to config
        config = form_to_config(request.form)
        
        # Validate member statuses
        if not config["hubspot"]["auto_create_segments"]:
            flash("Please provide at least one member status (e.g., Registered, Attended)", "error")
            return redirect(url_for("index"))
        
        # Create temporary YAML file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            temp_path = f.name
        
        try:
            # Run campaign creation
            result = run_campaign(temp_path)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            # Render results page
            return render_template("results.html", result=result, config=config)
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e
            
    except Exception as e:
        flash(f"Error creating campaign: {str(e)}", "error")
        app.logger.exception("Campaign creation failed")
        return redirect(url_for("index"))


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # Check if required environment variables are set
    required_vars = ["HUBSPOT_ACCESS_TOKEN", "SALESFORCE_USERNAME", "SALESFORCE_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("   Campaign creation may fail. Make sure your .env file is configured.")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
