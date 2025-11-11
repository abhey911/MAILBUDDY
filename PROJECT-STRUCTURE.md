# MailBuddy - Project Structure

Complete file tree and description of all components.

## Directory Structure

```
MAILBUDDY/
│
├── main.py                          # Main Streamlit application - RUN THIS FILE
│
├── requirements.txt                 # Python dependencies (streamlit, google-generativeai, pydantic)
├── README.md                        # Project overview and documentation
├── QUICKSTART.md                    # Quick start guide for new users
├── setup.ps1                        # Windows PowerShell setup script
├── .gitignore                       # Git ignore rules (excludes secrets, venv, data/known_contacts.json)
│
├── agents/                          # AI-powered agents
│   ├── __init__.py                  # Package initialization
│   └── email_agent.py               # Gemini API integration + template fallback
│
├── utils/                           # Utility modules
│   ├── __init__.py                  # Package initialization
│   ├── contacts.py                  # Known contacts management (JSON operations)
│   ├── email_folder_manager.py      # IMAP operations (connect, search, move, folders)
│   ├── inbox_monitor.py             # Background monitoring service (daemon thread)
│   ├── email_sender.py              # SMTP sending logic (TLS, authentication)
│   └── mailbuddy_triage.py          # Rule-based email classification engine
│
├── data/                            # User data (gitignored except example)
│   ├── known_contacts.json          # User's contact list (GITIGNORED)
│   └── known_contacts.example.json  # Example template for known_contacts.json
│
├── docs/                            # Documentation
│   ├── IMAP-SETUP.md                # Step-by-step IMAP/SMTP configuration guide
│   ├── automation-guide.md          # How to use automation features effectively
│   └── flowcharts.md                # Mermaid flowcharts for all processes
│
└── tests/                           # Unit tests
    ├── __init__.py                  # Test package initialization
    ├── conftest.py                  # Pytest fixtures and shared test configuration
    ├── test_email_folder_manager.py # Tests for IMAP folder operations
    └── test_mailbuddy_triage.py     # Tests for email classification engine
```

## File Descriptions

### Root Files

| File | Description | Key Features |
|------|-------------|--------------|
| `main.py` | Main Streamlit app | UI sections, session state, automation controls |
| `requirements.txt` | Python dependencies | streamlit, google-generativeai, pydantic |
| `README.md` | Project documentation | Overview, features, quick start, troubleshooting |
| `QUICKSTART.md` | Quick start guide | 5-minute setup instructions |
| `setup.ps1` | Windows setup script | Automated venv creation, dependency installation |
| `.gitignore` | Git ignore rules | Excludes .venv, secrets, known_contacts.json |

### agents/

| File | Description | Key Components |
|------|-------------|----------------|
| `email_agent.py` | AI response generator | `generate_email_response()`, Gemini API integration, template fallback |

**Functions:**
- `generate_email_response(email_text, tone, important_info, api_key)` - Main generation function
- `test_gemini_connection(api_key)` - Test API connectivity
- Template generators for each tone (Professional, Friendly, Apologetic, Persuasive)

### utils/

| File | Description | Key Components |
|------|-------------|----------------|
| `contacts.py` | Contact management | Load/save known contacts JSON |
| `email_folder_manager.py` | IMAP operations | Connect, search, move emails, manage folders |
| `inbox_monitor.py` | Background monitoring | Daemon thread, polling, callback pattern |
| `email_sender.py` | SMTP sending | TLS encryption, authentication, threading headers |
| `mailbuddy_triage.py` | Email classification | Rule-based triage, keyword matching, Pydantic models |

#### contacts.py Functions:
- `load_contacts()` - Load from JSON
- `save_contacts(contacts)` - Save to JSON
- `add_contact(email)` - Add single contact
- `remove_contact(email)` - Remove single contact

#### email_folder_manager.py Class:
```python
class EmailFolderManager:
    - connect() - IMAP4_SSL connection
    - disconnect() - Safe logout
    - ensure_folders_exist() - Create triage folders
    - search_emails(folder, limit) - Fetch emails
    - move_email(msg_id, from_folder, to_folder) - Move email
    - get_folder_for_category(category) - Map category to folder
    - fetch_recent_emails(folder, limit) - Get full email details
```

#### inbox_monitor.py Class:
```python
class InboxMonitor:
    - set_new_emails_callback(callback) - Register callback
    - check_for_new_emails() - Poll IMAP once
    - start() - Start daemon thread
    - stop() - Stop monitoring
    - get_status() - Return status dict
    - set_check_interval(seconds) - Update interval
```

#### email_sender.py Functions:
- `send_email(sender_email, sender_password, recipient_email, subject, body, ...)` - Send via SMTP
- `validate_email_address(email)` - Regex validation

#### mailbuddy_triage.py Classes:
```python
class EmailTriageResult(BaseModel):
    category: str
    action: str
    justification: str

class TriageTask:
    - run(email_data) - Classify email
    - _is_from_known_contact(sender) - Check known contacts
    - _contains_keywords(text, keywords) - Keyword matching
    - _matches_pattern(text, patterns) - Regex matching
```

**Categories:**
- URGENT (🔴) - Known contact + urgent keywords
- IMPORTANT (🟡) - Known contact OR urgent keywords
- NEWSLETTER (📰) - Newsletter patterns
- PROMOTIONAL (🎁) - Promotional keywords
- OTP_RECEIPT (🧾) - OTP codes, receipts
- OTHER (📄) - Everything else

### data/

