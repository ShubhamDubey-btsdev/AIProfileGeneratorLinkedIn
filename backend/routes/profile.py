"""
Profile Routes
API endpoints for profile-related functionality
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.profile_service import ProfileService
from utils.response_formatter import create_response, create_error_response

# Create blueprint
profile_bp = Blueprint('profile', __name__)

# Initialize service
profile_service = ProfileService()


@profile_bp.route('/info', methods=['GET'])
def get_profile_info():
    """
    Get information about profile generation capabilities
    
    Returns:
        JSON response with feature information
    """
    try:
        service_status = profile_service.get_service_status()
        
        profile_info = {
            'features': {
                'linkedin_scraping': {
                    'available': True,
                    'description': 'Extract profile data from LinkedIn URLs',
                    'methods': ['URL direct', 'Name search', 'Manual database']
                },
                'ai_briefing': {
                    'available': service_status['ai_processor']['available'],
                    'description': 'Generate AI-powered briefings using Azure OpenAI',
                    'includes': [
                        'Executive summary',
                        'Key insights',
                        'Conversation starters',
                        'Meeting preparation notes',
                        'Strategic observations'
                    ]
                },
                'news_integration': {
                    'available': service_status['news_collector']['available'],
                    'description': 'Collect recent news articles about the person',
                    'source': 'NewsAPI integration'
                },
                'profile_validation': {
                    'available': True,
                    'description': 'Validates found profiles match searched names',
                    'includes': [
                        'Name matching',
                        'Nickname variations',
                        'Company account detection'
                    ]
                }
            },
            'supported_formats': {
                'input': {
                    'linkedin_url': 'Direct LinkedIn profile URLs',
                    'person_name': 'Full person names with optional company context',
                    'meeting_context': 'Optional context for targeted briefings'
                },
                'output': {
                    'json': 'Structured JSON response with all data',
                    'profile_data': 'LinkedIn profile information',
                    'briefing': 'AI-generated briefing with insights',
                    'news_articles': 'Related news articles array'
                }
            },
            'processing_capabilities': {
                'manual_database_profiles': 20,
                'nickname_variations': 30,
                'search_methods': 4,
                'max_processing_time': '30 seconds',
                'rate_limiting': 'Built-in delays for ethical scraping'
            }
        }
        
        return create_response(profile_info, 'Profile information retrieved')
        
    except Exception as e:
        return create_error_response(
            f'Internal server error: {str(e)}',
            500,
            {'error_type': 'profile_info_error'}
        )


@profile_bp.route('/status', methods=['GET'])
def get_profile_service_status():
    """
    Get detailed status of profile generation services
    
    Returns:
        JSON response with service component status
    """
    try:
        service_status = profile_service.get_service_status()
        
        # Add additional status information
        status_details = {
            'service_components': service_status,
            'overall_status': 'operational',
            'search_capabilities': {
                'url_based_search': True,
                'name_based_search': True,
                'manual_database_lookup': True,
                'google_search_integration': True,
                'duckduckgo_fallback': True,
                'smart_url_construction': True
            },
            'processing_features': {
                'profile_validation': True,
                'nickname_handling': True,
                'company_account_detection': True,
                'rate_limiting': True,
                'error_handling': True
            }
        }
        
        # Determine overall status
        critical_services = ['linkedin_scraper']
        all_critical_available = all(
            service_status[service]['available'] 
            for service in critical_services
        )
        
        if all_critical_available:
            status_details['overall_status'] = 'fully_operational'
        elif service_status['linkedin_scraper']['available']:
            status_details['overall_status'] = 'partially_operational'
        else:
            status_details['overall_status'] = 'limited_functionality'
        
        return create_response(status_details, 'Service status retrieved')
        
    except Exception as e:
        return create_error_response(
            f'Internal server error: {str(e)}',
            500,
            {'error_type': 'service_status_error'}
        )


@profile_bp.route('/examples', methods=['GET'])
def get_examples():
    """
    Get example requests and responses for the API
    
    Returns:
        JSON response with API usage examples
    """
    try:
        examples = {
            'search_by_url': {
                'description': 'Generate briefing from LinkedIn URL',
                'endpoint': '/api/search/by-url',
                'method': 'POST',
                'request_example': {
                    'linkedin_url': 'https://www.linkedin.com/in/satyanadella/',
                    'meeting_context': 'Partnership discussion with Microsoft'
                },
                'response_example': {
                    'success': True,
                    'message': 'Profile generated successfully',
                    'data': {
                        'linkedin_profile': {
                            'name': 'Satya Nadella',
                            'title': 'Chairman and CEO',
                            'company': 'Microsoft',
                            'url': 'https://www.linkedin.com/in/satyanadella/'
                        },
                        'briefing': {
                            'executive_summary': 'Satya Nadella is the Chairman and CEO of Microsoft...',
                            'key_insights': ['Technology leadership', 'Cloud transformation'],
                            'conversation_starters': ['Microsoft\'s AI strategy', 'Cloud adoption'],
                            'confidence_score': 95
                        },
                        'search_method': 'url_direct',
                        'processing_time': 8.5
                    }
                }
            },
            'search_by_name': {
                'description': 'Generate briefing by searching for person name',
                'endpoint': '/api/search/by-name',
                'method': 'POST',
                'request_example': {
                    'person_name': 'David Ackley',
                    'company_name': 'BTS',
                    'meeting_context': 'Partnership meeting'
                },
                'response_example': {
                    'success': True,
                    'message': 'Profile generated successfully',
                    'data': {
                        'linkedin_profile': {
                            'name': 'David Ackley',
                            'title': 'Executive',
                            'company': 'BTS',
                            'url': 'https://www.linkedin.com/in/daveackley/'
                        },
                        'briefing': {
                            'executive_summary': 'David Ackley is an executive at BTS...',
                            'key_insights': ['Business leadership', 'Industry expertise'],
                            'conversation_starters': ['BTS company growth', 'Market expansion'],
                            'confidence_score': 85
                        },
                        'search_method': 'manual_database',
                        'processing_time': 3.2
                    }
                }
            },
            'linkedin_url_only': {
                'description': 'Search for LinkedIn URL without full briefing',
                'endpoint': '/api/search/linkedin-url-only',
                'method': 'POST',
                'request_example': {
                    'person_name': 'Tim Cook',
                    'company_name': 'Apple'
                },
                'response_example': {
                    'success': True,
                    'message': 'LinkedIn URL search completed',
                    'data': {
                        'linkedin_url': 'https://www.linkedin.com/in/tim-cook-1b4ee/',
                        'person_name': 'Tim Cook',
                        'company_name': 'Apple',
                        'search_method': 'manual_database',
                        'found': True,
                        'processing_time': 0.5
                    }
                }
            },
            'validate_url': {
                'description': 'Validate LinkedIn URL format',
                'endpoint': '/api/search/validate-url',
                'method': 'POST',
                'request_example': {
                    'url': 'https://www.linkedin.com/in/example/'
                },
                'response_example': {
                    'success': True,
                    'message': 'URL validation completed',
                    'data': {
                        'url': 'https://www.linkedin.com/in/example/',
                        'is_valid': True,
                        'url_type': 'linkedin_profile'
                    }
                }
            }
        }
        
        return create_response(examples, 'API examples retrieved')
        
    except Exception as e:
        return create_error_response(
            f'Internal server error: {str(e)}',
            500,
            {'error_type': 'examples_error'}
        )


@profile_bp.route('/manual-database', methods=['GET'])
def get_manual_database_info():
    """
    Get information about the manual database of pre-loaded profiles
    
    Returns:
        JSON response with manual database information
    """
    try:
        # This would typically come from the actual database
        # For now, we'll provide general information
        manual_db_info = {
            'description': 'Pre-loaded LinkedIn URLs for common executives and public figures',
            'total_profiles': 20,
            'categories': {
                'tech_ceos': {
                    'count': 7,
                    'examples': ['Satya Nadella', 'Tim Cook', 'Sundar Pichai', 'Elon Musk']
                },
                'business_leaders': {
                    'count': 8,
                    'examples': ['Jeff Bezos', 'Warren Buffett', 'Richard Branson', 'Bill Gates']
                },
                'thought_leaders': {
                    'count': 5,
                    'examples': ['Simon Sinek', 'Daniel Pink', 'Adam Grant']
                }
            },
            'search_priority': 'Manual database is checked first for instant results',
            'accuracy': '100% for included profiles',
            'benefits': [
                'Instant lookup for common executives',
                'No search engine dependencies',
                'Handles nickname variations (e.g., Dave vs David)',
                'Reliable fallback when search engines fail'
            ],
            'expansion': 'Database can be easily expanded with additional profiles'
        }
        
        return create_response(manual_db_info, 'Manual database information retrieved')
        
    except Exception as e:
        return create_error_response(
            f'Internal server error: {str(e)}',
            500,
            {'error_type': 'manual_db_info_error'}
        ) 