# Campaign Automation Tool — Project Plan

## Objective

Create a better way to automate the campaign creation and execution process across HubSpot, Salesforce, Luma (for events with pre-registration), and Zapier.

---

## Key Systems

| System    | Role |
|-----------|------|
| **Salesforce** | Campaign shell, campaign members, member statuses |
| **HubSpot**    | Campaign shell, segments (one per member status), workflows to sync to Salesforce |
| **Luma**       | Pre-registration for events only |
| **Zapier**     | Workflows to move data between systems |

---

## Campaign Creation Flow

### HubSpot

1. **Make campaign shell**
   - **Required:** Campaign Name (taxonomy: `Type_name_Location_Date`)
   - Set taxonomy on campaign
2. **Set up segments**
   - Create **one segment per Campaign Member Status** in Salesforce:
     - Registered  
     - Attended  
     - No Show  
     - Hot Lead  
     - Waitlist  
   - *(Optional: Responded — your plan listed it under SF members; include if you use it.)*
3. **Add segments to campaign shell**
   - Associate each segment (list) with the campaign as assets
4. **Set up workflow**
   - Workflow sends segment membership into Salesforce as campaign members (with correct status)

### Salesforce

1. **Make campaign shell**
   - **Required**
     - Campaign Name (same taxonomy: `Type_name_Location_Date`)
     - **Active** = `true`
     - **Start Date** / **End Date**
   - **Optional**
     - Parent Campaign  
     - Type  
     - Attribution Source  
     - Description  
2. **Campaign Members**
   - Optional at creation; populated by workflow from HubSpot
   - For each member: **Responded** (Y/N) and **Status**
   - **Status values:** Registered, No Show, Hot Lead, Attended, Waitlist (and Responded if used)

---

## Taxonomy Convention

**Format:** `Type_name_Location_Date`

- **Type** — e.g. `1PEvent`, `Webinar`
- **name** — Campaign/event name
- **Location** — e.g. San Jose
- **Date** — e.g. `03162026` (MMDDYYYY)

**Example:** `1PEvent_GTC Nvidia Afterparty_San Jose_03162026`

---

## Example Campaign (Reference)

### Parent campaign (Salesforce)

- **Name:** `GTV Nvidia 3/6/2026`  
  *(Assumed typo: 3/6/206 → 3/6/2026.)*

### Child campaign

- **Campaign Name:** `1PEvent_GTC Nvidia Afterparty_San Jose_03162026`
- **Create in:** HubSpot and Salesforce

**Salesforce-only fields**

| Field              | Value     |
|--------------------|-----------|
| Active             | Yes       |
| Campaign Type      | Event     |
| Attribution Source | Marketing |
| Start Date         | 3/16/2026 |
| End Date           | 3/16/2026 |
| Parent Campaign    | GTV Nvidia 3/6/2026 |

**Member statuses (segments in HubSpot ↔ campaign member status in Salesforce)**

- Registered  
- Waitlist  
- Attended  
- No Show  

*(Hot Lead and Responded can be added to the standard set if needed.)*

---

## Requirements Summary (Checklist)

- [ ] Tool creates campaign in **HubSpot** with name and taxonomy
- [ ] Tool creates campaign in **Salesforce** with name, Active=true, dates, Type, Attribution Source, optional Parent
- [ ] Tool creates **one HubSpot list (segment) per member status** (Registered, Attended, No Show, Hot Lead, Waitlist)
- [ ] Tool **associates those lists with the HubSpot campaign**
- [ ] Workflow (Zapier/HubSpot) **sends list membership to Salesforce as campaign members** with correct status
- [ ] Config supports **parent campaign** (name or Id) for Salesforce
- [ ] Taxonomy format **Type_name_Location_Date** is the single naming standard

---

## Feedback & Notes

1. **Parent campaign:** Plan assumes the parent (e.g. “GTV Nvidia 3/6/2026”) already exists in Salesforce; the tool will look it up by name and set `ParentCampaignId` on the child. If the parent should be created by the tool, we can add that.
2. **Responded vs status:** You listed “Responded” as a member field (Y/N) and also statuses like Registered, Attended. The tool will support both: a Responded flag on CampaignMember and Status for the five (or six) values.
3. **Luma:** Not in scope for this phase; can be added when you’re ready for event pre-registration flows.
4. **Date format:** Using YYYY-MM-DD in config (e.g. `2026-03-16`); the tool can output or display as 3/16/2026 where needed.

---

## Where This Lives

- **Project:** `/Users/chris/Documents/campaign-automation/`
- **Campaign configs:** `config/campaigns/*.yaml`
- **Example campaign:** `config/campaigns/gtc-nvidia-afterparty.yaml` (created by the tooling work)
