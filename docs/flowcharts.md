# MailBuddy Process Flowcharts

Visual guides for understanding MailBuddy's workflows and processes.

---

## 1. IMAP Configuration Flow

```mermaid
flowchart TD
    Start([User Opens MailBuddy]) --> CheckConfig{IMAP Configured?}
    CheckConfig -->|No| ShowSettings[Show Email Server Settings]
    CheckConfig -->|Yes| MainApp[Show Main Application]
    
    ShowSettings --> EnterCreds[User Enters Credentials]
    EnterCreds --> ClickConnect[Click 'Connect IMAP']
    ClickConnect --> TryConnect{Connection Attempt}
    
    TryConnect -->|Success| CreateFolders[Create Triage Folders]
    TryConnect -->|Fail| ShowError[Show Error Message]
    ShowError --> EnterCreds
    
    CreateFolders --> FoldersOK{Folders Created?}
    FoldersOK -->|Yes| SetConfigured[Set imap_configured = True]
    FoldersOK -->|No| ShowError
    
    SetConfigured --> MainApp
    MainApp --> End([Ready to Use])
```

---

## 2. Inbox Monitoring Loop

```mermaid
flowchart TD
    Start([Start Monitor Clicked]) --> CreateMonitor[Create InboxMonitor Instance]
    CreateMonitor --> SetCallback[Set new_emails_callback]
    SetCallback --> StartThread[Start Background Thread]
    
    StartThread --> Loop{is_running?}
    Loop -->|Yes| ConnectIMAP[Connect to IMAP]
    Loop -->|No| Stop([Monitor Stopped])
    
    ConnectIMAP --> FetchRecent[Fetch Recent 20 Emails]
    FetchRecent --> FilterSeen[Filter Out Seen Message IDs]
    
    FilterSeen --> NewEmails{New Emails Found?}
    NewEmails -->|Yes| AddToCache[Add to seen_message_ids]
    NewEmails -->|No| UpdateTime[Update last_check_time]
    
    AddToCache --> CallCallback[Call new_emails_callback]
    CallCallback --> AddToPending[Add to pending_emails Queue]
    AddToPending --> UpdateTime
    
    UpdateTime --> Sleep[Sleep for N Minutes]
    Sleep --> Loop
    
    Stop --> Cleanup[Disconnect IMAP]
    Cleanup --> End([Thread Terminated])
```

---

## 3. Email Triage Classification Process

```mermaid
flowchart TD
    Start([Email Received]) --> Extract[Extract Subject, Sender, Body]
    Extract --> CheckOTP{Contains OTP/Receipt Keywords?}
    
    CheckOTP -->|Yes| CategoryReceipt[Category: OTP_RECEIPT]
    CheckOTP -->|No| CheckContact{From Known Contact?}
    
    CategoryReceipt --> ActionReceipt[Action: Move to Receipts]
    ActionReceipt --> End
    
    CheckContact -->|Yes| CheckUrgent{Contains Urgent Keywords?}
    CheckContact -->|No| CheckUrgentOnly{Contains Urgent Keywords?}
    
    CheckUrgent -->|Yes| CategoryUrgent[Category: URGENT]
    CheckUrgent -->|No| CategoryImportant[Category: IMPORTANT]
    
    CategoryUrgent --> ActionUrgent[Action: Move to Urgent]
    CategoryImportant --> ActionImportant[Action: Move to Important]
    
    CheckUrgentOnly -->|Yes| CategoryImportant2[Category: IMPORTANT]
    CheckUrgentOnly -->|No| CheckNewsletter{Contains Newsletter Keywords?}
    
    CategoryImportant2 --> ActionImportant
    
    CheckNewsletter -->|Yes| CategoryNewsletter[Category: NEWSLETTER]
    CheckNewsletter -->|No| CheckPromo{Contains Promo Keywords?}
    
    CategoryNewsletter --> ActionNewsletter[Action: Move to Newsletters]
    
    CheckPromo -->|Yes| CategoryPromo[Category: PROMOTIONAL]
    CheckPromo -->|No| CategoryOther[Category: OTHER]
    
    CategoryPromo --> ActionPromo[Action: Move to Promotions]
    CategoryOther --> ActionArchive[Action: Move to Archive]
    
    ActionUrgent --> End([Return TriageResult])
    ActionImportant --> End
    ActionNewsletter --> End
    ActionPromo --> End
    ActionArchive --> End
```

