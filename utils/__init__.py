"""Email validation and user input utilities"""

import re
from difflib import SequenceMatcher


def normalize_email(email):
    """Normalize email for consistent storage and comparison"""
    if not email:
        return ""
    return email.lower().strip()


def is_valid_email_format(email):
    """Validate email format with regex pattern"""
    if not email:
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_company_email(email, domain="@te.com"):
    """Check if email ends with company domain"""
    if not email:
        return False
    return email.lower().endswith(domain.lower())


def find_similar_email(email, existing_emails, threshold=0.85):
    """
    Find similar emails to detect typos using sequence matching.
    Returns the similar email if found, None otherwise.
    """
    normalized = normalize_email(email)

    for existing in existing_emails:
        existing_normalized = normalize_email(existing)
        # Skip exact matches
        if normalized == existing_normalized:
            continue

        # Calculate similarity ratio
        similarity = SequenceMatcher(None, normalized, existing_normalized).ratio()

        if similarity >= threshold:
            return existing

    return None


def get_email_suggestion(email):
    """
    Provide suggestions for common email typos.
    Returns suggested email or None.
    """
    normalized = normalize_email(email)

    # Common domain typos
    domain_corrections = {
        "@te.co": "@te.com",
        "@te.cm": "@te.com",
        "@te.con": "@te.com",
        "@t.com": "@te.com",
        "@tecom": "@te.com",
    }

    for wrong, correct in domain_corrections.items():
        if normalized.endswith(wrong):
            return normalized.replace(wrong, correct)

    return None


def validate_email_complete(email, existing_emails=None):
    """
    Complete email validation with all checks.
    Returns tuple: (is_valid, error_message, suggestion)
    """
    # Normalize first
    email = normalize_email(email)

    # Check if empty
    if not email:
        return False, "Email is required", None

    # Check format
    if not is_valid_email_format(email):
        return False, "Invalid email format. Please enter a valid email address.", None

    # Check company domain
    if not is_company_email(email):
        return False, "Only @te.com email addresses are allowed", None

    # Check for common typos in domain
    domain_suggestion = get_email_suggestion(email)
    if domain_suggestion:
        return False, f"Did you mean: {domain_suggestion}?", domain_suggestion

    # Check for similar existing emails (typo detection)
    if existing_emails:
        similar = find_similar_email(email, existing_emails)
        if similar:
            return False, f"An account with a similar email exists: {similar}", similar

    return True, None, None
