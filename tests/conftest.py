"""
Pytest Configuration and Fixtures

Shared test configuration for MailBuddy tests.
"""

import pytest
from unittest.mock import Mock, MagicMock
import imaplib


@pytest.fixture
def mock_imap_connection():
    """Mock IMAP4_SSL connection."""
    mock_mail = MagicMock(spec=imaplib.IMAP4_SSL)
    mock_mail.login.return_value = ('OK', [b'Logged in'])
    mock_mail.select.return_value = ('OK', [b'1'])
    mock_mail.search.return_value = ('OK', [b'1 2 3'])
    mock_mail.list.return_value = ('OK', [b'(\\HasNoChildren) "/" "INBOX"'])
    mock_mail.create.return_value = ('OK', [b'Folder created'])
    mock_mail.logout.return_value = ('OK', [b'Logging out'])
    return mock_mail


@pytest.fixture
def sample_email_data():
    """Sample email data for testing."""
    return {
        'id': '1',
        'message_id': '<test123@gmail.com>',
        'subject': 'Test Email Subject',
        'sender': 'Test Sender <sender@example.com>',
        'date': 'Mon, 1 Jan 2024 12:00:00 +0000',
        'body': 'This is a test email body with some content.'
    }


@pytest.fixture
def urgent_email_data():
    """Urgent email data for testing."""
    return {
        'id': '2',
        'message_id': '<urgent123@gmail.com>',
        'subject': 'URGENT: Action Required',
        'sender': 'Boss <boss@company.com>',
        'date': 'Mon, 1 Jan 2024 12:00:00 +0000',
        'body': 'This is an urgent email that requires immediate attention.'
    }


@pytest.fixture
def newsletter_email_data():
    """Newsletter email data for testing."""
    return {
        'id': '3',
        'message_id': '<newsletter123@company.com>',
        'subject': 'Weekly Newsletter - Updates',
        'sender': 'Newsletter <news@company.com>',
        'date': 'Mon, 1 Jan 2024 12:00:00 +0000',
        'body': 'Unsubscribe from this newsletter at any time.'
    }


@pytest.fixture
def known_contacts():
    """Sample known contacts list."""
    return [
        'boss@company.com',
        'client@business.com',
        'teammate@company.com'
    ]