---

## 4. Draft Generation Workflow

```mermaid
flowchart TD
    Start([User Clicks 'Generate Draft']) --> GetInput[Get Email Body + Tone + Info]
    GetInput --> CheckAPI{Gemini API Key Available?}
    
    CheckAPI -->|Yes| BuildPrompt[Build Gemini Prompt]
    CheckAPI -->|No| UseFallback[Use Template Fallback]
    
    BuildPrompt --> CallAPI[Call Gemini API]
    CallAPI --> APISuccess{API Response OK?}
    
    APISuccess -->|Yes| ParseResponse[Parse Response Text]
    APISuccess -->|No| UseFallback
    
    ParseResponse --> StoreDraft[Store in draft_responses]
    
    UseFallback --> SelectTemplate{Select Template by Tone}
    SelectTemplate --> Professional[Professional Template]
    SelectTemplate --> Friendly[Friendly Template]
    SelectTemplate --> Apologetic[Apologetic Template]
    SelectTemplate --> Persuasive[Persuasive Template]
    
    Professional --> InjectInfo{Important Info Provided?}
    Friendly --> InjectInfo
    Apologetic --> InjectInfo
    Persuasive --> InjectInfo
    
    InjectInfo -->|Yes| AddInfo[Add Info to Template]
    InjectInfo -->|No| UseDefault[Use Default Template]
    
    AddInfo --> StoreDraft
    UseDefault --> StoreDraft
    
    StoreDraft --> UpdateUI[Update UI]
    UpdateUI --> End([Show Draft in Generated Drafts])
```

---

## 5. Send Reply Flow

```mermaid
flowchart TD
    Start([User Clicks 'Send Reply']) --> GetCreds[Get SMTP Credentials]
    GetCreds --> CheckCreds{Credentials Valid?}
    
    CheckCreds -->|No| ErrorCreds[Show Error: Configure SMTP]
    CheckCreds -->|Yes| ExtractRecipient[Extract Recipient Email]
    
    ErrorCreds --> End([Stop])
    
    ExtractRecipient --> BuildSubject[Build Subject: 'Re: Original']
    BuildSubject --> GetBody[Get Edited Draft Body]
    GetBody --> CreateMIME[Create MIME Message]
    
    CreateMIME --> AddHeaders[Add Headers: From, To, Subject]
    AddHeaders --> AddThreading{Original Message-ID?}
    
    AddThreading -->|Yes| AddReplyHeaders[Add In-Reply-To + References]
    AddThreading -->|No| SkipThreading[Skip Threading]
    
    AddReplyHeaders --> ConnectSMTP[Connect to SMTP Server]
    SkipThreading --> ConnectSMTP
    
    ConnectSMTP --> StartTLS[Start TLS Encryption]
    StartTLS --> Login[Login with Credentials]
    
    Login --> LoginOK{Login Success?}
    LoginOK -->|No| ErrorAuth[Show Error: Auth Failed]
    LoginOK -->|Yes| SendMessage[Send Message]
    
    ErrorAuth --> End
    
    SendMessage --> SendOK{Send Success?}
    SendOK -->|No| ErrorSend[Show Error: SMTP Failed]
    SendOK -->|Yes| Cleanup[Remove from Drafts & Pending]
    
    ErrorSend --> End
    
    Cleanup --> ShowSuccess[Show Success Message]
    ShowSuccess --> RefreshUI[Refresh UI]
    RefreshUI --> End
```

---

## 6. Session State Lifecycle

