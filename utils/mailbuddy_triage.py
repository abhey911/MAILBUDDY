"""
Email Triage Engine

Rule-based email classification system.
"""

from pydantic import BaseModel
from typing import List, Dict
import re


class EmailTriageResult(BaseModel):
    """Pydantic model for triage output."""
    category: str
    action: str
    justification: str


class TriageTask:
    """Rule-based email classification."""
    
    # Keywords for different categories
    URGENT_KEYWORDS = [
        'urgent', 'asap', 'immediately', 'critical', 'emergency', 
        'important', 'deadline', 'action required', 'time sensitive'
    ]
    
    NEWSLETTER_KEYWORDS = [
        'unsubscribe', 'newsletter', 'weekly digest', 'subscription',
        'update from', 'mailing list', 'email preferences'
    ]
    
    PROMOTIONAL_KEYWORDS = [
        'sale', 'discount', 'offer', 'deal', 'promotion', 'coupon',
        'free shipping', 'limited time', '% off', 'buy now', 'shop now'
    ]
    
    RECEIPT_KEYWORDS = [
        'receipt', 'order confirmation', 'invoice', 'payment',
        'transaction', 'purchase', 'your order', 'order number',
        'tracking number', 'shipped', 'delivery'
    ]
    
    OTP_PATTERNS = [
        r'\b\d{4,6}\b',  # 4-6 digit codes
        r'verification code',
        r'one-time password',
        r'OTP',
        r'security code'
    ]
    
    def __init__(self, known_contacts: List[str]):
        """
        Initialize triage task.
        
        Args:
            known_contacts: List of known contact email addresses (lowercase)
        """
        self.known_contacts = set(c.lower() for c in known_contacts)
    
    def _extract_email_address(self, sender: str) -> str:
        """
        Extract email address from sender string.
        
        Args:
            sender: Sender string (e.g., "Name <email@example.com>")
            
        Returns:
            Email address
        """
        # Try to extract email from format: "Name <email@example.com>"
        match = re.search(r'<(.+?)>', sender)
        if match:
            return match.group(1).lower()
        return sender.lower()
    
    def _is_from_known_contact(self, sender: str) -> bool:
        """
        Check if email is from a known contact.
        
        Args:
            sender: Sender email or name <email>
            
        Returns:
            True if from known contact
        """
        email = self._extract_email_address(sender)
        return email in self.known_contacts
    
    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """
        Check if text contains any of the keywords.
        
        Args:
            text: Text to search
            keywords: List of keywords
            
        Returns:
            True if any keyword found
        """
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    def _matches_pattern(self, text: str, patterns: List[str]) -> bool:
        """
        Check if text matches any regex pattern.
        
        Args:
            text: Text to search
            patterns: List of regex patterns
            
        Returns:
            True if any pattern matches
        """
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def run(self, email_data: Dict) -> EmailTriageResult:
        """
        Classify email into category.
        
        Args:
            email_data: Dictionary with 'subject', 'sender', 'body'
            
        Returns:
            EmailTriageResult with category, action, and justification
        """
        subject = email_data.get('subject', '')
        sender = email_data.get('sender', '')
        body = email_data.get('body', '')
        
        combined_text = f"{subject} {body}"
        
        # Check for OTP/receipts first (highest priority)
        if self._matches_pattern(combined_text, self.OTP_PATTERNS):
            return EmailTriageResult(
                category="OTP_RECEIPT",
                action="Move to Receipts",
                justification="Contains OTP or verification code"
            )
        
        if self._contains_keywords(combined_text, self.RECEIPT_KEYWORDS):
            return EmailTriageResult(
                category="OTP_RECEIPT",
                action="Move to Receipts",
                justification="Appears to be a receipt or order confirmation"
            )
        
        # Check for urgent emails
        is_from_known = self._is_from_known_contact(sender)
        has_urgent_keywords = self._contains_keywords(combined_text, self.URGENT_KEYWORDS)
        
        if is_from_known and has_urgent_keywords:
            return EmailTriageResult(
                category="URGENT",
                action="Move to Urgent",
                justification="From known contact with urgent keywords"
            )
        
        if has_urgent_keywords:
            return EmailTriageResult(
                category="IMPORTANT",
                action="Move to Important",
                justification="Contains urgent keywords"
            )
        
        if is_from_known:
            return EmailTriageResult(
                category="IMPORTANT",
                action="Move to Important",
                justification="From known contact"
            )
        
        # Check for newsletters
        if self._contains_keywords(combined_text, self.NEWSLETTER_KEYWORDS):
            return EmailTriageResult(
                category="NEWSLETTER",
                action="Move to Newsletters",
                justification="Appears to be a newsletter or subscription"
            )
        
        # Check for promotional emails
        if self._contains_keywords(combined_text, self.PROMOTIONAL_KEYWORDS):
            return EmailTriageResult(
                category="PROMOTIONAL",
                action="Move to Promotions",
                justification="Contains promotional keywords"
            )
        
        # Default: archive
        return EmailTriageResult(
            category="OTHER",
            action="Move to Archive",
            justification="General email, no specific category matched"
        )
