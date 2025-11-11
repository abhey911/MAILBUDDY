"""
MailBuddy Utils Package

This package contains utility modules for email management.
"""

from .contacts import load_contacts, save_contacts
from .email_folder_manager import EmailFolderManager
from .inbox_monitor import InboxMonitor
from .email_sender import send_email
from .mailbuddy_triage import TriageTask, EmailTriageResult

__all__ = [
    'load_contacts',
    'save_contacts',
    'EmailFolderManager',
    'InboxMonitor',
    'send_email',
    'TriageTask',
    'EmailTriageResult'
]
