"""
Tests for Email Folder Manager

Unit tests for IMAP folder management functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from utils.email_folder_manager import EmailFolderManager


class TestEmailFolderManager:
    """Test cases for EmailFolderManager class."""
    
    def test_init(self):
        """Test EmailFolderManager initialization."""
        manager = EmailFolderManager(
            "test@gmail.com",
            "test_password",
            "imap.gmail.com",
            993
        )
        
        assert manager.email_address == "test@gmail.com"
        assert manager.password == "test_password"
        assert manager.imap_server == "imap.gmail.com"
        assert manager.imap_port == 993
        assert manager.mail is None
    
    @patch('utils.email_folder_manager.imaplib.IMAP4_SSL')
    def test_connect_success(self, mock_imap_ssl, mock_imap_connection):
        """Test successful IMAP connection."""
        mock_imap_ssl.return_value = mock_imap_connection
        
        manager = EmailFolderManager("test@gmail.com", "password")
        result = manager.connect()
        
        assert result is True
        assert manager.mail is not None
        mock_imap_ssl.assert_called_once_with("imap.gmail.com", 993)
        mock_imap_connection.login.assert_called_once_with("test@gmail.com", "password")
    
    @patch('utils.email_folder_manager.imaplib.IMAP4_SSL')
    def test_connect_failure(self, mock_imap_ssl):
        """Test failed IMAP connection."""
        mock_imap_ssl.side_effect = Exception("Connection failed")
        
        manager = EmailFolderManager("test@gmail.com", "password")
        result = manager.connect()
        
        assert result is False
        assert manager.mail is None
    
    def test_disconnect(self, mock_imap_connection):
        """Test IMAP disconnection."""
        manager = EmailFolderManager("test@gmail.com", "password")
        manager.mail = mock_imap_connection
        
        manager.disconnect()
        
        mock_imap_connection.logout.assert_called_once()
        assert manager.mail is None
    
    @patch('utils.email_folder_manager.imaplib.IMAP4_SSL')
    def test_ensure_folders_exist(self, mock_imap_ssl, mock_imap_connection):
        """Test folder creation."""
        mock_imap_ssl.return_value = mock_imap_connection
        
        manager = EmailFolderManager("test@gmail.com", "password")
        manager.connect()
        
        result = manager.ensure_folders_exist()
        
        assert result is True
        # Should attempt to create folders
        assert mock_imap_connection.create.call_count > 0
    
    def test_get_folder_for_category(self):
        """Test category to folder mapping."""
        manager = EmailFolderManager("test@gmail.com", "password")
        
        assert manager.get_folder_for_category("URGENT") == "Urgent"
        assert manager.get_folder_for_category("IMPORTANT") == "Important"
        assert manager.get_folder_for_category("NEWSLETTER") == "Newsletters"
        assert manager.get_folder_for_category("PROMOTIONAL") == "Promotions"
        assert manager.get_folder_for_category("OTP_RECEIPT") == "Receipts"
        assert manager.get_folder_for_category("OTHER") == "Archive"
        assert manager.get_folder_for_category("UNKNOWN") == "Archive"
    
    def test_decode_mime_header(self):
        """Test MIME header decoding."""
        manager = EmailFolderManager("test@gmail.com", "password")
        
        # Test simple ASCII
        result = manager.decode_mime_header("Test Subject")
        assert result == "Test Subject"
        
        # Test empty header
        result = manager.decode_mime_header("")
        assert result == ""
        
        # Test None
        result = manager.decode_mime_header(None)
        assert result == ""
    
    @patch('utils.email_folder_manager.imaplib.IMAP4_SSL')
    def test_move_email(self, mock_imap_ssl, mock_imap_connection):
        """Test moving email between folders."""
        mock_imap_ssl.return_value = mock_imap_connection
        mock_imap_connection.copy.return_value = ('OK', [b'Copied'])
        mock_imap_connection.store.return_value = ('OK', [b'Stored'])
        
        manager = EmailFolderManager("test@gmail.com", "password")
        manager.connect()
        
        result = manager.move_email("1", "INBOX", "Urgent")
        
        assert result is True
        mock_imap_connection.select.assert_called_with("INBOX")
        mock_imap_connection.copy.assert_called_with("1", "Urgent")
        mock_imap_connection.store.assert_called_with("1", '+FLAGS', '\\Deleted')
        mock_imap_connection.expunge.assert_called_once()
