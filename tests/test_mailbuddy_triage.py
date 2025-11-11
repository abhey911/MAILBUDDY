"""
Tests for Email Triage System

Unit tests for email classification functionality.
"""

import pytest
from utils.mailbuddy_triage import TriageTask, EmailTriageResult


class TestEmailTriageResult:
    """Test cases for EmailTriageResult model."""
    
    def test_create_result(self):
        """Test creating a triage result."""
        result = EmailTriageResult(
            category="URGENT",
            action="Move to Urgent",
            justification="From known contact with urgent keywords"
        )
        
        assert result.category == "URGENT"
        assert result.action == "Move to Urgent"
        assert "urgent" in result.justification.lower()


class TestTriageTask:
    """Test cases for TriageTask class."""
    
    def test_init(self, known_contacts):
        """Test TriageTask initialization."""
        triage = TriageTask(known_contacts)
        
        assert len(triage.known_contacts) == len(known_contacts)
        assert all(c.lower() in triage.known_contacts for c in known_contacts)
    
    def test_extract_email_address(self):
        """Test email extraction from sender string."""
        triage = TriageTask([])
        
        # Test with angle brackets
        result = triage._extract_email_address("John Doe <john@example.com>")
        assert result == "john@example.com"
        
        # Test plain email
        result = triage._extract_email_address("jane@example.com")
        assert result == "jane@example.com"
        
        # Test uppercase
        result = triage._extract_email_address("ADMIN@COMPANY.COM")
        assert result == "admin@company.com"
    
    def test_is_from_known_contact(self, known_contacts):
        """Test known contact detection."""
        triage = TriageTask(known_contacts)
        
        # Test known contact
        assert triage._is_from_known_contact("Boss <boss@company.com>") is True
        
        # Test unknown contact
        assert triage._is_from_known_contact("stranger@random.com") is False
        
        # Test case insensitivity
        assert triage._is_from_known_contact("BOSS@COMPANY.COM") is True
    
    def test_contains_keywords(self):
        """Test keyword detection."""
        triage = TriageTask([])
        
        text = "This is an URGENT message that requires immediate action"
        keywords = ['urgent', 'asap', 'immediately']
        
        assert triage._contains_keywords(text, keywords) is True
        assert triage._contains_keywords(text, ['newsletter']) is False
        assert triage._contains_keywords("", keywords) is False
    
    def test_triage_urgent_from_known_contact(self, known_contacts, urgent_email_data):
        """Test classification of urgent email from known contact."""
        triage = TriageTask(known_contacts)
        result = triage.run(urgent_email_data)
        
        assert result.category == "URGENT"
        assert "Urgent" in result.action
        assert "known contact" in result.justification.lower()
    
    def test_triage_newsletter(self, newsletter_email_data):
        """Test classification of newsletter."""
        triage = TriageTask([])
        result = triage.run(newsletter_email_data)
        
        assert result.category == "NEWSLETTER"
        assert "Newsletter" in result.action
        assert "newsletter" in result.justification.lower()
    
    def test_triage_promotional(self):
        """Test classification of promotional email."""
        triage = TriageTask([])
        
        email_data = {
            'subject': 'Big Sale - 50% OFF Today Only!',
            'sender': 'shop@store.com',
            'body': 'Limited time offer. Buy now and save!'
        }
        
        result = triage.run(email_data)
        
        assert result.category == "PROMOTIONAL"
        assert "Promotion" in result.action
    
    def test_triage_receipt(self):
        """Test classification of receipt/order confirmation."""
        triage = TriageTask([])
        
        email_data = {
            'subject': 'Order Confirmation #12345',
            'sender': 'orders@amazon.com',
            'body': 'Thank you for your purchase. Your order number is 12345.'
        }
        
        result = triage.run(email_data)
        
        assert result.category == "OTP_RECEIPT"
        assert "Receipt" in result.action
    
    def test_triage_otp(self):
        """Test classification of OTP email."""
        triage = TriageTask([])
        
        email_data = {
            'subject': 'Your verification code',
            'sender': 'noreply@service.com',
            'body': 'Your one-time password is: 123456'
        }
        
        result = triage.run(email_data)
        
        assert result.category == "OTP_RECEIPT"
    
    def test_triage_important_from_known(self, known_contacts):
        """Test classification of non-urgent email from known contact."""
        triage = TriageTask(known_contacts)
        
        email_data = {
            'subject': 'Meeting notes from yesterday',
            'sender': 'Boss <boss@company.com>',
            'body': 'Here are the notes we discussed.'
        }
        
        result = triage.run(email_data)
        
        assert result.category == "IMPORTANT"
        assert "Important" in result.action
    
    def test_triage_important_with_urgent_keywords(self):
        """Test classification with urgent keywords but unknown sender."""
        triage = TriageTask([])
        
        email_data = {
            'subject': 'Important deadline approaching',
            'sender': 'stranger@random.com',
            'body': 'This requires immediate attention.'
        }
        
        result = triage.run(email_data)
        
        assert result.category == "IMPORTANT"
    
    def test_triage_other(self):
        """Test classification of generic email."""
        triage = TriageTask([])
        
        email_data = {
            'subject': 'Just saying hi',
            'sender': 'random@email.com',
            'body': 'Hope you are doing well.'
        }
        
        result = triage.run(email_data)
        
        assert result.category == "OTHER"
        assert "Archive" in result.action
    
    def test_triage_empty_email(self):
        """Test handling of empty email data."""
        triage = TriageTask([])
        
        email_data = {
            'subject': '',
            'sender': '',
            'body': ''
        }
        
        result = triage.run(email_data)
        
        # Should default to OTHER category
        assert result.category == "OTHER"
    
    def test_triage_missing_fields(self):
        """Test handling of missing email fields."""
        triage = TriageTask([])
        
        email_data = {}
        
        # Should not crash and return a result
        result = triage.run(email_data)
        assert isinstance(result, EmailTriageResult)
        assert result.category in ["URGENT", "IMPORTANT", "NEWSLETTER", 
                                   "PROMOTIONAL", "OTP_RECEIPT", "OTHER"]
