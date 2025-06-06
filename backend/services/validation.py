"""
Validation Service
Input validation for API requests
"""

import re
from urllib.parse import urlparse


def validate_search_by_url_request(data):
    """
    Validate search by URL request data
    
    Args:
        data: Request data dict
        
    Returns:
        tuple: (is_valid, errors_list)
    """
    errors = []
    
    # Check if linkedin_url is provided
    if not data.get('linkedin_url'):
        errors.append('linkedin_url is required')
    else:
        linkedin_url = data['linkedin_url'].strip()
        
        # Validate URL format
        if not validate_linkedin_url_format(linkedin_url):
            errors.append('Invalid LinkedIn URL format. Must be a valid LinkedIn profile URL')
    
    # Validate meeting_context if provided
    meeting_context = data.get('meeting_context', '')
    if meeting_context and len(meeting_context) > 1000:
        errors.append('meeting_context must be less than 1000 characters')
    
    return len(errors) == 0, errors


def validate_search_by_name_request(data):
    """
    Validate search by name request data
    
    Args:
        data: Request data dict
        
    Returns:
        tuple: (is_valid, errors_list)
    """
    errors = []
    
    # Check if person_name is provided
    if not data.get('person_name'):
        errors.append('person_name is required')
    else:
        person_name = data['person_name'].strip()
        
        # Validate name format
        if len(person_name) < 2:
            errors.append('person_name must be at least 2 characters long')
        elif len(person_name) > 100:
            errors.append('person_name must be less than 100 characters')
        elif not validate_person_name_format(person_name):
            errors.append('person_name contains invalid characters')
    
    # Validate company_name if provided
    company_name = data.get('company_name', '')
    if company_name:
        company_name = company_name.strip()
        if len(company_name) > 100:
            errors.append('company_name must be less than 100 characters')
        elif not validate_company_name_format(company_name):
            errors.append('company_name contains invalid characters')
    
    # Validate meeting_context if provided
    meeting_context = data.get('meeting_context', '')
    if meeting_context and len(meeting_context) > 1000:
        errors.append('meeting_context must be less than 1000 characters')
    
    return len(errors) == 0, errors


def validate_linkedin_url_format(url):
    """
    Validate LinkedIn URL format
    
    Args:
        url: URL string to validate
        
    Returns:
        bool: True if valid LinkedIn URL
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        # Parse URL
        parsed = urlparse(url.strip())
        
        # Check if it's a valid URL
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # Check if it's LinkedIn
        if 'linkedin.com' not in parsed.netloc.lower():
            return False
        
        # Check if it's a profile URL
        if '/in/' not in parsed.path:
            return False
        
        return True
        
    except Exception:
        return False


def validate_person_name_format(name):
    """
    Validate person name format
    
    Args:
        name: Name string to validate
        
    Returns:
        bool: True if valid name format
    """
    if not name or not isinstance(name, str):
        return False
    
    # Allow letters, spaces, hyphens, apostrophes, and periods
    # Common in names like "Mary-Jane", "O'Connor", "Jr.", etc.
    pattern = r"^[A-Za-z\s\-'\.]+$"
    
    return bool(re.match(pattern, name.strip()))


def validate_company_name_format(company):
    """
    Validate company name format
    
    Args:
        company: Company name string to validate
        
    Returns:
        bool: True if valid company name format
    """
    if not company or not isinstance(company, str):
        return False
    
    # Allow letters, numbers, spaces, common punctuation for company names
    # Examples: "AT&T", "3M Company", "Johnson & Johnson", etc.
    pattern = r"^[A-Za-z0-9\s\-'\.&,()]+$"
    
    return bool(re.match(pattern, company.strip()))


def sanitize_input(text, max_length=None):
    """
    Sanitize text input
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Strip whitespace
    sanitized = text.strip()
    
    # Limit length if specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def validate_request_data(data, required_fields=None):
    """
    General request data validation
    
    Args:
        data: Request data dict
        required_fields: List of required field names
        
    Returns:
        tuple: (is_valid, errors_list)
    """
    errors = []
    
    if not isinstance(data, dict):
        errors.append('Request data must be a JSON object')
        return False, errors
    
    # Check required fields
    if required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f'{field} is required')
    
    return len(errors) == 0, errors 