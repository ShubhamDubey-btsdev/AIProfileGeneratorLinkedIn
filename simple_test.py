#!/usr/bin/env python3
"""
Simple test script to debug LinkedIn search issues
"""

from linkedin_scraper import LinkedInScraper
import requests
from urllib.parse import quote

def test_google_directly():
    """Test Google search directly to see what's happening"""
    
    query = '"Satya Nadella" site:linkedin.com/in/ "Microsoft"'
    search_url = f"https://www.google.com/search?q={quote(query)}&num=10"
    
    print(f"🔍 Testing Google search directly")
    print(f"🌐 URL: {search_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print(f"📄 Content length: {len(content)} characters")
            
            # Check if we can find LinkedIn in the content
            if 'linkedin.com' in content.lower():
                print("✅ LinkedIn found in response")
                # Extract a small sample around linkedin mentions
                import re
                matches = re.finditer(r'linkedin\.com/in/[^"\s]+', content, re.IGNORECASE)
                for i, match in enumerate(matches):
                    if i < 3:  # Show first 3 matches
                        print(f"🔗 Found: {match.group()}")
            else:
                print("❌ No LinkedIn references found in response")
                
            # Save response for debugging
            with open('google_response.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print("💾 Response saved to google_response.html for inspection")
                
        else:
            print(f"❌ Non-200 status code: {response.status_code}")
            print(f"Response text: {response.text[:500]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_known_linkedin_url():
    """Test with a known LinkedIn URL to verify scraping works"""
    
    print(f"\n🧪 Testing known LinkedIn URL...")
    scraper = LinkedInScraper()
    
    known_url = "https://www.linkedin.com/in/satyanadella/"
    print(f"🔗 Testing URL: {known_url}")
    
    result = scraper.scrape_profile(known_url)
    if result:
        print("✅ LinkedIn scraping works!")
        print(f"👤 Name: {result.get('name', 'N/A')}")
        print(f"🏢 Title: {result.get('title', 'N/A')}")
    else:
        print("❌ LinkedIn scraping failed")

def test_search_functionality():
    """Test the search functionality"""
    
    print(f"\n🔍 Testing search functionality...")
    scraper = LinkedInScraper()
    
    result = scraper.search_linkedin_profile("Satya Nadella", "Microsoft")
    if result:
        print(f"✅ Search found: {result}")
    else:
        print("❌ Search failed")

if __name__ == "__main__":
    print("=== LINKEDIN SEARCH DEBUG TEST ===")
    
    # Test 1: Direct Google search
    test_google_directly()
    
    # Test 2: Known LinkedIn URL
    test_known_linkedin_url()
    
    # Test 3: Search functionality
    test_search_functionality()
    
    print("\n=== TEST COMPLETE ===") 