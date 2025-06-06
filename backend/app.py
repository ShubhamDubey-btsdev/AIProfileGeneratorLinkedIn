"""
Flask API for AI Profile Generator
Main application file that sets up routes and CORS
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime
import traceback

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.search import search_bp
from routes.profile import profile_bp
from utils.response_formatter import create_response, create_error_response

app = Flask(__name__)

# Enable CORS for all domains on all routes
CORS(app)

# Configure Flask
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Register blueprints
app.register_blueprint(search_bp, url_prefix='/api/search')
app.register_blueprint(profile_bp, url_prefix='/api/profile')

@app.route('/')
def home():
    """Root endpoint with API information"""
    return create_response({
        'service': 'AI Profile Generator API',
        'version': '1.0.0',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'health': '/api/health',
            'search_by_url': '/api/search/by-url',
            'search_by_name': '/api/search/by-name',
            'profile_info': '/api/profile/info'
        }
    }, 'API is running successfully')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return create_response({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'AI Profile Generator API',
        'components': {
            'linkedin_scraper': 'available',
            'ai_processor': 'available',
            'news_collector': 'available'
        }
    }, 'Service is healthy')

@app.route('/api/status')
def status():
    """Detailed status endpoint"""
    try:
        # Import and test components
        from linkedin_scraper import LinkedInScraper
        from ai_processor import AIProcessor
        from news_collector import NewsCollector
        from config import AZURE_OPENAI_KEY, NEWS_API_KEY
        
        # Test component initialization
        linkedin_scraper = LinkedInScraper()
        ai_processor = AIProcessor()
        news_collector = NewsCollector()
        
        status_data = {
            'service': 'AI Profile Generator API',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'linkedin_scraper': {
                    'status': 'ready',
                    'description': 'LinkedIn profile extraction and search'
                },
                'ai_processor': {
                    'status': 'ready' if ai_processor.client_ready else 'needs_config',
                    'description': 'Azure OpenAI integration',
                    'configured': bool(AZURE_OPENAI_KEY and AZURE_OPENAI_KEY != 'your_azure_openai_key_here')
                },
                'news_collector': {
                    'status': 'ready' if news_collector.api_key_configured else 'needs_config',
                    'description': 'News API integration',
                    'configured': bool(NEWS_API_KEY and NEWS_API_KEY != 'your_news_api_key_here')
                }
            },
            'features': {
                'url_search': True,
                'name_search': True,
                'manual_database': True,
                'profile_validation': True,
                'ai_briefing': ai_processor.client_ready,
                'news_collection': news_collector.api_key_configured
            }
        }
        
        return create_response(status_data, 'Status check completed')
        
    except Exception as e:
        return create_error_response(
            f'Status check failed: {str(e)}',
            500,
            {'error_type': 'component_initialization_error'}
        )

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return create_error_response(
        'Endpoint not found',
        404,
        {'available_endpoints': [
            '/api/health',
            '/api/status',
            '/api/search/by-url',
            '/api/search/by-name'
        ]}
    )

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return create_error_response(
        'Internal server error',
        500,
        {'error_details': str(error)}
    )

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all uncaught exceptions"""
    app.logger.error(f'Unhandled exception: {str(e)}')
    app.logger.error(traceback.format_exc())
    
    return create_error_response(
        'An unexpected error occurred',
        500,
        {
            'error_type': type(e).__name__,
            'error_message': str(e)
        }
    )

if __name__ == '__main__':
    print("🚀 Starting AI Profile Generator API...")
    print("📍 Available at: http://localhost:5000")
    print("📋 Health check: http://localhost:5000/api/health")
    print("📊 Status check: http://localhost:5000/api/status")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    ) 