```mermaid
flowchart TD
    Start([App Launch]) --> InitState[initialize_session_state]
    
    InitState --> CreateVars[Create Session Variables]
    CreateVars --> V1[imap_configured = False]
    CreateVars --> V2[folder_manager = None]
    CreateVars --> V3[inbox_monitor = None]
    CreateVars --> V4[pending_emails = empty list]
    CreateVars --> V5[draft_responses = empty dict]
    CreateVars --> V6[tone = 'Professional']
    CreateVars --> V7[monitor_running = False]
    
    V1 --> RenderUI[Render UI]
    V2 --> RenderUI
    V3 --> RenderUI
    V4 --> RenderUI
    V5 --> RenderUI
    V6 --> RenderUI
    V7 --> RenderUI
    
    RenderUI --> UserAction{User Interaction?}
    
    UserAction -->|Configure IMAP| UpdateConfig[imap_configured = True<br/>folder_manager = instance]
    UserAction -->|Start Monitor| UpdateMonitor[monitor_running = True<br/>inbox_monitor.start]
    UserAction -->|New Email Detected| UpdatePending[pending_emails.append]
    UserAction -->|Generate Draft| UpdateDrafts[draft_responses add item]
    UserAction -->|Send Email| RemoveItems[Remove from pending & drafts]
    
    UpdateConfig --> Rerun[st.rerun]
    UpdateMonitor --> Rerun
    UpdatePending --> Rerun
    UpdateDrafts --> Rerun
    RemoveItems --> Rerun
    
    Rerun --> RenderUI
    
    UserAction -->|Close App| Shutdown[Stop Monitor Thread]
    Shutdown --> End([Session Ends])
```

---

## 7. Background Thread Architecture

```mermaid
flowchart LR
    subgraph MainThread [Main Thread - Streamlit UI]
        UI[Streamlit UI] --> Display[Display State]
        Display --> UserInput[User Interactions]
        UserInput --> UpdateState[Update Session State]
        UpdateState --> UI
    end
    
    subgraph MonitorThread [Monitor Thread - Daemon]
        Loop[While is_running] --> IMAP[Poll IMAP]
        IMAP --> Filter[Filter New Emails]
        Filter --> Callback[Call Callback Function]
        Callback --> Sleep[Sleep N Minutes]
        Sleep --> Loop
    end
    
    MonitorThread -->|new_emails_callback| UpdateState
    UI -->|start/stop| MonitorThread
    
    style MainThread fill:#e1f5ff
    style MonitorThread fill:#fff4e1
```

---

## 8. Complete User Journey

```mermaid
flowchart TD
    Start([Open MailBuddy]) --> First{First Time?}
    
    First -->|Yes| Setup[Read IMAP-SETUP.md]
    First -->|No| Login[IMAP Already Configured]
    
    Setup --> GetAppPwd[Get Gmail App Password]
    GetAppPwd --> GetAPI[Get Gemini API Key]
    GetAPI --> EnterCreds[Enter in MailBuddy UI]
    EnterCreds --> Connect[Connect IMAP]
    Connect --> Login
    
    Login --> AddContacts[Add Known Contacts]
    AddContacts --> SetInterval[Set Check Interval]
    SetInterval --> StartMon[Start Monitor]
    
    StartMon --> Wait[Wait for New Emails]
    Wait --> EmailDetected{New Email?}
    
    EmailDetected -->|Yes| ShowPending[Show in Pending Queue]
    EmailDetected -->|No| Wait
    
    ShowPending --> UserReview[User Reviews Email]
    UserReview --> Decision{What to Do?}
    
    Decision -->|Reply| SelectTone[Select Tone]
    Decision -->|Organize| MoveFolder[Move to Folder]
    Decision -->|Ignore| Dismiss[Dismiss]
    
    SelectTone --> AddInfo[Add Important Info Optional]
    AddInfo --> GenDraft[Generate Draft]
    GenDraft --> ReviewDraft[Review & Edit Draft]
    
    ReviewDraft --> SendDecision{Send?}
    SendDecision -->|Yes| SendEmail[Send via SMTP]
    SendDecision -->|No| Regenerate[Regenerate or Discard]
    
    SendEmail --> Success[Success! Email Sent]
    MoveFolder --> OrganizeDone[Email Organized]
    Dismiss --> DismissDone[Removed from Queue]
    Regenerate --> GenDraft
    
    Success --> Wait
    OrganizeDone --> Wait
    DismissDone --> Wait
    
    Wait --> EndDay{End of Day?}
    EndDay -->|Yes| StopMon[Stop Monitor]
    EndDay -->|No| Wait
    
    StopMon --> End([Close MailBuddy])
```

---

## 9. Error Handling Flow

