# How to Get Your GitHub Personal Access Token

Follow these steps to create a GitHub Personal Access Token:

---

## Step 1: Go to GitHub Token Settings

1. Go to: **https://github.com/settings/tokens**
2. Or navigate manually:
   - Click your profile picture (top right)
   - Click **"Settings"**
   - In the left sidebar, click **"Developer settings"**
   - Click **"Personal access tokens"**
   - Click **"Tokens (classic)"**

---

## Step 2: Generate New Token

1. Click **"Generate new token"** dropdown
2. Select **"Generate new token (classic)"**

---

## Step 3: Configure Token

1. **Note** (name for your token): `Railway Deployment` (or any name you prefer)

2. **Expiration**: Choose how long the token should last
   - Recommended: **90 days** or **No expiration** (for production use)

3. **Select scopes**: Check these boxes:
   - ✅ **`repo`** - Full control of private repositories
     - This includes: `repo:status`, `repo_deployment`, `public_repo`, `repo:invite`, `security_events`
   - ✅ **`workflow`** - Update GitHub Action workflows (optional, but good to have)

4. Scroll down and click **"Generate token"**

---

## Step 4: Copy Your Token

⚠️ **IMPORTANT**: GitHub will show your token **ONCE**. Copy it immediately!

1. You'll see a page with your token (starts with `ghp_` or `github_pat_`)
2. **Copy the entire token** - it's long!
3. **Save it somewhere safe** (password manager, notes app, etc.)
4. You won't be able to see it again after you leave this page

---

## Step 5: Use Token to Push

Now use this token as your password when pushing:

```bash
cd /Users/chris/Documents/campaign-automation
git push -u origin main
```

When prompted:
- **Username**: `chrispalermo-fw`
- **Password**: Paste your new token (not your GitHub password!)

---

## Token Format

Your token will look like one of these:
- `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (new format)
- `github_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (classic format)

Both work the same way!

---

## Troubleshooting

### "Permission denied" error
- Make sure you selected the `repo` scope
- Make sure you copied the entire token (no spaces)
- Try creating a new token if the old one doesn't work

### "Token expired" error
- Create a new token with longer expiration
- Or set expiration to "No expiration"

### Can't find "Developer settings"
- Make sure you're logged into GitHub
- Go directly to: https://github.com/settings/tokens

---

## Security Tips

- ✅ Store tokens securely (password manager)
- ✅ Use different tokens for different purposes
- ✅ Revoke old tokens you're not using
- ✅ Set expiration dates for security
- ❌ Never commit tokens to git repositories
- ❌ Never share tokens publicly

---

## Quick Link

Direct link to create token: **https://github.com/settings/tokens/new**
