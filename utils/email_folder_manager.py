"""
Email Folder Manager

Manages email folders and moving messages using IMAP.
"""

import imaplib
import email
from typing import List, Tuple, Optional
from email.header import decode_header


class EmailFolderManager:
    """Manages email folders and moving messages using IMAP."""
    
    DEFAULT_FOLDER_MAPPING = {
        "URGENT": "Urgent",
        "IMPORTANT": "Important",
        "NEWSLETTER": "Newsletters",
        "PROMOTIONAL": "Promotions",
        "OTP_RECEIPT": "Receipts",
        "OTHER": "Archive"
    }
    
    def __init__(self, email_address: str, password: str, 
                 imap_server: str = "imap.gmail.com", imap_port: int = 993):
        """
        Initialize the email folder manager.
        
        Args:
            email_address: Email address for IMAP login
            password: App password for IMAP authentication
            imap_server: IMAP server hostname
            imap_port: IMAP server port (default: 993 for SSL)
        """
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.mail = None
    
    def connect(self) -> bool:
        """
        Connect to IMAP server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.mail.login(self.email_address, self.password)
            return True
        except Exception as e:
            print(f"IMAP connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from IMAP server."""
        if self.mail:
            try:
                self.mail.logout()
            except:
                pass
            self.mail = None
    
    def ensure_folders_exist(self) -> bool:
        """
        Create triage folders if they don't exist.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.mail:
            return False
        
        try:
            # List existing folders
            result, folders = self.mail.list()
            if result != 'OK':
                return False
            
            existing_folders = set()
            for folder in folders:
                # Decode folder name
                folder_str = folder.decode() if isinstance(folder, bytes) else folder
                # Extract folder name (last part after delimiter)
                parts = folder_str.split('"')
                if len(parts) >= 3:
                    existing_folders.add(parts[-2])
            
            # Create missing folders
            for folder_name in self.DEFAULT_FOLDER_MAPPING.values():
                if folder_name not in existing_folders:
                    try:
                        self.mail.create(folder_name)
                    except Exception as e:
                        print(f"Error creating folder {folder_name}: {e}")
            
            return True
        except Exception as e:
            print(f"Error ensuring folders exist: {e}")
            return False
    
    def decode_mime_header(self, header: str) -> str:
        """
        Decode MIME-encoded email header.
        
        Args:
            header: Raw header string
            
        Returns:
            Decoded string
        """
        if not header:
            return ""
        
        decoded_parts = decode_header(header)
        result = []
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                result.append(part.decode(encoding or 'utf-8', errors='ignore'))
            else:
                result.append(part)
        
        return ''.join(result)
    
    def search_emails(self, folder: str = "INBOX", limit: int = 10) -> List[Tuple[str, str, str]]:
        """
        Search for emails in a specific folder.
        
        Args:
            folder: Folder name to search
            limit: Maximum number of emails to return
            
        Returns:
            List of tuples: (message_id, subject, sender)
        """
        if not self.mail:
            return []
        
        try:
            # Select folder
            result, _ = self.mail.select(folder, readonly=True)
            if result != 'OK':
                return []
            
            # Search for all emails
            result, message_numbers = self.mail.search(None, 'ALL')
            if result != 'OK':
                return []
            
            # Get message IDs
            msg_ids = message_numbers[0].split()
            
            # Get most recent messages (up to limit)
            msg_ids = msg_ids[-limit:] if len(msg_ids) > limit else msg_ids
            msg_ids.reverse()  # Most recent first
            
            emails = []
            for msg_id in msg_ids:
                try:
                    # Fetch email
                    result, msg_data = self.mail.fetch(msg_id, '(RFC822)')
                    if result != 'OK':
                        continue
                    
                    # Parse email
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    subject = self.decode_mime_header(msg.get('Subject', 'No Subject'))
                    sender = self.decode_mime_header(msg.get('From', 'Unknown'))
                    
                    emails.append((msg_id.decode(), subject, sender))
                except Exception as e:
                    print(f"Error fetching email {msg_id}: {e}")
                    continue
            
            return emails
        except Exception as e:
            print(f"Error searching emails: {e}")
            return []
    
    def move_email(self, msg_id: str, from_folder: str, to_folder: str) -> bool:
        """
        Move an email from one folder to another.
        
        Args:
            msg_id: Message ID to move
            from_folder: Source folder
            to_folder: Destination folder
            
        Returns:
            True if successful, False otherwise
        """
        if not self.mail:
            return False
        
        try:
            # Select source folder
            result, _ = self.mail.select(from_folder)
            if result != 'OK':
                return False
            
            # Copy to destination
            result, _ = self.mail.copy(msg_id, to_folder)
            if result != 'OK':
                return False
            
            # Mark as deleted in source
            result, _ = self.mail.store(msg_id, '+FLAGS', '\\Deleted')
            if result != 'OK':
                return False
            
            # Expunge deleted messages
            self.mail.expunge()
            
            return True
        except Exception as e:
            print(f"Error moving email: {e}")
            return False
    
    def get_folder_for_category(self, category: str) -> str:
        """
        Map triage category to folder name.
        
        Args:
            category: Triage category
            
        Returns:
            Folder name
        """
        return self.DEFAULT_FOLDER_MAPPING.get(category, "Archive")
    
    def get_email_body(self, msg: email.message.Message) -> str:
        """
        Extract email body from message.
        
        Args:
            msg: Email message object
            
        Returns:
            Email body as string
        """
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Get text content
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                body = str(msg.get_payload())
        
        return body.strip()
    
    def fetch_recent_emails(self, folder: str = "INBOX", limit: int = 10) -> List[dict]:
        """
        Fetch recent emails with full details.
        
        Args:
            folder: Folder to fetch from
            limit: Maximum number of emails
            
        Returns:
            List of email dictionaries
        """
        if not self.mail:
            return []
        
        try:
            # Select folder
            result, _ = self.mail.select(folder, readonly=True)
            if result != 'OK':
                return []
            
            # Search for all emails
            result, message_numbers = self.mail.search(None, 'ALL')
            if result != 'OK':
                return []
            
            # Get message IDs
            msg_ids = message_numbers[0].split()
            
            # Get most recent messages
            msg_ids = msg_ids[-limit:] if len(msg_ids) > limit else msg_ids
            msg_ids.reverse()
            
            emails = []
            for msg_id in msg_ids:
                try:
                    # Fetch email
                    result, msg_data = self.mail.fetch(msg_id, '(RFC822)')
                    if result != 'OK':
                        continue
                    
                    # Parse email
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    email_dict = {
                        'id': msg_id.decode(),
                        'subject': self.decode_mime_header(msg.get('Subject', 'No Subject')),
                        'sender': self.decode_mime_header(msg.get('From', 'Unknown')),
                        'date': msg.get('Date', ''),
                        'body': self.get_email_body(msg),
                        'message_id': msg.get('Message-ID', '')
                    }
                    
                    emails.append(email_dict)
                except Exception as e:
                    print(f"Error fetching email {msg_id}: {e}")
                    continue
            
            return emails
        except Exception as e:
            print(f"Error fetching recent emails: {e}")
            return []
