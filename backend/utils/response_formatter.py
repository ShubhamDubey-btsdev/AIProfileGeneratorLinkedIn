"""
Response Formatter Utility
Standardizes API responses across all endpoints
"""

from flask import jsonify
from datetime import datetime


def create_response(data=None, message="Success", status_code=200):
    """
    Create standardized success response
    
    Args:
        data: Response data (dict, list, etc.)
        message: Success message
        status_code: HTTP status code
    
    Returns:
        Flask JSON response
    """
    response_data = {
        'success': True,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    
    return jsonify(response_data), status_code


def create_error_response(message="An error occurred", status_code=400, details=None):
    """
    Create standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        details: Additional error details (dict)
    
    Returns:
        Flask JSON response
    """
    response_data = {
        'success': False,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'error': {
            'code': status_code,
            'message': message
        }
    }
    
    if details:
        response_data['error']['details'] = details
    
    return jsonify(response_data), status_code


def create_validation_error_response(validation_errors):
    """
    Create standardized validation error response
    
    Args:
        validation_errors: List of validation error messages
    
    Returns:
        Flask JSON response
    """
    return create_error_response(
        "Validation failed",
        400,
        {
            'validation_errors': validation_errors,
            'error_type': 'validation_error'
        }
    )


def create_profile_response(linkedin_profile, briefing, news_articles, search_method, processing_time):
    """
    Create standardized profile generation response
    
    Args:
        linkedin_profile: LinkedIn profile data
        briefing: AI-generated briefing
        news_articles: Related news articles
        search_method: Method used to find profile
        processing_time: Time taken to process request
    
    Returns:
        Flask JSON response
    """
    data = {
        'linkedin_profile': linkedin_profile,
        'briefing': briefing,
        'news_articles': news_articles,
        'search_method': search_method,
        'processing_time': round(processing_time, 2),
        'profile_found': bool(linkedin_profile),
        'briefing_generated': bool(briefing),
        'news_found': len(news_articles) if news_articles else 0
    }
    
    message = "Profile generated successfully"
    if not linkedin_profile:
        message = "Profile not found"
    elif not briefing:
        message = "Profile found but briefing generation failed"
    
    return create_response(data, message) 