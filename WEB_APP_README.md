# Campaign Automation Web App

A user-friendly web interface for creating campaigns in HubSpot and Salesforce.

## Features

- 📝 **Simple Form Interface** - Fill out a form instead of editing YAML files
- 🚀 **One-Click Campaign Creation** - Creates campaigns, segments, and workflows automatically
- ✅ **Real-time Results** - See campaign IDs and workflow information immediately
- 🎨 **Modern UI** - Clean, responsive design that works on all devices

## Quick Start

### 1. Install Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate

# Install Flask (if not already installed)
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Make sure your `.env` file has all required credentials:
- `HUBSPOT_ACCESS_TOKEN`
- `SALESFORCE_USERNAME`
- `SALESFORCE_PASSWORD`
- `SALESFORCE_SECURITY_TOKEN`

### 3. Run the Web App

```bash
python app.py
```

The app will start on `http://localhost:5000`

### 4. Open in Browser

Navigate to: **http://localhost:5000**

## Usage

1. **Fill out the form:**
   - Campaign name, dates, and basic info
   - Member statuses (one per line: Registered, Waitlist, Attended, No Show)
   - HubSpot and Salesforce configuration
   - Workflow settings

2. **Submit the form:**
   - The app will create everything automatically
   - You'll see a results page with campaign IDs and workflow information

3. **Complete workflow setup:**
   - Follow the instructions on the results page
   - Configure enrollment triggers in HubSpot UI
   - Add "Set Salesforce Campaign" actions
   - Activate workflows

## Form Fields Explained

### Required Fields

- **Campaign Name**: Format `Type_name_Location_Date` (e.g., `1PEvent_GTC Nvidia Afterparty_San Jose_03162026`)
- **Start Date / End Date**: Campaign dates
- **Member Statuses**: One per line (e.g., Registered, Waitlist, Attended, No Show)

### Optional Fields

- **HubSpot Notes**: Additional notes for the HubSpot campaign
- **Salesforce Status**: Campaign status (default: Planned)
- **Salesforce Description**: Campaign description
- **Salesforce Type**: Campaign type (e.g., Event, Webinar)
- **Parent Campaign**: Name of parent campaign if this is a child campaign
- **Wait Time**: Minutes to wait before syncing to Salesforce (default: 10)
- **Webhook URL**: Zapier webhook URL if using webhook-based sync

## Production Deployment

For production use, you should:

1. **Set a secure secret key:**
   ```bash
   export FLASK_SECRET_KEY="your-secure-random-key-here"
   ```

2. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up HTTPS** (use a reverse proxy like nginx)

4. **Add authentication** (consider Flask-Login or similar)

## Troubleshooting

### "Missing environment variables" warning
- Make sure your `.env` file is in the project root
- Check that all required variables are set

### Campaign creation fails
- Verify your HubSpot and Salesforce credentials are correct
- Check that you have the required API scopes/permissions
- Review the error message for specific issues

### Workflows not appearing
- Make sure Automation scope is enabled in HubSpot Private App
- Check the results page for workflow IDs
- Workflows may need manual configuration in HubSpot UI

## API Endpoints

- `GET /` - Main form page
- `POST /create` - Process form and create campaign
- `GET /health` - Health check endpoint

## Next Steps After Campaign Creation

After creating a campaign via the web app:

1. **Configure Workflow Enrollment Triggers** (in HubSpot UI)
2. **Add "Set Salesforce Campaign" Actions** (in HubSpot UI)
3. **Activate Workflows** (in HubSpot UI)

See `CONFIGURE_WORKFLOWS.md` for detailed instructions.
