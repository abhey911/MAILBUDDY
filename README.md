# MailBuddy: Think Less, Send Smart 📧

An intelligent email management system that automates inbox monitoring, generates AI-powered responses, and streamlines your email workflow.

## Overview

MailBuddy is a Python-based Streamlit application that automatically monitors your Gmail inbox, detects new emails, allows selective draft generation with AI, and sends replies - all with a clean, user-friendly interface.

## Features

- **🤖 Automated Inbox Monitoring**: Background service polls Gmail IMAP every N minutes (configurable)
- **🎯 Smart Email Triage**: Automatically categorize emails (Urgent, Important, Newsletters, Promotions, Receipts, Archive)
- **✍️ AI-Powered Draft Generation**: Uses Google Gemini API to generate intelligent responses
- **📬 Multiple Tone Support**: Professional, Friendly, Apologetic, Persuasive
- **⚡ One-Click Reply Sending**: Review, edit, and send with SMTP integration
- **📊 Real-time Status**: Live monitoring status, statistics, and feedback

## Tech Stack

- **Frontend**: Streamlit
- **Email**: IMAP (inbox monitoring), SMTP (sending)
- **AI**: Google Gemini API
- **Language**: Python 3.8+
- **Data Validation**: Pydantic

## Project Structure

```
MailBuddy/
├── main.py                          # Main Streamlit app
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── .gitignore                       # Git ignore rules
├── agents/
│   ├── __init__.py
│   └── email_agent.py              # AI response generation
├── utils/
│   ├── __init__.py
│   ├── inbox_monitor.py            # Background IMAP monitoring
│   ├── email_folder_manager.py     # IMAP operations
│   ├── email_sender.py             # SMTP sending logic
│   ├── mailbuddy_triage.py         # Email classification
│   └── contacts.py                 # Contact management
├── data/
│   ├── known_contacts.json         # User contacts (gitignored)
│   └── known_contacts.example.json # Example template
├── docs/
│   ├── IMAP-SETUP.md              # IMAP setup guide
│   ├── automation-guide.md         # Automation usage guide
│   └── flowcharts.md              # Process flowcharts
└── tests/
    ├── conftest.py
    ├── test_email_folder_manager.py
    └── test_mailbuddy_triage.py
```

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd MailBuddy
```

### 2. Set up virtual environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure IMAP and SMTP

See detailed instructions in [docs/IMAP-SETUP.md](docs/IMAP-SETUP.md)

**Quick setup:**
1. Enable IMAP in Gmail settings
2. Generate an App Password (not your regular password)
3. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### 5. Set up secrets (optional but recommended)

Create `.streamlit/secrets.toml`:

```toml
GOOGLE_API_KEY = "your_gemini_api_key"
SENDER_EMAIL = "your.email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

Alternatively, configure via the UI on first run.

### 6. Run the application

```bash
streamlit run main.py
```

### 7. Access the app

Open your browser to: `http://localhost:8501`

## Usage

1. **Configure Email Settings**: Enter IMAP/SMTP credentials
2. **Start Automated Monitor**: Set check interval and start monitoring
3. **Review Pending Emails**: See newly detected emails in queue
4. **Generate Drafts**: Select tone and generate AI responses
5. **Review & Edit**: Edit drafts before sending
6. **Send Replies**: One-click sending with automatic cleanup

## 🌐 Deploy to Streamlit Cloud

Want to run MailBuddy in the cloud? It's 100% compatible with Streamlit Cloud!

**See detailed guide:** [STREAMLIT-DEPLOYMENT.md](STREAMLIT-DEPLOYMENT.md)

**Quick secrets format:** [SECRETS-FORMAT.md](SECRETS-FORMAT.md)

```toml
GOOGLE_API_KEY = "your_api_key"
SENDER_EMAIL = "your@gmail.com"
EMAIL_PASSWORD = "your app password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

## Documentation

- **[IMAP Setup Guide](docs/IMAP-SETUP.md)**: Step-by-step IMAP configuration
- **[Automation Guide](docs/automation-guide.md)**: How to use automation features
- **[Flowcharts](docs/flowcharts.md)**: Visual process diagrams
- **[Streamlit Deployment](STREAMLIT-DEPLOYMENT.md)**: Deploy to Streamlit Cloud
- **[Secrets Format](SECRETS-FORMAT.md)**: Quick reference for secrets

## Security Best Practices

- ✅ Never commit passwords or API keys to git
- ✅ Use Gmail App Passwords (not regular password)
- ✅ SSL/TLS for IMAP (port 993) and SMTP (STARTTLS on 587)
- ✅ Store known contacts locally only (gitignored)
- ✅ Use `.streamlit/secrets.toml` for production deployment

## Troubleshooting

**IMAP Connection Issues:**
- Verify IMAP is enabled in Gmail settings
- Use App Password, not regular password
- Check firewall/antivirus blocking port 993

**Gemini API Errors:**
- Verify API key is valid
- Check API quota limits
- Falls back to template-based generation if API unavailable

**Monitor Not Detecting Emails:**
- Check IMAP credentials
- Verify interval setting (default: 5 minutes)
- Look for errors in status panel

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For issues and questions, please open an issue on GitHub.

---
## QUICK DEMO VIDEO
Watch a complete walkthrough of MailBuddy 
https://drive.google.com/file/d/1LMbcgiVboXF6QQfc39zrsyRrAGurGi_x/view?usp=sharing

---

**Made with  using Streamlit and Google Gemini**
