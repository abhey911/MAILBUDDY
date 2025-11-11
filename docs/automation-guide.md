# MailBuddy Automation Guide

Learn how to effectively use MailBuddy's automation features to manage your inbox effortlessly.

## Table of Contents

1. [Overview](#overview)
2. [Automated Inbox Monitoring](#automated-inbox-monitoring)
3. [Email Triage System](#email-triage-system)
4. [Draft Generation Workflow](#draft-generation-workflow)
5. [Best Practices](#best-practices)
6. [Tips & Tricks](#tips--tricks)

---

## Overview

MailBuddy automates three key email management tasks:

1. **Monitoring**: Automatically checks for new emails in background
2. **Triaging**: Classifies emails into categories (Urgent, Important, etc.)
3. **Drafting**: Generates AI-powered responses with customizable tone

### The Automation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                  MAILBUDDY WORKFLOW                         │
└─────────────────────────────────────────────────────────────┘

 1. MONITOR          2. DETECT           3. QUEUE
   (Background)        (Auto)              (Pending)
      │                  │                    │
      ▼                  ▼                    ▼
  ┌────────┐        ┌────────┐          ┌────────┐
  │  IMAP  │───────>│  New   │─────────>│Pending │
  │ Check  │        │Emails? │          │ Queue  │
  └────────┘        └────────┘          └────────┘
      │                                      │
      └──────> Sleep N minutes <─────────────┘
                                             │
                                             ▼
                                        ┌─────────┐
                                        │ TRIAGE  │
                                        │ Classify│
                                        └─────────┘
                                             │
                    ┌────────────────────────┼────────────────────┐
                    ▼                        ▼                    ▼
              ┌─────────┐              ┌─────────┐          ┌─────────┐
              │ URGENT  │              │IMPORTANT│          │ OTHER   │
              └─────────┘              └─────────┘          └─────────┘
                    │                        │                    │
                    └────────────────────────┼────────────────────┘
                                             ▼
                                        ┌─────────┐
                                        │  USER   │
                                        │ SELECTS │
                                        └─────────┘
                                             │
                                             ▼
                                        ┌─────────┐
                                        │   AI    │
                                        │GENERATE │
                                        └─────────┘
                                             │
                                             ▼
                                        ┌─────────┐
                                        │ REVIEW  │
                                        │  EDIT   │
                                        └─────────┘
                                             │
                                             ▼
                                        ┌─────────┐
                                        │  SEND   │
                                        │  SMTP   │
                                        └─────────┘
```

---

## Automated Inbox Monitoring

### How It Works

The Inbox Monitor runs in a **background thread** that:

1. Polls your Gmail INBOX via IMAP every N minutes
2. Fetches recent emails (last 20)
3. Filters out emails already seen (uses Message-ID tracking)
4. Adds new emails to the Pending Queue
5. Repeats after sleep interval

### Configuration

#### Check Interval

- **Range**: 1-30 minutes
- **Default**: 5 minutes
- **Recommendation**: 
  - 1-2 minutes for high-volume urgent inbox
  - 5-10 minutes for normal workload
  - 15-30 minutes for low-priority monitoring

#### Starting the Monitor

1. Configure IMAP settings first
2. Set your desired check interval with the slider
3. Click **🟢 Start Monitor**
4. Monitor status shows "🟢 Active"

#### Stopping the Monitor

1. Click **⚫ Stop Monitor**
2. Status changes to "⚫ Stopped"
3. Background thread stops gracefully

#### Manual Check

- Click **🔄 Check Now** to poll immediately
- Useful for testing or when you expect an important email
- Works even when monitor is stopped

### Status Information

The monitor displays:

- **Status**: 🟢 Active or ⚫ Stopped
- **Check Interval**: Current interval in minutes
- **Last Check**: Timestamp of last poll (HH:MM:SS)
- **Emails Seen**: Total unique emails tracked (prevents duplicates)

---

## Email Triage System

### Categories

MailBuddy automatically classifies emails into 6 categories:

| Category | Icon | Criteria | Action |
|----------|------|----------|--------|
| **URGENT** | 🔴 | From known contact + urgent keywords | Move to Urgent |
| **IMPORTANT** | 🟡 | From known contact OR urgent keywords | Move to Important |
| **NEWSLETTER** | 📰 | Contains newsletter patterns | Move to Newsletters |
| **PROMOTIONAL** | 🎁 | Contains promotional keywords | Move to Promotions |
| **RECEIPTS** | 🧾 | OTP codes, receipts, confirmations | Move to Receipts |
| **OTHER** | 📄 | Everything else | Move to Archive |

### Known Contacts

**Why It Matters**: Emails from known contacts are prioritized as IMPORTANT or URGENT.

**Managing Contacts**:

1. In the sidebar, see your current known contacts
2. Add new contact: Enter email → Click "➕ Add Contact"
3. Contacts are stored in `data/known_contacts.json` (gitignored)
4. Contacts affect triage classification immediately

**Tips**:
- Add your team members, clients, VIPs
- Add personal contacts for urgent personal emails
- Review and update regularly

### Triage Keywords

#### Urgent Keywords
- urgent, asap, immediately, critical, emergency
- important, deadline, action required, time sensitive

#### Newsletter Keywords
- unsubscribe, newsletter, weekly digest, subscription
- mailing list, email preferences

#### Promotional Keywords
- sale, discount, offer, deal, promotion, coupon
- free shipping, limited time, % off, buy now

#### Receipt Keywords
- receipt, order confirmation, invoice, payment
- transaction, purchase, tracking number

### Manual Triage Actions

For each pending email:

1. **View Email**: Expand to see full body
2. **Triage Suggestion**: See category and justification
3. **Move to Folder**: Click "📁 Move to [Folder]" to organize
4. **Generate Draft**: Create AI response (see next section)
5. **Dismiss**: Remove from pending without action

---

## Draft Generation Workflow

### Step 1: Select Email & Tone

From the Pending Emails section:

1. Choose the email you want to reply to
2. Select tone from dropdown:
   - **Professional**: Formal, business-like
   - **Friendly**: Warm, conversational
   - **Apologetic**: Sorry, understanding
   - **Persuasive**: Confident, compelling

### Step 2: Add Context (Optional)

- Use "Important information to include" field
- Examples:
  - "Meeting scheduled for Tuesday 3pm"
  - "Include pricing: $99/month"
  - "Mention our new product launch"
- AI will incorporate this into the response

### Step 3: Generate Draft

1. Click **✍️ Generate Draft**
2. MailBuddy uses Google Gemini API
3. If API unavailable, falls back to template
4. Draft appears in "Generated Drafts" section

### Step 4: Review & Edit

In the Generated Drafts section:

1. **Review**: Read the generated response
2. **Edit**: Modify text directly in the text area
3. **Update**: Click "💾 Update" to save changes
4. **Regenerate**: Click "🔄 Regenerate" for new version (same tone)

### Step 5: Send or Discard

- **📤 Send Reply**: Sends via SMTP, removes from queues
- **🗑️ Discard**: Deletes draft without sending

### AI vs Template Generation

**Gemini API** (Preferred):
- ✅ Context-aware responses
- ✅ Natural language
- ✅ Incorporates custom instructions
- ⚠️ Requires API key and quota

**Template Fallback**:
- ✅ Always available
- ✅ No API key needed
- ⚠️ Generic responses
- ⚠️ Less personalized

---

## Best Practices

### 1. Configure Known Contacts First

**Why**: Ensures urgent emails from important people are prioritized.

**How**:
- Add contacts before starting monitor
- Update contacts as your network grows
- Review contacts monthly

### 2. Start with Longer Intervals

**Why**: Prevents overwhelming yourself with too many emails.

**How**:
- Begin with 10-15 minute intervals
- Adjust based on your email volume
- Decrease if missing urgent emails
- Increase if getting too many notifications

### 3. Review Before Sending

**Why**: AI-generated content should always be human-reviewed.

**How**:
- Read every draft before sending
- Edit for tone, accuracy, context
- Add personal touches
- Verify recipient information

### 4. Use Different Tones Strategically

**Professional**: 
- Client communications
- Formal business inquiries
- Official requests

**Friendly**:
- Team members
- Casual networking
- Thank you notes

**Apologetic**:
- Service recovery
- Delayed responses
- Mistakes or errors

**Persuasive**:
- Sales outreach
- Partnership proposals
- Negotiation

### 5. Organize with Folders

**Why**: Keeps inbox clean and emails findable.

**How**:
- Use "Move to [Folder]" for each category
- Check folders periodically
- Archive newsletters/promotions for later
- Keep Urgent/Important folders prioritized

### 6. Manual Compose for Complex Emails

**When**:
- Multi-recipient messages
- Sensitive topics
- Detailed proposals
- Custom formatting needed

**How**:
- Use "✉️ Manual Compose" section
- Write initial draft or outline
- Click "🤖 Generate with AI" for assistance
- Edit and send

---

## Tips & Tricks

### Batch Processing

Process multiple emails efficiently:

1. Start monitor, let it collect emails (10-15 min)
2. Stop monitor
3. Review all pending emails
4. Generate drafts for relevant emails
5. Batch edit all drafts
6. Send all at once
7. Restart monitor

### Custom Important Info Templates

Save common instructions as notes:

- "Include standard disclaimer"
- "Mention 30-day guarantee"
- "Add my calendar link: [URL]"
- "Refer to our privacy policy"

Copy-paste when generating drafts.

### Triage Override

If triage misclassifies:

1. Check "Known Contacts" list
2. Add/remove contacts as needed
3. Manually move to correct folder
4. Future emails from same sender will be reclassified

### Keyboard Workflow (Coming Soon)

Future versions will support keyboard shortcuts:

- `G`: Generate draft
- `S`: Send reply
- `D`: Discard
- `E`: Edit draft
- `N`: Next email

### Monitor During Work Hours Only

**Setup**:
1. Start monitor at beginning of workday
2. Set 5-minute interval
3. Stop monitor at end of day

**Benefits**:
- No after-hours interruptions
- Focused email processing
- Better work-life balance

### API Quota Management

**If you hit Gemini API limits**:

1. Reduce generation frequency
2. Use templates for simple emails
3. Batch generate during off-peak hours
4. Upgrade API plan if needed

**Template fallback automatically activates** if API fails.

---

## Troubleshooting

### Monitor Not Detecting New Emails

**Check**:
- ✅ IMAP connection is active
- ✅ Monitor status shows "🟢 Active"
- ✅ Interval is reasonable (not too long)
- ✅ New emails are arriving in INBOX (not filtered to folders)

**Solution**: Click "🔄 Check Now" to force immediate check.

### Drafts Not Generating

**Check**:
- ✅ Gemini API key is entered
- ✅ API key is valid (test with "🧪 Test Gemini API")
- ✅ Internet connection is active

**Solution**: System will automatically use template fallback.

### Emails Classified Incorrectly

**Check**:
- ✅ Known Contacts list
- ✅ Email content matches keywords

**Solution**: 
- Add/remove contacts
- Manually move to correct folder
- Future similar emails will learn

### Sent Emails Not Threading

**Check**:
- ✅ Original email has Message-ID
- ✅ SMTP is configured correctly

**Note**: Gmail threading depends on headers. Most emails will thread correctly.

---

## Advanced Usage

### Custom Workflow Example

**"VIP Fast Response" Workflow**:

```
1. Add VIP contacts to Known Contacts
2. Set 2-minute check interval
3. Start monitor
4. When VIP email detected:
   → Auto-classified as URGENT
   → Generate Professional draft
   → Quick review & edit
   → Send within 5 minutes
```

**"Newsletter Cleanup" Workflow**:

```
1. Let monitor run for 1 hour
2. Stop monitor
3. Filter pending emails by category: NEWSLETTER
4. Bulk move all to Newsletters folder
5. Review monthly for unsubscribes
```

---

## Next Steps

- ✅ Read [IMAP Setup Guide](IMAP-SETUP.md) for configuration
- ✅ Review [Flowcharts](flowcharts.md) for visual guides
- ✅ Experiment with different tones
- ✅ Build your Known Contacts list
- ✅ Find your optimal check interval

---

**Happy automating! 🚀**
