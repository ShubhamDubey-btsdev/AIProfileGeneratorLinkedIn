#!/usr/bin/env python3
"""
Test script for name-based LinkedIn search functionality
"""

from linkedin_scraper import LinkedInScraper

def test_name_search():
    """Test the name-based LinkedIn search functionality"""
    
    print("=== TESTING NAME-BASED LINKEDIN SEARCH ===\n")
    
    scraper = LinkedInScraper()
    
    # Test cases
    test_cases = [
        {
            "name": "Satya Nadella",
            "company": "Microsoft",
            "description": "Microsoft CEO - should find profile easily"
        },
        {
            "name": "Tim Cook", 
            "company": "Apple",
            "description": "Apple CEO - well-known public figure"
        },
        {
            "name": "Reid Hoffman",
            "company": "LinkedIn", 
            "description": "LinkedIn Co-founder - should find on LinkedIn"
        },
        {
            "name": "Sundar Pichai",
            "company": "Google",
            "description": "Google CEO - major tech leader"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🧪 Test {i}: {test_case['description']}")
        print(f"   Name: {test_case['name']}")
        print(f"   Company: {test_case['company']}")
        
        try:
            # Search for LinkedIn URL
            linkedin_url = scraper.search_linkedin_profile(
                test_case['name'], 
                test_case['company']
            )
            
            if linkedin_url:
                print(f"   ✅ SUCCESS: Found LinkedIn URL")
                print(f"   🔗 URL: {linkedin_url}")
                
                # Optional: Try to scrape basic info (comment out if testing rate limits)
                # print("   📄 Testing profile extraction...")
                # profile_data = scraper.scrape_profile(linkedin_url)
                # if profile_data:
                #     print(f"   👤 Name extracted: {profile_data.get('name', 'N/A')}")
                #     print(f"   🏢 Company extracted: {profile_data.get('company', 'N/A')}")
                # else:
                #     print("   ⚠️  Could not extract profile data")
                    
            else:
                print(f"   ❌ FAILED: No LinkedIn URL found")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        
        print("-" * 60)
    
    print("\n=== NAME SEARCH TEST COMPLETE ===")
    print("\nNotes:")
    print("- Search success depends on Google's current results")
    print("- Rate limiting may affect consecutive searches")
    print("- Some profiles may be private or have changed URLs")
    print("- Company context significantly improves search accuracy")

if __name__ == "__main__":
    test_name_search() 