"""
Email Sender

SMTP sending logic for email replies.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


def send_email(
    sender_email: str,
    sender_password: str,
    recipient_email: str,
    subject: str,
    body: str,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587,
    original_message_id: Optional[str] = None
) -> tuple[bool, str]:
    """
    Send an email via SMTP.
    
    Args:
        sender_email: Sender's email address
        sender_password: Sender's app password
        recipient_email: Recipient's email address
        subject: Email subject
        body: Email body (plain text)
        smtp_server: SMTP server hostname
        smtp_port: SMTP server port
        original_message_id: Original message ID for threading
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add In-Reply-To header for threading
        if original_message_id:
            msg['In-Reply-To'] = original_message_id
            msg['References'] = original_message_id
        
        # Attach body
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return True, "Email sent successfully!"
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Check your email and app password."
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


def validate_email_address(email: str) -> bool:
    """
    Basic email address validation.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid format, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
