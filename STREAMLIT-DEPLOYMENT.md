# 🚀 Streamlit Cloud Deployment Guide for MailBuddy

## YES! This project will work on Streamlit Cloud ✅

Your MailBuddy app is **100% compatible** with Streamlit Cloud deployment.

---

## 📋 Pre-Deployment Checklist

### ✅ What's Already Done
- [x] `.gitignore` properly configured
- [x] `requirements.txt` with all dependencies
- [x] Secrets handling via `st.secrets`
- [x] No hardcoded credentials in code
- [x] All relative imports working

### ⚠️ Before You Push to GitHub

1. **DO NOT commit these files** (already in .gitignore):
   - `.venv/` folder
   - `data/known_contacts.json`
   - `.streamlit/secrets.toml`
   - Any `.env` files

2. **Verify .gitignore is working:**
```powershell
git status
```
Make sure no sensitive files appear!

---

## 🔑 Streamlit Cloud Secrets Configuration

### Step 1: Get Your Credentials

You need **3 things**:

#### 1. **Gmail App Password**
- Go to: https://myaccount.google.com/security
- Enable "2-Step Verification"
- Go to "App passwords"
- Create new: "Mail" → "Other (MailBuddy)"
- Copy the 16-character password (remove spaces)

#### 2. **Google Gemini API Key**
- Go to: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy the API key

#### 3. **Your Gmail Address**
- The email you want to use for sending/receiving

---

### Step 2: Streamlit Cloud Secrets Format

In Streamlit Cloud dashboard, go to:
**App Settings → Secrets**

Paste this **EXACT FORMAT** (replace with your values):

```toml
# Google Gemini API Configuration
GOOGLE_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Email Configuration - IMAP (Receiving)
SENDER_EMAIL = "your.email@gmail.com"
EMAIL_PASSWORD = "abcd efgh ijkl mnop"

# Email Configuration - SMTP (Sending)
# Usually same as IMAP settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

### ⚠️ IMPORTANT NOTES:

1. **Keep the double quotes** around values
2. **App Password**: Include spaces exactly as shown by Google (e.g., "abcd efgh ijkl mnop")
3. **Email**: Use your full Gmail address
4. **API Key**: Copy entire key including any special characters
5. **No extra spaces** before/after `=`

---

## 🔧 Example Secrets Configuration

### ✅ CORRECT Format:

```toml
GOOGLE_API_KEY = "AIzaSyB1234567890abcdefghijklmnopqrstuv"
SENDER_EMAIL = "mailbuddy.demo@gmail.com"
EMAIL_PASSWORD = "wxyz abcd efgh ijkl"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

### ❌ WRONG Formats:

```toml
# Missing quotes
GOOGLE_API_KEY = AIzaSyB1234567890abcdefghijklmnopqrstuv

# Extra spaces
GOOGLE_API_KEY =    "AIzaSyB1234567890"   

# Wrong quote type
GOOGLE_API_KEY = 'AIzaSyB1234567890'

# Password without spaces removed (Google shows them)
EMAIL_PASSWORD = "wxyzabcdefghijkl"  # Wrong - needs spaces!
```

---

## 📤 GitHub Upload Steps

### Step 1: Initialize Git (if not done)

```powershell
cd "C:\Users\abhey\OneDrive\Desktop\MAILBUDDY"
git init
```

### Step 2: Add Files

```powershell
git add .
```

### Step 3: Verify No Secrets

```powershell
git status
```

**Check output - should NOT see:**
- `.venv/`
- `data/known_contacts.json`
- `.streamlit/` folder
- Any password files

**Should see:**
- `main.py`
- `requirements.txt`
- `agents/` folder
- `utils/` folder
- `docs/` folder
- `README.md`
- etc.

### Step 4: Commit

```powershell
git commit -m "Initial commit: MailBuddy email automation system"
```

### Step 5: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `MailBuddy`
3. Description: "Automated email management with AI-powered responses"
4. **Keep it Private** (recommended) or Public
5. **DO NOT** initialize with README (you already have one)
6. Click "Create repository"

### Step 6: Push to GitHub

```powershell
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/MailBuddy.git
git branch -M main
git push -u origin main
```

---

## 🌐 Streamlit Cloud Deployment Steps

### Step 1: Sign in to Streamlit Cloud

1. Go to: https://share.streamlit.io/
2. Sign in with GitHub account
3. Authorize Streamlit to access your repositories

### Step 2: Create New App

1. Click **"New app"**
2. Select your repository: `YOUR_USERNAME/MailBuddy`
3. Branch: `main`
4. Main file path: `main.py`
5. App URL: `mailbuddy-yourname` (or custom)

### Step 3: Add Secrets

1. Click **"Advanced settings"**
2. Scroll to **"Secrets"** section
3. Paste your secrets (format from above):

```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
SENDER_EMAIL = "your.email@gmail.com"
EMAIL_PASSWORD = "your app password here"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

4. Click **"Save"**

### Step 4: Deploy!

1. Click **"Deploy!"**
2. Wait 2-3 minutes for build
3. Your app will be live at: `https://mailbuddy-yourname.streamlit.app`

---

## ✅ Verification After Deployment

### Test 1: API Key
1. Open your deployed app
2. Expand "📧 Email Server Settings"
3. The fields should auto-populate from secrets
4. Click "🧪 Test Gemini API"
5. Should see: ✅ "Gemini API connection successful!"

