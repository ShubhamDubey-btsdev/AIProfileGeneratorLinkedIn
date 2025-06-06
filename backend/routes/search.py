"""
Search Routes
API endpoints for LinkedIn profile search functionality
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.profile_service import ProfileService
from services.validation import (
    validate_search_by_url_request, 
    validate_search_by_name_request,
    sanitize_input
)
from utils.response_formatter import (
    create_response, 
    create_error_response, 
    create_validation_error_response,
    create_profile_response
)

# Create blueprint
search_bp = Blueprint('search', __name__)

# Initialize service
profile_service = ProfileService()


@search_bp.route('/by-url', methods=['POST'])
def search_by_url():
    """
    Search and generate profile briefing by LinkedIn URL
    
    Request Body:
    {
        "linkedin_url": "https://linkedin.com/in/username/",
        "meeting_context": "Partnership discussion" (optional)
    }
    
    Returns:
        JSON response with profile data and briefing
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return create_error_response('Request body must contain JSON data', 400)
        
        # Validate request data
        is_valid, validation_errors = validate_search_by_url_request(data)
        if not is_valid:
            return create_validation_error_response(validation_errors)
        
        # Sanitize inputs
        linkedin_url = sanitize_input(data['linkedin_url'])
        meeting_context = sanitize_input(data.get('meeting_context', ''), 1000)
        
        # Generate profile
        result = profile_service.generate_profile_from_url(
            linkedin_url, 
            meeting_context
        )
        
        # Handle errors
        if result.get('error'):
            return create_error_response(
                result['error'], 
                400,
                {
                    'search_method': result.get('search_method'),
                    'processing_time': result.get('processing_time')
                }
            )
        
        # Return successful response
        return create_profile_response(
            result.get('linkedin_profile'),
            result.get('briefing'),
            result.get('news_articles', []),
            result.get('search_method'),
            result.get('processing_time')
        )
        
    except Exception as e:
        return create_error_response(
            f'Internal server error: {str(e)}',
            500,
            {'error_type': 'search_by_url_error'}
        )


@search_bp.route('/by-name', methods=['POST'])
def search_by_name():
    """
    Search and generate profile briefing by person name
    
    Request Body:
    {
        "person_name": "David Ackley",
        "company_name": "BTS" (optional),
        "meeting_context": "Partnership meeting" (optional)
    }
    
    Returns:
        JSON response with profile data and briefing
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return create_error_response('Request body must contain JSON data', 400)
        
        # Validate request data
        is_valid, validation_errors = validate_search_by_name_request(data)
        if not is_valid:
            return create_validation_error_response(validation_errors)
        
        # Sanitize inputs
        person_name = sanitize_input(data['person_name'], 100)
        company_name = sanitize_input(data.get('company_name', ''), 100)
        meeting_context = sanitize_input(data.get('meeting_context', ''), 1000)
        
        # Generate profile
        result = profile_service.generate_profile_from_name(
            person_name,
            company_name, 
            meeting_context
        )
        
        # Handle errors
        if result.get('error'):
            return create_error_response(
                result['error'], 
                400,
                {
                    'search_method': result.get('search_method'),
                    'processing_time': result.get('processing_time'),
                    'search_details': {
                        'person_name': person_name,
                        'company_name': company_name
                    }
                }
            )
        
        # Return successful response
        return create_profile_response(
            result.get('linkedin_profile'),
            result.get('briefing'),
            result.get('news_articles', []),
            result.get('search_method'),
            result.get('processing_time')
        )
        
    except Exception as e:
        return create_error_response(
            f'Internal server error: {str(e)}',
            500,
            {'error_type': 'search_by_name_error'}
        )


@search_bp.route('/linkedin-url-only', methods=['POST'])
def search_linkedin_url_only():
    """
    Search for LinkedIn URL only (without generating full briefing)
    
    Request Body:
    {
        "person_name": "David Ackley",
        "company_name": "BTS" (optional)
    }
    
    Returns:
        JSON response with LinkedIn URL if found
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return create_error_response('Request body must contain JSON data', 400)
        
        # Validate basic requirements
        if not data.get('person_name'):
            return create_validation_error_response(['person_name is required'])
        
        # Sanitize inputs
        person_name = sanitize_input(data['person_name'], 100)
        company_name = sanitize_input(data.get('company_name', ''), 100)
        
        # Search for LinkedIn URL only
        result = profile_service.search_linkedin_profile_only(person_name, company_name)
        
        if result.get('error'):
            return create_error_response(
                result['error'],
                400,
                {
                    'search_method': result.get('search_method'),
                    'processing_time': result.get('processing_time')
                }
            )
        
        # Return result
        return create_response(
            result,
            'LinkedIn URL search completed' if result.get('found') else 'LinkedIn URL not found'
        )
        
    except Exception as e:
        return create_error_response(
            f'Internal server error: {str(e)}',
            500,
            {'error_type': 'linkedin_url_search_error'}
        )


@search_bp.route('/validate-url', methods=['POST'])
def validate_linkedin_url():
    """
    Validate if a URL is a valid LinkedIn profile URL
    
    Request Body:
    {
        "url": "https://linkedin.com/in/username/"
    }
    
    Returns:
        JSON response with validation result
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or not data.get('url'):
            return create_validation_error_response(['url is required'])
        
        url = sanitize_input(data['url'])
        
        # Validate URL
        is_valid = profile_service.validate_linkedin_url(url)
        
        return create_response(
            {
                'url': url,
                'is_valid': is_valid,
                'url_type': 'linkedin_profile' if is_valid else 'invalid'
            },
            'URL validation completed'
        )
        
    except Exception as e:
        return create_error_response(
            f'Internal server error: {str(e)}',
            500,
            {'error_type': 'url_validation_error'}
        )


@search_bp.route('/methods', methods=['GET'])
def get_search_methods():
    """
    Get information about available search methods
    
    Returns:
        JSON response with search method details
    """
    try:
        methods_info = {
            'search_methods': [
                {
                    'name': 'by_url',
                    'endpoint': '/api/search/by-url',
                    'method': 'POST',
                    'description': 'Generate profile briefing from LinkedIn URL',
                    'required_fields': ['linkedin_url'],
                    'optional_fields': ['meeting_context']
                },
                {
                    'name': 'by_name',
                    'endpoint': '/api/search/by-name',
                    'method': 'POST',
                    'description': 'Generate profile briefing by searching for person name',
                    'required_fields': ['person_name'],
                    'optional_fields': ['company_name', 'meeting_context']
                },
                {
                    'name': 'linkedin_url_only',
                    'endpoint': '/api/search/linkedin-url-only',
                    'method': 'POST',
                    'description': 'Search for LinkedIn URL without generating full briefing',
                    'required_fields': ['person_name'],
                    'optional_fields': ['company_name']
                },
                {
                    'name': 'validate_url',
                    'endpoint': '/api/search/validate-url',
                    'method': 'POST',
                    'description': 'Validate if URL is a valid LinkedIn profile URL',
                    'required_fields': ['url'],
                    'optional_fields': []
                }
            ],
            'search_features': {
                'manual_database': 'Pre-loaded profiles for common executives',
                'google_search': 'Google search integration for profile discovery',
                'duckduckgo_fallback': 'DuckDuckGo search as fallback method',
                'url_construction': 'Smart URL construction with nickname variations',
                'profile_validation': 'Validates found profiles match searched names'
            }
        }
        
        return create_response(methods_info, 'Search methods information retrieved')
        
    except Exception as e:
        return create_error_response(
            f'Internal server error: {str(e)}',
            500,
            {'error_type': 'methods_info_error'}
        ) 