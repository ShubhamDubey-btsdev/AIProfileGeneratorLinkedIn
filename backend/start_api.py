#!/usr/bin/env python3
"""
Startup script for AI Profile Generator Flask API
"""

import os
import sys

# Add parent directory to path to import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app import app

def main():
    """Main function to start the Flask API"""
    
    print("🚀 AI Profile Generator Flask API")
    print("=" * 50)
    print("📍 Starting server...")
    print("🌐 API will be available at: http://localhost:5000")
    print("📋 Health check: http://localhost:5000/api/health")
    print("📊 Status check: http://localhost:5000/api/status")
    print("📖 API docs: http://localhost:5000/api/profile/examples")
    print("=" * 50)
    
    # Check if we're in development or production
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    try:
        app.run(
            host=host,
            port=port,
            debug=debug_mode,
            use_reloader=debug_mode
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 