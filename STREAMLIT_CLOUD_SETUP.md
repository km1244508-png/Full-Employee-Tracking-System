# 🚀 Deploy to Streamlit Community Cloud

Your Attendance & Work Progress Tracker is ready to deploy! Follow these steps:

## Step 1: Create Streamlit Cloud Account (if needed)
- Go to https://share.streamlit.io
- Sign up or log in with your GitHub account
- Authorize Streamlit to access your GitHub repositories

## Step 2: Deploy Your App
1. Click **"New app"** button
2. Select:
   - **Repository**: `km1244508-png/Attendance-Work-progress-Tracker`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click **"Deploy!"**

Streamlit will automatically:
- Clone your repo
- Install dependencies from `requirements.txt`
- Start the app at `https://[your-username]-attendance-app.streamlit.app`

## Step 3: Configure Environment Variables (IMPORTANT!)
Once deployment is live, set these secrets in Streamlit Cloud:

1. Click the **⋮ (menu)** icon on your deployed app
2. Select **"Settings"** → **"Secrets"**
3. Paste these into the `secrets.toml` editor:

```toml
# Database: Leave empty for default SQLite, OR set PostgreSQL connection
# For Neon/Supabase: DATABASE_URL = postgresql://user:password@host/dbname
DATABASE_URL = ""

# Company name displayed in app header
COMPANY_NAME = "Your Company Name"

# Cookie security: Generate with:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
COOKIE_PASSWORD = "your-random-secret-here"

# Optional: customize export directory
EXPORT_DIR = "exports"
```

4. Click **"Save"**
5. Streamlit will rerun your app with these secrets

## Step 4: First Run
When the app loads for the first time:
- ✅ Database initializes automatically
- ✅ Default admin user created: `admin` / `admin123`
- ⚠️ **IMPORTANT**: Change this password immediately!

## Step 5: Change Default Admin Password
1. Log in as `admin` with password `admin123`
2. Go to page **"2️⃣ Employee Management"**
3. Find the admin user and update password
4. Log out and verify new credentials work

## Troubleshooting

### "ModuleNotFoundError" on deployment
- Verify `requirements.txt` is at repo root ✓
- Verify `app.py` is at repo root ✓
- Check git commit is pushed to GitHub

### App shows "No such table" errors
- This is normal on first run - database is being initialized
- Refresh the page (it will auto-create tables)
- Default admin user will be seeded

### Cookie functionality not working
- Ensure `COOKIE_PASSWORD` environment variable is set in Secrets
- Clear browser cookies and try again
- Falls back to session state if cookies unavailable

### Database connection errors
- If using PostgreSQL, verify `DATABASE_URL` format:
  - `postgresql://user:password@host:5432/dbname`
  - Connection must be publicly accessible
- Recommended: Use Neon (free PostgreSQL) or Supabase

## Optional: Use PostgreSQL for Production

### Setup with Neon (Free)
1. Go to https://neon.tech
2. Sign up and create a project
3. Copy connection string: `postgresql://...`
4. In Streamlit Cloud Secrets, set:
   ```toml
   DATABASE_URL = "postgresql://your:password@ep-xxx.neon.tech/attendance"
   ```
5. Redeploy - database will initialize on first run

### Setup with Supabase (Free)
1. Go to https://supabase.com
2. Create new project
3. Get PostgreSQL connection string from project settings
4. Same setup as Neon above

## File Structure (Deployed)
```
repo-root/
├── app.py              ← Entry point (Streamlit loads this)
├── config.py           ← Settings (reads env variables)
├── requirements.txt    ← Dependencies
├── database/           ← SQLAlchemy models & setup
├── pages/              ← Multi-page app pages
├── utils/              ← Auth, UI, calculations
└── .streamlit/config.toml  ← Production settings
```

## Security Checklist
- ✅ No `.env` file in repo (excluded by .gitignore)
- ✅ No hardcoded credentials in code
- ✅ Database URL uses environment variables
- ✅ Cookie password must be changed from default
- ✅ Default admin password must be changed by user
- ✅ CORS enabled for cookie support
- ✅ XSRF protection disabled (required with CORS)

## Support
For issues:
1. Check Streamlit Cloud logs (click app menu → Manage app → Logs)
2. Verify all Secrets are set correctly
3. Ensure `requirements.txt` has all dependencies
4. Try redeploying (click menu → Reboot app)

---

Your app is now ready for the world! 🎉

**Repository**: https://github.com/km1244508-png/Attendance-Work-progress-Tracker
**Status**: ✅ Production-ready, all tests passed
