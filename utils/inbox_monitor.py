"""
Inbox Monitor

Background service that monitors inbox for new emails.
"""

import threading
import time
from typing import List, Dict, Callable, Optional
from datetime import datetime


class InboxMonitor:
    """Background service that monitors inbox for new emails."""
    
    def __init__(self, folder_manager, check_interval_seconds: int = 300):
        """
        Initialize the inbox monitor.
        
        Args:
            folder_manager: EmailFolderManager instance
            check_interval_seconds: Interval between checks (default: 300 = 5 minutes)
        """
        self.folder_manager = folder_manager
        self.check_interval_seconds = check_interval_seconds
        self.is_running = False
        self.monitor_thread = None
        self.seen_message_ids = set()
        self.last_check_time = None
        self.new_emails_callback = None
        self.lock = threading.Lock()
    
    def set_new_emails_callback(self, callback: Callable[[List[Dict]], None]):
        """
        Register callback for when new emails are detected.
        
        Args:
            callback: Function to call with list of new emails
        """
        self.new_emails_callback = callback
    
    def check_for_new_emails(self) -> List[Dict]:
        """
        Poll IMAP and fetch new emails.
        
        Returns:
            List of new email dictionaries
        """
        try:
            # Fetch recent emails
            all_emails = self.folder_manager.fetch_recent_emails("INBOX", limit=20)
            
            # Filter out emails we've already seen
            new_emails = []
            with self.lock:
                for email_data in all_emails:
                    msg_id = email_data.get('message_id', email_data.get('id'))
                    if msg_id and msg_id not in self.seen_message_ids:
                        new_emails.append(email_data)
                        self.seen_message_ids.add(msg_id)
                
                self.last_check_time = datetime.now()
            
            return new_emails
        except Exception as e:
            print(f"Error checking for new emails: {e}")
            return []
    
    def _monitor_loop(self):
        """Background thread loop that checks for new emails."""
        while self.is_running:
            try:
                # Check for new emails
                new_emails = self.check_for_new_emails()
                
                # Call callback if new emails found
                if new_emails and self.new_emails_callback:
                    self.new_emails_callback(new_emails)
                
                # Sleep for interval
                sleep_count = 0
                while self.is_running and sleep_count < self.check_interval_seconds:
                    time.sleep(1)
                    sleep_count += 1
            except Exception as e:
                print(f"Error in monitor loop: {e}")
                time.sleep(10)  # Wait a bit before retrying
    
    def start(self):
        """Start the monitoring service."""
        if self.is_running:
            return
        
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop(self):
        """Stop the monitoring service."""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            self.monitor_thread = None
    
    def get_status(self) -> Dict:
        """
        Get current monitoring status.
        
        Returns:
            Dictionary with status information
        """
        with self.lock:
            return {
                'running': self.is_running,
                'last_check_time': self.last_check_time,
                'emails_seen_count': len(self.seen_message_ids),
                'check_interval_seconds': self.check_interval_seconds
            }
    
    def set_check_interval(self, seconds: int):
        """
        Update the check interval.
        
        Args:
            seconds: New interval in seconds
        """
        self.check_interval_seconds = max(60, min(1800, seconds))  # Clamp between 1-30 min
    
    def reset_seen_messages(self):
        """Reset the seen messages cache."""
        with self.lock:
            self.seen_message_ids.clear()
