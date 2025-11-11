# Streamlit Cloud Secrets - Quick Reference

## 📋 Copy This Into Streamlit Cloud Secrets

Go to: **App Settings → Secrets** in Streamlit Cloud

Paste this format (replace with your actual values):

```toml
# Google Gemini API Key
# Get it from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Your Gmail Address
SENDER_EMAIL = "your.email@gmail.com"

# Gmail App Password (NOT your regular password!)
# Get it from: https://myaccount.google.com/security → App passwords
# Include spaces as shown: "abcd efgh ijkl mnop"
EMAIL_PASSWORD = "abcd efgh ijkl mnop"

# SMTP Server Settings (usually no need to change)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

---

## ✅ Example (with fake credentials)

```toml
GOOGLE_API_KEY = "AIzaSyB1234567890abcdefghijklmnopqrstuv"
SENDER_EMAIL = "mailbuddy.demo@gmail.com"
EMAIL_PASSWORD = "wxyz abcd efgh ijkl"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

---

## ⚠️ Important Rules

1. ✅ **Keep double quotes** around all values
2. ✅ **Include spaces** in App Password (e.g., "abcd efgh ijkl mnop")
3. ✅ **Use EXACT variable names** (case-sensitive)
4. ✅ **No extra spaces** before/after `=`
5. ❌ **Never commit** this to GitHub!

---

## 🔑 How to Get These Values

### 1. Gmail App Password
```
1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification" (if not enabled)
3. Click "App passwords"
4. Select: Mail → Other (Custom name)
5. Name it: "MailBuddy"
6. Copy the 16-character password
7. Paste WITH SPACES: "abcd efgh ijkl mnop"
```

### 2. Gemini API Key
```
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Select or create a Google Cloud project
4. Copy the entire API key
5. Paste in secrets
```

### 3. Gmail Address
```
Just your regular Gmail address that you want to use
```

---

## 🚀 Quick Deployment Steps

### 1. Push to GitHub
```powershell
cd "C:\Users\abhey\OneDrive\Desktop\MAILBUDDY"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/MailBuddy.git
git push -u origin main
```

### 2. Deploy on Streamlit
```
1. Go to: https://share.streamlit.io/
2. Click "New app"
3. Select: YOUR_USERNAME/MailBuddy
4. Main file: main.py
5. Click "Advanced settings"
6. Paste secrets (from above)
7. Click "Deploy!"
```

### 3. Test Your App
```
1. Wait 2-3 minutes for deployment
2. Open your app URL
3. Click "🧪 Test Gemini API"
4. Click "🔌 Connect IMAP"
5. Start using MailBuddy!
```

---

## 🔧 Troubleshooting

### "IMAP connection failed"
- Check App Password has spaces: `"abcd efgh ijkl mnop"`
- Regenerate App Password if needed
- Verify SENDER_EMAIL is correct

### "Gemini API error"
- Verify API key is complete
- Check for typos
- Ensure quotes are present

### "Secrets not found"
- Variable names must be EXACT (uppercase)
- Check TOML format (= with quotes)
- Reboot app after saving secrets

---

## 📝 Save This Template

Copy this to a safe place (NOT in GitHub):

```toml
GOOGLE_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
SENDER_EMAIL = "YOUR_EMAIL@gmail.com"
EMAIL_PASSWORD = "YOUR APP PASSWORD WITH SPACES"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

Fill it in and paste into Streamlit Cloud!

---

**That's it! Your MailBuddy will be live! 🎉**