| File | Description | Format |
|------|-------------|--------|
| `known_contacts.json` | User's important contacts | JSON array of email addresses (gitignored) |
| `known_contacts.example.json` | Template file | Example structure |

### docs/

| File | Description | Contents |
|------|-------------|----------|
| `IMAP-SETUP.md` | IMAP/SMTP setup guide | Enable IMAP, App Password, API key, troubleshooting |
| `automation-guide.md` | Automation usage guide | Workflows, best practices, tips & tricks |
| `flowcharts.md` | Process flowcharts | 10 Mermaid diagrams visualizing all processes |

### tests/

| File | Description | Test Coverage |
|------|-------------|---------------|
| `conftest.py` | Pytest configuration | Fixtures, mock objects, sample data |
| `test_email_folder_manager.py` | IMAP manager tests | Connection, folders, moving emails |
| `test_mailbuddy_triage.py` | Triage engine tests | Classification, keywords, categories |

## Key Session State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `imap_configured` | bool | IMAP connection status |
| `folder_manager` | EmailFolderManager | IMAP manager instance |
| `inbox_monitor` | InboxMonitor | Background monitor instance |
| `pending_emails` | List[Dict] | Queue of newly detected emails |
| `draft_responses` | Dict[str, Dict] | Generated drafts keyed by email ID |
| `tone` | str | Selected tone (Professional/Friendly/etc.) |
| `monitor_running` | bool | Monitor active status |
| `check_interval` | int | Check interval in minutes |

## Configuration Files (User Created)

### .streamlit/secrets.toml (Optional)
```toml
GOOGLE_API_KEY = "your_gemini_api_key"
SENDER_EMAIL = "your.email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

**Security Note:** This file is gitignored and should NEVER be committed!

## Workflow Summary

### 1. IMAP Configuration
- User enters credentials in UI
- EmailFolderManager connects to IMAP
- Creates triage folders (Urgent, Important, etc.)

### 2. Monitoring
- InboxMonitor starts daemon thread
- Polls IMAP every N minutes
- Filters new emails by Message-ID
- Calls callback to update pending_emails

### 3. Triage
- TriageTask classifies each email
- Checks known contacts
- Matches keywords and patterns
- Returns category + action + justification

### 4. Draft Generation
- User selects email + tone
- Calls Gemini API with prompt
- Falls back to template if API unavailable
- Stores in draft_responses

### 5. Review & Send
- User edits draft
- Validates SMTP credentials
- Sends via SMTP with TLS
- Adds In-Reply-To header for threading
- Removes from queues on success

## Dependencies

### Required (requirements.txt)
- `streamlit>=1.28.0` - Web UI framework
- `google-generativeai>=0.3.0` - Gemini API client
- `pydantic>=2.0.0` - Data validation

### Python Standard Library
- `imaplib` - IMAP client
- `smtplib` - SMTP client
- `email` - Email parsing
- `threading` - Background monitoring
- `json` - Config file handling
- `re` - Regex pattern matching
- `datetime` - Timestamps
- `os` - Environment variables

### Optional (for testing)
- `pytest` - Test framework
- `unittest.mock` - Mocking

## Running the Application

### Quick Start
```powershell
# Setup (first time only)
.\setup.ps1

# Run
streamlit run main.py
```

### Manual Setup
```powershell
# Create venv
python -m venv .venv

# Activate
.\.venv\Scripts\activate

# Install
pip install -r requirements.txt

# Run
streamlit run main.py
```

### Access
- Local: http://localhost:8501
- Network: http://<your-ip>:8501

## Git Workflow

### What's Tracked
- All source code (.py files)
- Documentation (.md files)
- Example files (.example.json)
- Configuration templates
- Tests

### What's Ignored (.gitignore)
- Virtual environment (.venv/)
- Secrets (.streamlit/secrets.toml)
- User data (data/known_contacts.json)
- Python cache (__pycache__/, *.pyc)
- IDE files (.vscode/, .idea/)

## Deployment Options

### Local
- Run on your machine
- Full control, no cloud costs
- Requires machine to be online

### Streamlit Cloud
1. Push to GitHub (excluding secrets)
2. Connect Streamlit Cloud to repo
3. Add secrets in Cloud dashboard
4. Deploy automatically

### Docker (Advanced)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "main.py"]
```

## Troubleshooting Reference

| Issue | File to Check | Solution |
|-------|---------------|----------|
| IMAP connection fails | `email_folder_manager.py` | Check credentials, App Password |
| Monitor not detecting | `inbox_monitor.py` | Verify interval, check IMAP connection |
| Triage misclassifies | `mailbuddy_triage.py` | Update known_contacts.json |
| Draft generation fails | `email_agent.py` | Check API key, uses template fallback |
| Send fails | `email_sender.py` | Verify SMTP credentials |
| UI not loading | `main.py` | Check session state initialization |

## Performance Notes

- **IMAP Polling**: Default 5 min interval prevents rate limiting
- **Email Limit**: Fetches last 20 emails per check (configurable)
- **Thread Safety**: InboxMonitor uses threading.Lock for state
- **Seen Messages**: Cached in memory to prevent duplicates
- **API Quota**: Gemini has free tier limits, template fallback available

## Future Enhancements

Potential features to add:
- [ ] Keyboard shortcuts
- [ ] Batch operations
- [ ] Custom triage rules UI
- [ ] Email templates library
- [ ] Scheduled sending
- [ ] Multiple account support
- [ ] Advanced filtering
- [ ] Statistics dashboard

---

**Project Status:** ✅ Production Ready

**Last Updated:** 2025-01-11

**Version:** 1.0.0