```mermaid
flowchart TD
    Start([Action Attempted]) --> TryCatch[Try Block]
    
    TryCatch --> Success{Success?}
    Success -->|Yes| Return[Return Result]
    Success -->|No| CatchError[Catch Exception]
    
    Return --> End([Operation Complete])
    
    CatchError --> ErrorType{Error Type?}
    
    ErrorType -->|IMAP Error| IMAPHandle[Log Error<br/>Show User-Friendly Message<br/>Disconnect Safely]
    ErrorType -->|SMTP Error| SMTPHandle[Check Credentials<br/>Show Auth Error<br/>Don't Cleanup Drafts]
    ErrorType -->|API Error| APIHandle[Log API Error<br/>Fall Back to Template<br/>Continue Operation]
    ErrorType -->|Network Error| NetHandle[Show Connection Error<br/>Suggest Retry<br/>Preserve State]
    ErrorType -->|Other| GenHandle[Log Error<br/>Show Generic Message<br/>Safe Fallback]
    
    IMAPHandle --> UserAction{User Action}
    SMTPHandle --> UserAction
    APIHandle --> AutoFallback[Automatic Fallback]
    NetHandle --> UserAction
    GenHandle --> UserAction
    
    UserAction -->|Retry| Start
    UserAction -->|Cancel| End
    
    AutoFallback --> Return
```

---

## 10. Folder Organization System

```mermaid
flowchart LR
    subgraph Gmail [Gmail Account]
        INBOX[📥 INBOX]
        
        subgraph TriageFolders [MailBuddy Folders]
            Urgent[🔴 Urgent]
            Important[🟡 Important]
            Newsletter[📰 Newsletters]
            Promo[🎁 Promotions]
            Receipt[🧾 Receipts]
            Archive[📄 Archive]
        end
    end
    
    INBOX -->|Monitor| Detect[Detect New Emails]
    Detect -->|Triage| Classify{Classify}
    
    Classify -->|Known + Urgent| Urgent
    Classify -->|Known OR Urgent| Important
    Classify -->|Newsletter Pattern| Newsletter
    Classify -->|Promo Keywords| Promo
    Classify -->|OTP/Receipt| Receipt
    Classify -->|Other| Archive
    
    Urgent -->|User Reviews| Action[Generate Draft<br/>or<br/>Manual Action]
    Important -->|User Reviews| Action
    Newsletter -->|Batch Process| BulkAction[Unsubscribe<br/>Archive<br/>Delete]
    Promo -->|Batch Process| BulkAction
    Receipt -->|Keep Record| Keep[Store for Reference]
    Archive -->|Low Priority| Review[Periodic Review]
    
    style INBOX fill:#ffd700
    style Urgent fill:#ff6b6b
    style Important fill:#ffd93d
    style Newsletter fill:#6bcf7f
    style Promo fill:#a29bfe
    style Receipt fill:#74b9ff
    style Archive fill:#dfe6e9
```

---

## Legend

### Flowchart Symbols

- **Rectangle**: Process/Action
- **Diamond**: Decision/Condition
- **Parallelogram**: Input/Output
- **Rounded Rectangle**: Start/End
- **Arrow**: Flow Direction
- **Dashed Line**: Optional Path

### Color Coding

- 🔴 **Red**: Urgent/High Priority
- 🟡 **Yellow**: Important/Medium Priority
- 🟢 **Green**: Success/OK
- ⚫ **Gray**: Stopped/Inactive
- 🔵 **Blue**: Information/Process

---

## How to Use These Flowcharts

1. **For Learning**: Follow the flows to understand MailBuddy's logic
2. **For Debugging**: Trace where an issue occurs in the flow
3. **For Development**: Use as reference when modifying code
4. **For Documentation**: Share with team members or users

---

## Interactive Mermaid Diagrams

These diagrams are written in **Mermaid** syntax and can be:

- Rendered in GitHub README
- Viewed in Mermaid Live Editor: https://mermaid.live/
- Embedded in documentation sites
- Exported as SVG/PNG images

### Viewing Tips

**In VS Code**:
1. Install "Markdown Preview Mermaid Support" extension
2. Open this file in preview mode
3. Diagrams render automatically

**In GitHub**:
1. Push this file to your repository
2. Navigate to it in GitHub UI
3. Mermaid diagrams render natively

**In Browser**:
1. Copy a diagram
2. Paste into https://mermaid.live/
3. Edit and export as needed

---

**For more information, see:**
- [IMAP Setup Guide](IMAP-SETUP.md)
- [Automation Guide](automation-guide.md)
- [Main README](../README.md)
