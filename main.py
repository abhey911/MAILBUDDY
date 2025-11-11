
import streamlit as st
import os
from datetime import datetime
from typing import Dict, List

from agents.email_agent import generate_email_response, test_gemini_connection
from utils.contacts import load_contacts, save_contacts, add_contact, remove_contact
from utils.email_folder_manager import EmailFolderManager
from utils.inbox_monitor import InboxMonitor
from utils.email_sender import send_email, validate_email_address
from utils.mailbuddy_triage import TriageTask, EmailTriageResult


# Page configuration
st.set_page_config(
    page_title="MailBuddy - Think Less, Send Smart",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize all session state variables."""
    if 'imap_configured' not in st.session_state:
        st.session_state.imap_configured = False
    
    if 'folder_manager' not in st.session_state:
        st.session_state.folder_manager = None
    
    if 'inbox_monitor' not in st.session_state:
        st.session_state.inbox_monitor = None
    
    if 'pending_emails' not in st.session_state:
        st.session_state.pending_emails = []
    
    if 'draft_responses' not in st.session_state:
        st.session_state.draft_responses = {}
    
    if 'generated_response' not in st.session_state:
        st.session_state.generated_response = ""
    
    if 'editing_response' not in st.session_state:
        st.session_state.editing_response = ""
    
    if 'tone' not in st.session_state:
        st.session_state.tone = "Professional"
    
    if 'monitor_running' not in st.session_state:
        st.session_state.monitor_running = False
    
    if 'check_interval' not in st.session_state:
        st.session_state.check_interval = 5  # minutes


def new_emails_callback(new_emails: List[Dict]):
    """Callback when new emails are detected by monitor."""
    if new_emails:
        st.session_state.pending_emails.extend(new_emails)


def configure_imap_section():
    """Render IMAP configuration section."""
    with st.expander("📧 Email Server Settings", expanded=not st.session_state.imap_configured):
        st.markdown("### IMAP & SMTP Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### IMAP Settings (Receiving)")
            
            # Try to get from secrets first, then environment
            default_email = st.secrets.get("SENDER_EMAIL", os.getenv("SENDER_EMAIL", ""))
            default_password = st.secrets.get("EMAIL_PASSWORD", os.getenv("EMAIL_PASSWORD", ""))
            
            email_address = st.text_input(
                "Email Address",
                value=default_email,
                key="imap_email",
                help="Your Gmail address"
            )
            
            email_password = st.text_input(
                "App Password",
                value=default_password,
                type="password",
                key="imap_password",
                help="Gmail App Password (not regular password)"
            )
            
            imap_server = st.text_input("IMAP Server", value="imap.gmail.com", key="imap_server")
            imap_port = st.number_input("IMAP Port", value=993, key="imap_port")
        
        with col2:
            st.markdown("#### SMTP Settings (Sending)")
            
            smtp_email = st.text_input(
                "SMTP Email",
                value=default_email,
                key="smtp_email",
                help="Usually same as IMAP email"
            )
            
            smtp_password = st.text_input(
                "SMTP Password",
                value=default_password,
                type="password",
                key="smtp_password",
                help="Same App Password as IMAP"
            )
            
            smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com", key="smtp_server")
            smtp_port = st.number_input("SMTP Port", value=587, key="smtp_port")
        
        # Gemini API Key
        st.markdown("#### 🤖 AI Configuration")
        default_api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
        
        api_key = st.text_input(
            "Google Gemini API Key",
            value=default_api_key,
            type="password",
            key="gemini_api_key",
            help="Get your key from https://makersuite.google.com/app/apikey"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🔌 Connect IMAP", use_container_width=True):
                with st.spinner("Connecting to IMAP server..."):
                    folder_manager = EmailFolderManager(
                        email_address, email_password, imap_server, imap_port
                    )
                    
                    if folder_manager.connect():
                        # Ensure folders exist
                        if folder_manager.ensure_folders_exist():
                            st.session_state.folder_manager = folder_manager
                            st.session_state.imap_configured = True
                            st.success("✅ IMAP connected successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to create folders")
                    else:
                        st.error("❌ IMAP connection failed. Check credentials.")
        
        with col2:
            if st.button("🧪 Test Gemini API", use_container_width=True):
                if api_key:
                    with st.spinner("Testing API connection..."):
                        success, message = test_gemini_connection(api_key)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.warning("⚠️ Please enter API key first")
        
        with col3:
            if st.button("📬 Fetch Latest Emails", use_container_width=True):
                if st.session_state.folder_manager:
                    with st.spinner("Fetching emails from INBOX..."):
                        try:
                            recent_emails = st.session_state.folder_manager.fetch_recent_emails("INBOX", limit=10)
                            if recent_emails:
                                # Add to pending queue
                                new_count = 0
                                for email_data in recent_emails:
                                    # Check if already in pending
                                    msg_id = email_data.get('message_id', email_data.get('id'))
                                    already_exists = any(
                                        e.get('message_id') == msg_id or e.get('id') == msg_id 
                                        for e in st.session_state.pending_emails
                                    )
                                    if not already_exists:
                                        st.session_state.pending_emails.append(email_data)
                                        new_count += 1
                                
                                if new_count > 0:
                                    st.success(f"✅ Fetched {new_count} email(s)!")
                                    st.rerun()
                                else:
                                    st.info("All emails already in queue")
                            else:
                                st.info("No emails found in INBOX")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("⚠️ Connect to IMAP first")
        
        if st.session_state.imap_configured:
            st.success("🟢 IMAP is configured and connected")
            
            # Show pending emails count
            if st.session_state.pending_emails:
                st.info(f"📬 {len(st.session_state.pending_emails)} email(s) in pending queue")


def automated_monitor_section():
    """Render automated inbox monitoring section."""
    if not st.session_state.imap_configured:
        st.info("📧 Please configure IMAP settings first to enable monitoring")
        return
    
    with st.expander("⚡ Automated Inbox Monitor", expanded=True):
        st.markdown("### Background Email Monitoring")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            check_interval = st.slider(
                "Check Interval (minutes)",
                min_value=1,
                max_value=30,
                value=st.session_state.check_interval,
                key="monitor_interval_slider",
                help="How often to check for new emails"
            )
            st.session_state.check_interval = check_interval
        
        with col2:
            if not st.session_state.monitor_running:
                if st.button("🟢 Start Monitor", use_container_width=True):
                    # Create monitor if not exists
                    if not st.session_state.inbox_monitor:
                        st.session_state.inbox_monitor = InboxMonitor(
                            st.session_state.folder_manager,
                            check_interval_seconds=check_interval * 60
                        )
                        st.session_state.inbox_monitor.set_new_emails_callback(new_emails_callback)
                    else:
                        st.session_state.inbox_monitor.set_check_interval(check_interval * 60)
                    
                    st.session_state.inbox_monitor.start()
                    st.session_state.monitor_running = True
                    st.success("✅ Monitor started!")
                    st.rerun()
            else:
                if st.button("⚫ Stop Monitor", use_container_width=True):
                    if st.session_state.inbox_monitor:
                        st.session_state.inbox_monitor.stop()
                    st.session_state.monitor_running = False
                    st.success("✅ Monitor stopped!")
                    st.rerun()
        
        with col3:
            if st.button("🔄 Check Now", use_container_width=True):
                if st.session_state.folder_manager:
                    with st.spinner("Checking for new emails..."):
                        # Use folder_manager directly to fetch emails
                        try:
                            recent_emails = st.session_state.folder_manager.fetch_recent_emails("INBOX", limit=20)
                            if recent_emails:
                                # Filter out already seen emails
                                new_count = 0
                                for email_data in recent_emails:
                                    # Check if already in pending
                                    msg_id = email_data.get('message_id', email_data.get('id'))
                                    already_exists = any(
                                        e.get('message_id') == msg_id or e.get('id') == msg_id 
                                        for e in st.session_state.pending_emails
                                    )
                                    if not already_exists:
                                        st.session_state.pending_emails.append(email_data)
                                        new_count += 1
                                
                                if new_count > 0:
                                    st.success(f"✅ Found {new_count} new email(s)!")
                                    st.rerun()
                                else:
                                    st.info("No new emails (all already in queue)")
                            else:
                                st.info("No emails found in INBOX")
                        except Exception as e:
                            st.error(f"Error fetching emails: {str(e)}")
                else:
                    st.warning("⚠️ Please connect to IMAP first")
        
        # Status display
        if st.session_state.inbox_monitor:
            status = st.session_state.inbox_monitor.get_status()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                status_icon = "🟢" if status['running'] else "⚫"
                st.metric("Status", f"{status_icon} {'Active' if status['running'] else 'Stopped'}")
            
            with col2:
                st.metric("Check Interval", f"{check_interval} min")
            
            with col3:
                last_check = status['last_check_time']
                if last_check:
                    time_str = last_check.strftime("%H:%M:%S")
                else:
                    time_str = "Never"
                st.metric("Last Check", time_str)
            
            with col4:
                st.metric("Emails Seen", status['emails_seen_count'])


def pending_emails_section():
    """Render pending emails queue section."""
    if not st.session_state.imap_configured:
        return
    
    with st.expander(f"📬 Pending Emails ({len(st.session_state.pending_emails)})", expanded=True):
        if not st.session_state.pending_emails:
            st.info("No pending emails. Start the monitor or click 'Check Now' to fetch new emails.")
            return
        
        st.markdown("### Newly Detected Emails")
        
        # Load contacts for triage
        known_contacts = load_contacts()
        triage_task = TriageTask(known_contacts)
        
        for idx, email_data in enumerate(st.session_state.pending_emails):
            email_id = email_data.get('message_id', email_data.get('id'))
            
            with st.container():
                st.markdown("---")
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**From:** {email_data.get('sender', 'Unknown')}")
                    st.markdown(f"**Subject:** {email_data.get('subject', 'No Subject')}")
                
                with col2:
                    # Triage classification
                    triage_result = triage_task.run(email_data)
                    
                    category_colors = {
                        "URGENT": "🔴",
                        "IMPORTANT": "🟡",
                        "NEWSLETTER": "📰",
                        "PROMOTIONAL": "🎁",
                        "OTP_RECEIPT": "🧾",
                        "OTHER": "📄"
                    }
                    
                    icon = category_colors.get(triage_result.category, "📄")
                    st.markdown(f"{icon} **{triage_result.category}**")
                
                # Email body preview
                body_preview = email_data.get('body', '')[:200]
                if len(email_data.get('body', '')) > 200:
                    body_preview += "..."
                
                with st.expander("View Email"):
                    st.text_area("Email Body", value=email_data.get('body', ''), height=150, key=f"email_body_{idx}")
                    
                    st.markdown(f"**Triage Suggestion:** {triage_result.action}")
                    st.markdown(f"**Justification:** {triage_result.justification}")
                
                # Actions
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
                
                with col1:
                    tone_key = f"tone_{idx}"
                    tone = st.selectbox(
                        "Tone",
                        ["Professional", "Friendly", "Apologetic", "Persuasive"],
                        key=tone_key
                    )
                
                with col2:
                    if st.button("✍️ Generate Draft", key=f"gen_{idx}", use_container_width=True):
                        with st.spinner("Generating response..."):
                            api_key = st.session_state.get('gemini_api_key', '')
                            important_info = st.session_state.get(f'important_info_{idx}', '')
                            
                            response = generate_email_response(
                                email_data.get('body', ''),
                                tone=tone,
                                important_info=important_info if important_info else None,
                                api_key=api_key if api_key else None
                            )
                            
                            st.session_state.draft_responses[email_id] = {
                                'email_data': email_data,
                                'response': response,
                                'tone': tone,
                                'original_index': idx
                            }
                            
                            st.success("✅ Draft generated!")
                            st.rerun()
                
                with col3:
                    if st.button("📤 Send Response", key=f"send_resp_{idx}", use_container_width=True):
                        with st.spinner("Generating and sending response..."):
                            api_key = st.session_state.get('gemini_api_key', '')
                            important_info = st.session_state.get(f'important_info_{idx}', '')
                            
                            # Generate response
                            response = generate_email_response(
                                email_data.get('body', ''),
                                tone=tone,
                                important_info=important_info if important_info else None,
                                api_key=api_key if api_key else None
                            )
                            
                            # Send via SMTP - read directly from widget keys
                            smtp_email = st.session_state.get('smtp_email', '')
                            smtp_password = st.session_state.get('smtp_password', '')
                            smtp_server = st.session_state.get('smtp_server', 'smtp.gmail.com')
                            smtp_port = st.session_state.get('smtp_port', 587)
                            
                            if smtp_email and smtp_password:
                                success, message = send_email(
                                    sender_email=smtp_email,
                                    sender_password=smtp_password,
                                    recipient_email=email_data.get('sender', ''),
                                    subject=f"Re: {email_data.get('subject', '')}",
                                    body=response,
                                    smtp_server=smtp_server,
                                    smtp_port=smtp_port,
                                    original_message_id=email_data.get('message_id')
                                )
                                
                                if success:
                                    st.session_state.pending_emails.pop(idx)
                                    st.success("✅ Response sent!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                            else:
                                st.error("❌ SMTP not configured. Please enter SMTP credentials in Email Server Settings.")
                
                with col4:
                    folder = st.session_state.folder_manager.get_folder_for_category(triage_result.category)
                    if st.button(f"📁 Move to {folder[:8]}", key=f"move_{idx}", use_container_width=True):
                        with st.spinner(f"Moving to {folder}..."):
                            # Use 'id' field which is the IMAP message ID
                            imap_msg_id = email_data.get('id')
                            if imap_msg_id:
                                success = st.session_state.folder_manager.move_email(
                                    imap_msg_id,
                                    "INBOX",
                                    folder
                                )
                                if success:
                                    st.session_state.pending_emails.pop(idx)
                                    st.success(f"✅ Moved to {folder}!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to move email")
                            else:
                                st.error("❌ Email ID not found")
                
                with col5:
                    if st.button("🗑️ Dismiss", key=f"dismiss_{idx}", use_container_width=True):
                        st.session_state.pending_emails.pop(idx)
                        st.rerun()
                
                # Optional important info field
                st.text_input(
                    "Important information to include (optional)",
                    key=f"important_info_{idx}",
                    placeholder="Add context for AI to include in response..."
                )


def generated_drafts_section():
    """Render generated drafts section."""
    if not st.session_state.draft_responses:
        return
    
    with st.expander(f"✍️ Generated Drafts ({len(st.session_state.draft_responses)})", expanded=True):
        st.markdown("### Review and Send Drafts")
        
        for email_id, draft_data in list(st.session_state.draft_responses.items()):
            email_data = draft_data['email_data']
            response = draft_data['response']
            
            with st.container():
                st.markdown("---")
                
                st.markdown(f"**To:** {email_data.get('sender', 'Unknown')}")
                st.markdown(f"**Re:** {email_data.get('subject', 'No Subject')}")
                st.markdown(f"**Tone:** {draft_data.get('tone', 'Professional')}")
                
                # Editable draft
                edited_response = st.text_area(
                    "Draft Response",
                    value=response,
                    height=200,
                    key=f"draft_{email_id}"
                )
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📤 Send Reply", key=f"send_{email_id}", use_container_width=True):
                        smtp_email = st.session_state.get('smtp_email', '')
                        smtp_password = st.session_state.get('smtp_password', '')
                        smtp_server = st.session_state.get('smtp_server', 'smtp.gmail.com')
                        smtp_port = st.session_state.get('smtp_port', 587)
                        
                        if not smtp_email or not smtp_password:
                            st.error("❌ SMTP credentials not configured")
                        else:
                            with st.spinner("Sending email..."):
                                # Extract recipient email
                                sender = email_data.get('sender', '')
                                import re
                                match = re.search(r'<(.+?)>', sender)
                                recipient = match.group(1) if match else sender
                                
                                subject = f"Re: {email_data.get('subject', 'No Subject')}"
                                
                                success, message = send_email(
                                    sender_email=smtp_email,
                                    sender_password=smtp_password,
                                    recipient_email=recipient,
                                    subject=subject,
                                    body=edited_response,
                                    smtp_server=smtp_server,
                                    smtp_port=smtp_port,
                                    original_message_id=email_data.get('message_id')
                                )
                                
                                if success:
                                    # Remove from drafts and pending
                                    del st.session_state.draft_responses[email_id]
                                    
                                    # Remove from pending if still there
                                    st.session_state.pending_emails = [
                                        e for e in st.session_state.pending_emails
                                        if e.get('message_id') != email_id
                                    ]
                                    
                                    st.success(f"✅ {message}")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                
                with col2:
                    if st.button("🔄 Regenerate", key=f"regen_{email_id}", use_container_width=True):
                        with st.spinner("Regenerating..."):
                            api_key = st.session_state.get('gemini_api_key', '')
                            
                            new_response = generate_email_response(
                                email_data.get('body', ''),
                                tone=draft_data.get('tone', 'Professional'),
                                api_key=api_key if api_key else None
                            )
                            
                            st.session_state.draft_responses[email_id]['response'] = new_response
                            st.success("✅ Regenerated!")
                            st.rerun()
                
                with col3:
                    if st.button("💾 Update", key=f"update_{email_id}", use_container_width=True):
                        st.session_state.draft_responses[email_id]['response'] = edited_response
                        st.success("✅ Draft updated!")
                
                with col4:
                    if st.button("🗑️ Discard", key=f"discard_{email_id}", use_container_width=True):
                        del st.session_state.draft_responses[email_id]
                        st.rerun()


def classified_folders_section():
    """Render section to browse emails in classified folders."""
    if not st.session_state.imap_configured:
        return
    
    with st.expander("📁 Browse Classified Folders", expanded=False):
        st.markdown("### View Emails by Category")
        
        # Folder selection
        folders = {
            "🔴 Urgent": "Urgent",
            "🟡 Important": "Important",
            "📰 Newsletters": "Newsletters",
            "🎁 Promotions": "Promotions",
            "🧾 Receipts": "Receipts",
            "📄 Archive": "Archive"
        }
        
        selected_folder_display = st.selectbox(
            "Select Folder:",
            options=list(folders.keys())
        )
        
        selected_folder = folders[selected_folder_display]
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            limit = st.number_input("Emails to show:", min_value=5, max_value=50, value=10, step=5)
        
        with col2:
            if st.button("🔄 Load Folder", use_container_width=True):
                with st.spinner(f"Loading emails from {selected_folder}..."):
                    try:
                        emails = st.session_state.folder_manager.fetch_recent_emails(selected_folder, limit=limit)
                        st.session_state[f'folder_emails_{selected_folder}'] = emails
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error loading folder: {str(e)}")
        
        # Display folder emails
        folder_key = f'folder_emails_{selected_folder}'
        if folder_key in st.session_state and st.session_state[folder_key]:
            emails = st.session_state[folder_key]
            st.markdown(f"**{len(emails)} email(s) in {selected_folder}**")
            
            for idx, email_data in enumerate(emails):
                with st.container():
                    st.markdown("---")
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**From:** {email_data.get('sender', 'Unknown')}")
                        st.markdown(f"**Subject:** {email_data.get('subject', 'No Subject')}")
                        st.caption(f"Date: {email_data.get('date', 'Unknown')}")
                    
                    with col2:
                        if st.button("👁️ View", key=f"view_folder_{selected_folder}_{idx}", use_container_width=True):
                            st.session_state[f'viewing_email_{idx}'] = not st.session_state.get(f'viewing_email_{idx}', False)
                            st.rerun()
                    
                    # Show email body if viewing
                    if st.session_state.get(f'viewing_email_{idx}', False):
                        st.text_area(
                            "Email Body:",
                            value=email_data.get('body', ''),
                            height=200,
                            key=f"folder_body_{selected_folder}_{idx}",
                            disabled=True
                        )
                        
                        # Actions
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("↩️ Move to INBOX", key=f"move_inbox_{selected_folder}_{idx}", use_container_width=True):
                                imap_msg_id = email_data.get('id')
                                if imap_msg_id:
                                    success = st.session_state.folder_manager.move_email(
                                        imap_msg_id,
                                        selected_folder,
                                        "INBOX"
                                    )
                                    if success:
                                        st.success("✅ Moved to INBOX!")
                                        # Remove from current view
                                        st.session_state[folder_key].pop(idx)
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to move")
                        
                        with col2:
                            if st.button("📤 Reply", key=f"reply_{selected_folder}_{idx}", use_container_width=True):
                                # Add to drafts for replying
                                email_id = email_data.get('message_id', email_data.get('id'))
                                if email_id not in st.session_state.draft_responses:
                                    st.session_state.draft_responses[email_id] = {
                                        'email_data': email_data,
                                        'response': '',
                                        'tone': 'Professional',
                                        'original_index': idx
                                    }
                                    st.success("✅ Added to drafts!")
                                    st.rerun()
        else:
            st.info(f"Click 'Load Folder' to view emails in {selected_folder}")


def manual_compose_section():
    """Render manual email composition section."""
    with st.expander("✉️ Manual Compose", expanded=False):
        st.markdown("### Compose New Email")
        
        col1, col2 = st.columns(2)
        
        with col1:
            recipient = st.text_input("To:", placeholder="recipient@example.com")
            subject = st.text_input("Subject:", placeholder="Email subject")
        
        with col2:
            tone = st.selectbox("Tone:", ["Professional", "Friendly", "Apologetic", "Persuasive"], key="manual_tone")
        
        email_content = st.text_area("Email Content:", height=200, placeholder="Write your email here...")
        
        col1, col2, col3 = st.columns([2, 2, 6])
        
        with col1:
            if st.button("🤖 Generate with AI", use_container_width=True):
                if email_content:
                    with st.spinner("Generating..."):
                        api_key = st.session_state.get('gemini_api_key', '')
                        
                        # Use as prompt/context
                        prompt = f"Generate a complete email based on this request: {email_content}"
                        response = generate_email_response(prompt, tone=tone, api_key=api_key if api_key else None)
                        
                        st.session_state.generated_response = response
                        st.rerun()
                else:
                    st.warning("⚠️ Please enter email content first")
        
        with col2:
            if st.button("📤 Send Email", use_container_width=True):
                if not recipient or not subject or not email_content:
                    st.error("❌ Please fill all fields")
                elif not validate_email_address(recipient):
                    st.error("❌ Invalid recipient email address")
                else:
                    smtp_email = st.session_state.get('smtp_email', '')
                    smtp_password = st.session_state.get('smtp_password', '')
                    smtp_server = st.session_state.get('smtp_server', 'smtp.gmail.com')
                    smtp_port = st.session_state.get('smtp_port', 587)
                    
                    if not smtp_email or not smtp_password:
                        st.error("❌ SMTP credentials not configured")
                    else:
                        with st.spinner("Sending..."):
                            success, message = send_email(
                                sender_email=smtp_email,
                                sender_password=smtp_password,
                                recipient_email=recipient,
                                subject=subject,
                                body=email_content,
                                smtp_server=smtp_server,
                                smtp_port=smtp_port
                            )
                            
                            if success:
                                st.success(f"✅ {message}")
                                # Clear fields
                                st.session_state.generated_response = ""
                            else:
                                st.error(f"❌ {message}")
        
        # Show generated response if exists
        if st.session_state.generated_response:
            st.markdown("### Generated Response:")
            edited = st.text_area(
                "Edit before sending:",
                value=st.session_state.generated_response,
                height=200,
                key="edited_manual_response"
            )


def sidebar_content():
    """Render sidebar content."""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/mail.png", width=80)
        st.title("MailBuddy")
        st.caption("Think Less, Send Smart")
        
        st.markdown("---")
        
        st.markdown("### 📊 Quick Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Pending", len(st.session_state.pending_emails))
        with col2:
            st.metric("Drafts", len(st.session_state.draft_responses))
        
        st.markdown("---")
        
        st.markdown("### 👥 Known Contacts")
        
        contacts = load_contacts()
        
        if contacts:
            for contact in contacts[:5]:  # Show first 5
                st.text(f"• {contact}")
            
            if len(contacts) > 5:
                st.caption(f"... and {len(contacts) - 5} more")
        else:
            st.info("No contacts added yet")
        
        # Add contact
        new_contact = st.text_input("Add contact email:", placeholder="email@example.com")
        if st.button("➕ Add Contact", use_container_width=True):
            if new_contact and validate_email_address(new_contact):
                if add_contact(new_contact):
                    st.success("✅ Contact added!")
                    st.rerun()
            else:
                st.error("❌ Invalid email address")
        
        st.markdown("---")
        
        st.markdown("### 📚 Documentation")
        st.markdown("[📖 IMAP Setup Guide](docs/IMAP-SETUP.md)")
        st.markdown("[🤖 Automation Guide](docs/automation-guide.md)")
        st.markdown("[📊 Flowcharts](docs/flowcharts.md)")
        
        st.markdown("---")
        st.caption("Made with ❤️ using Streamlit")


def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Header
    st.title("📧 MailBuddy: Think Less, Send Smart")
    st.markdown("Automated email management with AI-powered responses")
    
    # Sidebar
    sidebar_content()
    
    # Main sections
    configure_imap_section()
    automated_monitor_section()
    pending_emails_section()
    classified_folders_section()
    generated_drafts_section()
    manual_compose_section()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        <p>MailBuddy v1.0 | Powered by Google Gemini | 
        <a href='https://github.com' target='_blank'>GitHub</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
