# IMAP Setup Guide for MailBuddy

This guide will walk you through setting up IMAP access for Gmail to use with MailBuddy.

## Prerequisites

- A Gmail account
- Access to Gmail settings
- 2-Step Verification enabled (required for App Passwords)

## Step 1: Enable IMAP in Gmail

1. **Log in to Gmail** using your web browser
2. Click the **Settings gear** icon (top right)
3. Click **"See all settings"**
4. Navigate to the **"Forwarding and POP/IMAP"** tab
5. In the IMAP section, select **"Enable IMAP"**
6. Click **"Save Changes"** at the bottom

## Step 2: Enable 2-Step Verification

App Passwords require 2-Step Verification to be enabled.

1. Go to your **Google Account**: https://myaccount.google.com/
2. Navigate to **Security** (left sidebar)
3. Under "How you sign in to Google", click **2-Step Verification**
4. Follow the prompts to enable 2-Step Verification
   - You'll need to verify your phone number
   - Choose your preferred second verification method

## Step 3: Generate an App Password

⚠️ **Important**: You MUST use an App Password, not your regular Gmail password!

1. Go to your **Google Account**: https://myaccount.google.com/
2. Navigate to **Security** (left sidebar)
3. Under "How you sign in to Google", click **2-Step Verification**
4. Scroll down to the bottom and click **"App passwords"**
   - If you don't see this option, make sure 2-Step Verification is enabled
5. You may need to sign in again
6. Under "Select app", choose **"Mail"**
7. Under "Select device", choose **"Other (Custom name)"**
8. Enter **"MailBuddy"** as the name
9. Click **"Generate"**
10. **Copy the 16-character password** that appears
    - It will look like: `xxxx xxxx xxxx xxxx`
    - Save this somewhere safe - you won't be able to see it again!

## Step 4: Configure MailBuddy

### Option A: Using the UI (Recommended for beginners)

1. Run MailBuddy: `streamlit run main.py`
2. In the "📧 Email Server Settings" section, enter:
   - **Email Address**: your.email@gmail.com
   - **App Password**: The 16-character password from Step 3 (no spaces)
   - **IMAP Server**: imap.gmail.com
   - **IMAP Port**: 993
   - **SMTP Server**: smtp.gmail.com
   - **SMTP Port**: 587
3. Click **"🔌 Connect IMAP"**

### Option B: Using Streamlit Secrets (Recommended for deployment)

1. Create a `.streamlit` folder in your project root
2. Create a file named `secrets.toml` inside it
3. Add the following:

```toml
GOOGLE_API_KEY = "your_gemini_api_key_here"
SENDER_EMAIL = "your.email@gmail.com"
EMAIL_PASSWORD = "your_app_password_here"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

4. Save the file
5. Restart MailBuddy

⚠️ **Security Note**: Never commit `secrets.toml` to Git! It's already in `.gitignore`.

## Step 5: Get Google Gemini API Key (Optional but Recommended)

For AI-powered draft generation:

1. Go to **Google AI Studio**: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Select your Google Cloud project (or create a new one)
4. Copy the API key
5. Enter it in MailBuddy's AI Configuration section or add to `secrets.toml`

## Testing Your Configuration

### Test IMAP Connection

1. In MailBuddy, click **"🔌 Connect IMAP"**
2. You should see: ✅ "IMAP connected successfully!"
3. If you see an error, check:
   - Email address is correct
   - App Password is correct (16 characters, no spaces)
   - IMAP is enabled in Gmail settings

### Test Gemini API

1. Enter your API key
2. Click **"🧪 Test Gemini API"**
3. You should see: ✅ "Gemini API connection successful!"

## Troubleshooting

### Error: "Authentication failed"

**Causes:**
- Using regular Gmail password instead of App Password
- App Password was copied with spaces
- 2-Step Verification not enabled

**Solutions:**
- Generate a new App Password following Step 3
- Remove all spaces from the password when pasting
- Enable 2-Step Verification in Google Account settings

### Error: "IMAP connection failed"

**Causes:**
- IMAP not enabled in Gmail
- Firewall/antivirus blocking port 993
- Network connectivity issues

**Solutions:**
- Enable IMAP following Step 1
- Temporarily disable firewall/antivirus to test
- Check your internet connection
- Try using a different network

### Error: "Failed to create folders"

**Causes:**
- Insufficient IMAP permissions
- Gmail folder limit reached

**Solutions:**
- Check Gmail folder/label count (max 500)
- Try creating folders manually in Gmail first
- Sign out and sign back in to refresh IMAP session

### Error: "Invalid credentials" when sending

**Causes:**
- SMTP password different from IMAP password
- SMTP settings incorrect

**Solutions:**
- Use the same App Password for both IMAP and SMTP
- Verify SMTP server is `smtp.gmail.com`
- Verify SMTP port is `587` (not 465 or 25)

## Security Best Practices

✅ **DO:**
- Use App Passwords, never your regular password
- Keep your App Password secret
- Use `.streamlit/secrets.toml` for storing credentials
- Revoke App Passwords you're not using
- Enable 2-Step Verification

❌ **DON'T:**
- Commit passwords to Git
- Share your App Password
- Use your regular Gmail password
- Disable 2-Step Verification after creating App Password

## Revoking Access

If you want to stop MailBuddy's access to your Gmail:

1. Go to your **Google Account**: https://myaccount.google.com/
2. Navigate to **Security**
3. Click **2-Step Verification**
4. Scroll to **App passwords**
5. Click the **X** next to "MailBuddy"
6. Confirm revocation

## Gmail IMAP Limits

Be aware of Gmail's IMAP limits:

- **Daily download limit**: ~2.5 GB/day
- **Simultaneous connections**: 15 connections max
- **Commands per second**: Limited (varies)

MailBuddy is designed to stay within these limits with default settings.

## Non-Gmail Email Providers

While this guide focuses on Gmail, MailBuddy can work with other IMAP providers:

### Outlook/Hotmail

- IMAP Server: `outlook.office365.com`
- IMAP Port: `993`
- SMTP Server: `smtp.office365.com`
- SMTP Port: `587`
- Use App Password (enable in Outlook account settings)

### Yahoo Mail

- IMAP Server: `imap.mail.yahoo.com`
- IMAP Port: `993`
- SMTP Server: `smtp.mail.yahoo.com`
- SMTP Port: `587`
- Generate App Password in Yahoo Account Security settings

### Custom Domain / Other Providers

Consult your email provider's documentation for:
- IMAP server address and port
- SMTP server address and port
- Whether App Passwords are supported

## Need More Help?

- Check the [Automation Guide](automation-guide.md)
- Review [Flowcharts](flowcharts.md) for visual process guides
- Open an issue on GitHub

---

**Next Steps**: Once IMAP is configured, check out the [Automation Guide](automation-guide.md) to learn how to use MailBuddy's automation features!
