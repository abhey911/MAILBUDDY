"""
Contact Management Utilities

Load and save known contacts for email triage.
"""

import json
import os
from typing import List


def get_contacts_file_path() -> str:
    """Get the path to the known contacts JSON file."""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(current_dir, "data", "known_contacts.json")


def load_contacts() -> List[str]:
    """
    Load known contacts from JSON file.
    
    Returns:
        List of email addresses (lowercase)
    """
    file_path = get_contacts_file_path()
    
    if not os.path.exists(file_path):
        # Create default empty file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        save_contacts([])
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            contacts = data.get("known_contacts", [])
            # Normalize to lowercase
            return [email.lower().strip() for email in contacts]
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading contacts: {e}")
        return []


def save_contacts(contacts: List[str]) -> bool:
    """
    Save known contacts to JSON file.
    
    Args:
        contacts: List of email addresses
        
    Returns:
        True if successful, False otherwise
    """
    file_path = get_contacts_file_path()
    
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Normalize and deduplicate
        normalized = list(set(email.lower().strip() for email in contacts))
        
        data = {
            "known_contacts": sorted(normalized)
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return True
    except IOError as e:
        print(f"Error saving contacts: {e}")
        return False


def add_contact(email: str) -> bool:
    """
    Add a contact to the known contacts list.
    
    Args:
        email: Email address to add
        
    Returns:
        True if successful, False otherwise
    """
    contacts = load_contacts()
    email = email.lower().strip()
    
    if email not in contacts:
        contacts.append(email)
        return save_contacts(contacts)
    
    return True


def remove_contact(email: str) -> bool:
    """
    Remove a contact from the known contacts list.
    
    Args:
        email: Email address to remove
        
    Returns:
        True if successful, False otherwise
    """
    contacts = load_contacts()
    email = email.lower().strip()
    
    if email in contacts:
        contacts.remove(email)
        return save_contacts(contacts)
    
    return True