### Test 2: IMAP Connection
1. Credentials should be pre-filled
2. Click "🔌 Connect IMAP"
3. Should see: ✅ "IMAP connected successfully!"

### Test 3: Monitor
1. Set check interval (5 minutes)
2. Click "🟢 Start Monitor"
3. Should see status change to "🟢 Active"

---

## 🔒 Security Best Practices

### ✅ DO:
- Use **Streamlit Cloud Secrets** (never commit secrets.toml)
- Use **Gmail App Passwords** (never use real password)
- Keep repo **Private** if contains any personal data
- Use **different API keys** for dev/production

### ❌ DON'T:
- Commit `.streamlit/secrets.toml` to GitHub
- Commit `data/known_contacts.json` 
- Share your App Password publicly
- Use your regular Gmail password

---

## 🐛 Troubleshooting

### "Module not found" Error

**Cause:** Missing package in requirements.txt

**Fix:** Make sure `requirements.txt` has:
```
streamlit>=1.28.0
google-generativeai>=0.3.0
pydantic>=2.0.0
```

### "IMAP connection failed" on Streamlit Cloud

**Cause:** Wrong App Password or spaces

**Fix:** 
1. Generate new App Password
2. Copy with spaces: `abcd efgh ijkl mnop`
3. Update secrets in Streamlit dashboard
4. Reboot app

### "API Key Invalid"

**Cause:** Wrong API key or quotes

**Fix:**
1. Verify API key at: https://makersuite.google.com/app/apikey
2. Check quotes in secrets (must be double quotes)
3. No extra spaces

### "Secrets not loading"

**Cause:** Wrong TOML format

**Fix:**
```toml
# Correct format
GOOGLE_API_KEY = "value_here"

# NOT this:
google_api_key = value_here
```

### App Crashes on Start

**Check Logs:**
1. Streamlit Cloud dashboard
2. Click "Manage app"
3. View logs
4. Look for errors

**Common fixes:**
- Reboot app
- Check secrets format
- Verify requirements.txt

---

## 📊 Resource Limits on Streamlit Cloud

### Free Tier Limits:
- **CPU**: 0.078 cores
- **RAM**: 800 MB
- **Sleep**: After 7 days of inactivity
- **Concurrent users**: Limited

### For MailBuddy:
- ✅ Background monitoring: Works fine
- ✅ IMAP connections: No issues
- ✅ Gemini API calls: Supported
- ⚠️ Heavy email processing: May be slow
- ⚠️ Many concurrent users: May hit limits

---

## 🎯 Production Tips

### 1. Optimize Check Interval
- Set to **5-10 minutes** (not 1 minute)
- Reduces resource usage
- Prevents rate limiting

### 2. Monitor Gemini API Quota
- Free tier: 60 requests/minute
- Track usage in Google Cloud Console
- Template fallback activates if quota exceeded

### 3. Keep Known Contacts Small
- Limit to <100 contacts
- Stored in session state (uses RAM)

### 4. Use Private Repo
- Recommended for personal email automation
- Prevents credential leaks
- Free private repos on GitHub

### 5. Regular Updates
```powershell
# Update code
git add .
git commit -m "Update: improved triage rules"
git push

# Streamlit auto-deploys on push!
```

---

## 🔄 Updating Your Deployed App

### To Update Code:

```powershell
# 1. Make changes to code
# 2. Commit and push
git add .
git commit -m "Your update message"
git push

# Streamlit Cloud auto-detects and redeploys!
```

### To Update Secrets:

1. Go to Streamlit Cloud dashboard
2. Click your app → "Settings"
3. Edit secrets
4. Click "Save"
5. Click "Reboot app"

---

## 📱 Accessing Your Deployed App

### Your App URL:
```
https://mailbuddy-yourname.streamlit.app
```

### Share with Others:
- URL is public if repo is public
- They can't see your secrets
- Each user needs their own credentials
- Or you can keep repo private (only you access)

---

## 💡 Alternative: Local Secrets (Development)

### For local development:

Create `.streamlit/secrets.toml`:

```toml
GOOGLE_API_KEY = "your_key"
SENDER_EMAIL = "your@email.com"
EMAIL_PASSWORD = "your app password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

**This file is gitignored** - safe for local testing!

---

## ✅ Final Deployment Checklist

Before deploying:

- [ ] `.gitignore` includes sensitive files
- [ ] No secrets in code (using `st.secrets`)
- [ ] `requirements.txt` is complete
- [ ] Code tested locally
- [ ] Gmail App Password generated
- [ ] Gemini API key obtained
- [ ] GitHub repo created
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account ready
- [ ] Secrets formatted correctly (TOML)
- [ ] App deployed and tested

---

## 🎉 Summary

**YES, your MailBuddy app will work on Streamlit Cloud!**

### What You Need:

1. **Push to GitHub** (exclude secrets)
2. **Deploy on Streamlit Cloud**
3. **Add these secrets:**

```toml
GOOGLE_API_KEY = "AIzaSy..."
SENDER_EMAIL = "your@gmail.com"
EMAIL_PASSWORD = "abcd efgh ijkl mnop"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

4. **Access your app** at `https://mailbuddy-yourname.streamlit.app`

---

## 📞 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app
- **Secrets Docs**: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- **MailBuddy Docs**: See `README.md` and `docs/` folder

---

**You're ready to deploy! 🚀**
