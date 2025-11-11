# MailBuddy Quick Start Guide

Get up and running with MailBuddy in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Gmail account with IMAP enabled
- Google Gemini API key (optional but recommended)

## Installation

### 1. Navigate to Project Directory

```powershell
cd "c:\Users\abhey\OneDrive\Desktop\MAILBUDDY"
```

### 2. Create Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate Virtual Environment

```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Configuration

### Quick Setup (Using UI)

1. Run the application:
```powershell
streamlit run main.py
```

2. The app will open in your browser at `http://localhost:8501`

3. In the "📧 Email Server Settings" section, enter:
   - **Email Address**: your.email@gmail.com
   - **App Password**: Your Gmail App Password (see below)
   - **SMTP Email**: Same as email address
   - **SMTP Password**: Same App Password
   - **Gemini API Key**: Your Google Gemini API key

4. Click "🔌 Connect IMAP"

### Getting Gmail App Password

**Quick Steps:**

1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification" (if not already enabled)
3. Go to "App passwords"
4. Create new app password for "Mail" - "Other (Custom name)"
5. Name it "MailBuddy"
6. Copy the 16-character password (remove spaces)

**Detailed guide**: See [docs/IMAP-SETUP.md](docs/IMAP-SETUP.md)

### Getting Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## First Steps

### 1. Add Known Contacts

In the sidebar:
- Enter email addresses of important contacts
- Click "➕ Add Contact"
- These contacts will be prioritized in triage

### 2. Start Monitoring

1. Set check interval (5 minutes recommended)
2. Click "🟢 Start Monitor"
3. Monitor will check for new emails automatically

### 3. Process Emails

When new emails arrive:
1. Review in "📬 Pending Emails" section
2. Select tone (Professional/Friendly/Apologetic/Persuasive)
3. Click "✍️ Generate Draft"
4. Review and edit in "✍️ Generated Drafts"
5. Click "📤 Send Reply"

## Common Commands

### Run Application
```powershell
streamlit run main.py
```

### Stop Application
Press `Ctrl+C` in terminal

### Deactivate Virtual Environment
```powershell
deactivate
```

### Run Tests (if pytest installed)
```powershell
pip install pytest
pytest tests/
```

## Troubleshooting

### "Import error" or "Module not found"
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

### "IMAP connection failed"
- Check IMAP is enabled in Gmail settings
- Use App Password, not regular password
- Verify no spaces in password

### "Gemini API error"
- Verify API key is correct
- Check API quota limits
- System will fall back to templates automatically

### Monitor not detecting emails
- Check IMAP connection is active
- Verify monitor status shows "🟢 Active"
- Try "🔄 Check Now" to test manually

## File Structure

```
MAILBUDDY/
├── main.py                 # Run this file
├── requirements.txt        # Dependencies
├── README.md              # Full documentation
├── .gitignore             # Git ignore rules
├── agents/
│   └── email_agent.py     # AI generation
├── utils/
│   ├── contacts.py        # Contact management
│   ├── email_folder_manager.py  # IMAP operations
│   ├── inbox_monitor.py   # Background monitoring
│   ├── email_sender.py    # SMTP sending
│   └── mailbuddy_triage.py  # Email classification
├── data/
│   ├── known_contacts.json  # Your contacts (auto-created)
│   └── known_contacts.example.json  # Example file
├── docs/
│   ├── IMAP-SETUP.md      # Detailed IMAP guide
│   ├── automation-guide.md  # How to use automation
│   └── flowcharts.md      # Visual process guides
└── tests/
    └── ...                # Unit tests
```

## Next Steps

- Read [IMAP Setup Guide](docs/IMAP-SETUP.md) for detailed configuration
- Review [Automation Guide](docs/automation-guide.md) for best practices
- Check [Flowcharts](docs/flowcharts.md) for visual workflows

## Support

- Check documentation in `docs/` folder
- Review code comments for technical details
- Open issues on GitHub

---

**Happy emailing! 📧**
