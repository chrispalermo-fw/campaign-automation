# Salesforce Authentication Troubleshooting

## Current Issue: Authentication Failed (invalid_grant)

### Quick Fixes to Try:

#### 1. Check Connected App IP Relaxation Settings

1. Go to **Setup** → **App Manager**
2. Find **Campaign Automation Tool**
3. Click the dropdown (▼) → **Edit**
4. Scroll to **OAuth Policies** section
5. Find **IP Relaxation**:
   - Set to: **Relax IP restrictions** ✅
6. Click **Save**

#### 2. Check Connected App Activation

- Connected Apps can take 2-10 minutes to fully activate
- Wait a few minutes and try again
- You can check if it's active by looking at the Connected App detail page

#### 3. Verify OAuth Scopes

Make sure your Connected App has these scopes:
- ✅ `Access and manage your data (api)`
- ✅ `Perform requests on your behalf at any time (refresh_token, offline_access)`

#### 4. Try with Security Token (if IP restrictions are strict)

If your org has strict IP restrictions, you might need to append your security token to your password:

1. **Get your Security Token:**
   - Go to your profile (top right) → **Settings**
   - **My Personal Information** → **Reset My Security Token**
   - Click **Reset Security Token**
   - Check your email for the token

2. **Append token to password:**
   - If your password is: `Welovebrunoluna143!`
   - And your security token is: `ABC123XYZ`
   - Use: `Welovebrunoluna143!ABC123XYZ`

3. **Update .env file** with the combined password+token

#### 5. Check Permitted Users

In Connected App settings:
- **Permitted Users**: Should be "All users may self-authorize" (for testing)
- Or make sure your user is in the approved list

---

## Test After Making Changes

After updating settings, wait 2-3 minutes, then test:

```bash
python -m src.run_campaign config/campaigns/gtc-nvidia-afterparty.yaml
```

---

## Still Not Working?

If none of the above works, we can:
1. Try using username/password + security token method (simpler, no Connected App needed)
2. Check if there are any org-level IP restrictions
3. Verify your user has API access enabled
