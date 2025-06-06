#!/usr/bin/env python3
"""
Test script for AI Profile Generator Flask API
"""

import requests
import json
import sys

API_BASE = "http://localhost:5000"

def test_endpoint(method, endpoint, data=None, description=""):
    """Test a single API endpoint"""
    url = f"{API_BASE}{endpoint}"
    
    print(f"\n🧪 Testing: {description}")
    print(f"📍 {method} {endpoint}")
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, timeout=30)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('message', 'OK')}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the API server running?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run API tests"""
    
    print("🚀 AI Profile Generator API Test Suite")
    print("=" * 50)
    
    tests = [
        # Basic endpoints
        ('GET', '/', None, 'Root endpoint'),
        ('GET', '/api/health', None, 'Health check'),
        ('GET', '/api/status', None, 'Status check'),
        
        # Profile info endpoints
        ('GET', '/api/profile/info', None, 'Profile info'),
        ('GET', '/api/profile/examples', None, 'API examples'),
        ('GET', '/api/search/methods', None, 'Search methods'),
        
        # URL validation
        ('POST', '/api/search/validate-url', {
            'url': 'https://www.linkedin.com/in/satyanadella/'
        }, 'URL validation'),
        
        # LinkedIn URL search
        ('POST', '/api/search/linkedin-url-only', {
            'person_name': 'Satya Nadella',
            'company_name': 'Microsoft'
        }, 'LinkedIn URL search'),
        
        # Full profile generation (name-based)
        ('POST', '/api/search/by-name', {
            'person_name': 'David Ackley',
            'company_name': 'BTS',
            'meeting_context': 'Partnership meeting'
        }, 'Profile generation by name'),
        
        # Full profile generation (URL-based)
        ('POST', '/api/search/by-url', {
            'linkedin_url': 'https://www.linkedin.com/in/satyanadella/',
            'meeting_context': 'Partnership discussion'
        }, 'Profile generation by URL'),
    ]
    
    passed = 0
    total = len(tests)
    
    for method, endpoint, data, description in tests:
        success = test_endpoint(method, endpoint, data, description)
        if success:
            passed += 1
    
    print(f"\n📊 Test Results")
    print("=" * 30)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 