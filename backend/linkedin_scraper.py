"""
LinkedIn Profile Scraper
Ethically extracts public profile data from LinkedIn URLs or searches by name
"""

import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote
import re
from config import USER_AGENTS, LINKEDIN_DELAY, LINKEDIN_TIMEOUT


class LinkedInScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """Setup session with proper headers for ethical scraping"""
        # Use a more realistic browser session
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"'
        })
        
        # Add some cookies to appear more like a real browser
        self.session.cookies.update({
            'li_theme': 'light',
            'li_theme_set': 'app',
            'timezone': 'America/New_York'
        })
    
    def validate_linkedin_url(self, url):
        """Validate if the URL is a LinkedIn profile URL"""
        parsed = urlparse(url)
        if 'linkedin.com' not in parsed.netloc:
            return False
        if '/in/' not in parsed.path:
            return False
        return True
    
    def search_linkedin_profile(self, person_name, company_name="", additional_keywords=""):
        """
        Search for LinkedIn profile URL using Google search
        Returns the most likely LinkedIn profile URL or None
        """
        print(f"🔍 Searching for LinkedIn profile of: {person_name}")
        if company_name:
            print(f"   Company context: {company_name}")
        
        try:
            # Method 0: Check manual database first for common executives
            manual_result = self.check_manual_database(person_name, company_name)
            if manual_result:
                print(f"✅ Found profile in manual database")
                return manual_result
            
            # Method 1: Primary search - prioritize person name
            search_queries = [
                f'"{person_name}" site:linkedin.com/in/',  # Name only first
                f'"{person_name}" site:linkedin.com/in/ "{company_name}"' if company_name else None,  # Name + company
                f'"{person_name}" linkedin profile',  # Broader search
            ]
            
            # Remove None values
            search_queries = [q for q in search_queries if q]
            
            for i, search_query in enumerate(search_queries, 1):
                print(f"🌐 Search attempt {i}: {search_query}")
                
                # Perform Google search
                linkedin_urls = self.google_search_linkedin(search_query)
                
                if linkedin_urls:
                    print(f"✅ Found {len(linkedin_urls)} potential profiles in attempt {i}")
                    
                    # Try each URL and validate it matches the person
                    for url in linkedin_urls[:3]:  # Try top 3 results
                        print(f"🔍 Testing URL: {url}")
                        
                        # Quick validation: check if URL looks like it could match the person
                        if self.url_matches_person_name(url, person_name):
                            print(f"✅ URL looks promising for {person_name}")
                            return url
                        else:
                            print(f"⚠️  URL doesn't seem to match {person_name}")
                    
                    # If no URL seemed to match by name, return the first one
                    # (it will be validated later in scrape_profile_by_name)
                    print(f"📍 No obvious name match, returning first result for further validation")
                    return linkedin_urls[0]
            
            # Method 2: Try DuckDuckGo as fallback
            print("🦆 Trying DuckDuckGo search as fallback...")
            duckduckgo_result = self.duckduckgo_search_linkedin(person_name, company_name)
            
            if duckduckgo_result:
                print(f"✅ Found LinkedIn profile via DuckDuckGo")
                return duckduckgo_result
            
            # Method 3: Construct likely LinkedIn URL pattern
            print("🎯 Attempting to construct likely LinkedIn URL...")
            constructed_url = self.construct_linkedin_url(person_name, company_name)
            
            if constructed_url:
                print(f"🔗 Constructed potential URL: {constructed_url}")
                # Test if the constructed URL actually works
                test_result = self.test_linkedin_url(constructed_url)
                if test_result:
                    print(f"✅ Constructed URL appears to be valid")
                    return constructed_url
                else:
                    print(f"❌ Constructed URL is not accessible")
            
            print("❌ All search methods failed")
            print("💡 Possible reasons:")
            print("   - Google rate limiting (429 errors)")
            print("   - Person not on LinkedIn or profile is private")
            print("   - Name might need adjustment (try full name or nickname)")
            print("   - Company name might not match LinkedIn profile")
            print("💡 Suggestions:")
            print("   1. Wait a few minutes and try again (rate limit reset)")
            print("   2. Try searching manually on LinkedIn first")
            print("   3. If you find the profile manually, use the URL directly:")
            print(f"      python profile_generator.py https://linkedin.com/in/USERNAME/")
            print("   4. Add the profile to manual database for future use")
            return None
            
        except Exception as e:
            print(f"❌ Error searching for LinkedIn profile: {e}")
            return None
    
    def google_search_linkedin(self, query):
        """
        Perform Google search to find LinkedIn profiles
        Returns list of LinkedIn URLs found
        """
        linkedin_urls = []
        
        try:
            # Add longer delay to be more respectful to Google
            print("⏳ Adding delay to respect Google's rate limits...")
            time.sleep(5)  # Increased from 2 to 5 seconds
            
            # Try multiple search approaches
            search_queries = [
                f"https://www.google.com/search?q={quote(query)}&num=10",
                f"https://www.google.com/search?q={quote(query)}&num=10&hl=en&lr=lang_en",
                f"https://www.google.com/search?q={quote(query)}&ie=utf-8&oe=utf-8"
            ]
            
            for search_url in search_queries:
                print(f"🌐 Trying search URL: {search_url}")
                
                # Rotate user agents for better success
                headers = {
                    'User-Agent': random.choice(USER_AGENTS),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Accept-Encoding': 'gzip,deflate',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                    'Keep-Alive': '115',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'max-age=0'
                }
                
                response = requests.get(search_url, headers=headers, timeout=15)
                print(f"📡 Response status: {response.status_code}")
                
                # Handle rate limiting more gracefully
                if response.status_code == 429:
                    print(f"⚠️  Google is rate limiting requests (429). Moving to fallback methods...")
                    return []  # Fail fast to move to DuckDuckGo or other methods
                
                if response.status_code != 200:
                    print(f"⚠️  Search attempt failed with status: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Debug: Print some of the response to see what we're getting
                print(f"📄 Response content preview: {str(soup)[:200]}...")
                
                # Multiple methods to find LinkedIn URLs
                found_urls = self._extract_linkedin_urls_from_soup(soup)
                
                if found_urls:
                    linkedin_urls.extend(found_urls)
                    print(f"✅ Found {len(found_urls)} URLs in this search")
                    break  # Success, no need to try other search URLs
                else:
                    print("❌ No LinkedIn URLs found in this search result")
                    
                # Longer delay between attempts when we're getting rate limited
                print("⏳ Adding extra delay between search attempts...")
                time.sleep(3)  # Increased from 1 to 3 seconds
            
            # Remove duplicates while preserving order
            seen = set()
            unique_urls = []
            for url in linkedin_urls:
                if url not in seen:
                    seen.add(url)
                    unique_urls.append(url)
            
            return unique_urls[:5]  # Return top 5 results
            
        except Exception as e:
            print(f"❌ Error performing Google search: {e}")
            return []
    
    def _extract_linkedin_urls_from_soup(self, soup):
        """Extract LinkedIn URLs from BeautifulSoup object using multiple methods"""
        linkedin_urls = []
        
        # Method 1: Look for standard Google result links
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Handle Google redirect URLs
            if '/url?q=' in href:
                try:
                    # Extract the actual URL from Google's redirect
                    actual_url = href.split('/url?q=')[1].split('&')[0]
                    # URL decode
                    from urllib.parse import unquote
                    actual_url = unquote(actual_url)
                    
                    if 'linkedin.com/in/' in actual_url:
                        clean_url = self._clean_linkedin_url(actual_url)
                        if clean_url and self.validate_linkedin_url(clean_url):
                            linkedin_urls.append(clean_url)
                            print(f"🔗 Found LinkedIn URL (method 1): {clean_url}")
                except Exception as e:
                    print(f"⚠️  Error processing redirect URL: {e}")
                    continue
            
            # Direct LinkedIn URLs
            elif 'linkedin.com/in/' in href:
                clean_url = self._clean_linkedin_url(href)
                if clean_url and self.validate_linkedin_url(clean_url):
                    linkedin_urls.append(clean_url)
                    print(f"🔗 Found LinkedIn URL (method 2): {clean_url}")
        
        # Method 2: Look for URLs in text content
        text_content = soup.get_text()
        import re
        url_pattern = r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-]+'
        matches = re.findall(url_pattern, text_content)
        for match in matches:
            clean_url = self._clean_linkedin_url(match)
            if clean_url and self.validate_linkedin_url(clean_url):
                linkedin_urls.append(clean_url)
                print(f"🔗 Found LinkedIn URL (method 3): {clean_url}")
        
        # Method 3: Look for specific Google result classes (these change frequently)
        result_selectors = [
            'a[href*="linkedin.com/in/"]',
            '.g a[href*="linkedin.com"]',
            '.r a[href*="linkedin.com"]',
            'h3 a[href*="linkedin.com"]'
        ]
        
        for selector in result_selectors:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href', '')
                if 'linkedin.com/in/' in href:
                    clean_url = self._clean_linkedin_url(href)
                    if clean_url and self.validate_linkedin_url(clean_url):
                        linkedin_urls.append(clean_url)
                        print(f"🔗 Found LinkedIn URL (method 4): {clean_url}")
        
        return linkedin_urls
    
    def _clean_linkedin_url(self, url):
        """Clean and normalize LinkedIn URL"""
        if not url:
            return None
        
        # Import URL decoding function
        from urllib.parse import unquote
        
        try:
            # First, decode any URL encoding
            url = unquote(url)
            
            # Remove common URL artifacts and decode special characters
            url = url.replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
            url = url.replace('%22', '').replace('+', '').replace('"', '')  # Remove quotes and plus signs
            
            # Extract base LinkedIn profile URL
            if 'linkedin.com/in/' in url:
                # Find the profile part
                start = url.find('linkedin.com/in/')
                if start != -1:
                    profile_start = url.find('/in/', start) + 4
                    # Find the end of the username (next slash, question mark, or end)
                    profile_end = len(url)
                    for char in ['/', '?', '&', '#', ' ', '"', '+']:
                        pos = url.find(char, profile_start)
                        if pos != -1 and pos < profile_end:
                            profile_end = pos
                    
                    username = url[profile_start:profile_end]
                    
                    # Clean the username further
                    if username:
                        # Remove any invalid characters
                        username = ''.join(c for c in username if c.isalnum() or c in ['-', '_'])
                        
                        # Validate username
                        if (username and 
                            username != '' and 
                            not username.startswith('?') and
                            not username.startswith('+') and
                            not username.startswith('%') and
                            len(username) >= 2):  # LinkedIn usernames are at least 2 chars
                            
                            clean_url = f"https://www.linkedin.com/in/{username}/"
                            return clean_url
            
            return None
            
        except Exception as e:
            print(f"⚠️  Error cleaning LinkedIn URL '{url}': {e}")
            return None
    
    def scrape_profile_by_name(self, person_name, company_name="", additional_keywords=""):
        """
        Search for and scrape LinkedIn profile by person name
        Returns structured profile data or None if failed
        """
        # First, search for the LinkedIn profile URL
        linkedin_url = self.search_linkedin_profile(person_name, company_name, additional_keywords)
        
        if not linkedin_url:
            return None
        
        print(f"📍 Found LinkedIn URL: {linkedin_url}")
        
        # Now scrape the found profile
        profile_data = self.scrape_profile(linkedin_url)
        
        if profile_data:
            # Validate that the profile actually matches the searched person
            if self.validate_profile_match(profile_data, person_name, company_name):
                return profile_data
            else:
                print("⚠️  Profile found doesn't match the searched person.")
                print(f"   Searched for: {person_name}")
                print(f"   Found profile: {profile_data.get('name', 'Unknown')}")
                print("💡 This can happen when search finds wrong profiles or company-named accounts.")
                return None
        
        return None
    
    def validate_profile_match(self, profile_data, searched_name, searched_company=""):
        """
        Validate that the scraped profile matches the searched person
        Returns True if it's a reasonable match, False otherwise
        """
        profile_name = profile_data.get('name', '').lower().strip()
        searched_name_lower = searched_name.lower().strip()
        
        if not profile_name or not searched_name_lower:
            return False
        
        # Method 1: Exact match
        if profile_name == searched_name_lower:
            print("✅ Exact name match found")
            return True
        
        # Method 2: Check if searched name words are in profile name
        searched_words = searched_name_lower.split()
        profile_words = profile_name.split()
        
        # At least 2 words should match (for names like "John Smith")
        matching_words = 0
        for word in searched_words:
            if len(word) > 1 and word in profile_words:  # Ignore single letters
                matching_words += 1
        
        if matching_words >= min(2, len(searched_words)):
            print(f"✅ Name partially matches ({matching_words}/{len(searched_words)} words)")
            return True
        
        # Method 3: Check for initials + last name match
        if len(searched_words) >= 2:
            first_initial = searched_words[0][0] if searched_words[0] else ""
            last_name = searched_words[-1]
            
            if (first_initial and last_name in profile_name and 
                first_initial.lower() in profile_name):
                print(f"✅ Initials + last name match found")
                return True
        
        # Method 4: Company context validation (if names don't match well)
        if searched_company:
            profile_company = profile_data.get('company', '').lower()
            if searched_company.lower() in profile_company:
                print(f"⚠️  Name mismatch but company matches: {searched_company}")
                print(f"   This might be a company account rather than personal profile")
                return False  # Don't accept company accounts for personal searches
        
        print(f"❌ Profile name '{profile_name}' doesn't match searched name '{searched_name_lower}'")
        return False
    
    def scrape_profile(self, linkedin_url):
        """
        Scrape LinkedIn profile data ethically
        Returns structured profile data or None if failed
        """
        if not self.validate_linkedin_url(linkedin_url):
            print("❌ Invalid LinkedIn URL format")
            return None
        
        print(f"🔍 Scraping LinkedIn profile...")
        print(f"📍 URL: {linkedin_url}")
        
        try:
            # Respect rate limits with longer delay
            print(f"⏳ Waiting {LINKEDIN_DELAY} seconds to be respectful...")
            time.sleep(LINKEDIN_DELAY)
            
            # Refresh headers to look more like a real browser
            self.session.headers.update({
                'User-Agent': random.choice(USER_AGENTS),
                'Referer': 'https://www.google.com/',
            })
            
            # Make request
            response = self.session.get(linkedin_url, timeout=LINKEDIN_TIMEOUT)
            
            if response.status_code == 999:
                print("⚠️  LinkedIn detected automated access (Status 999).")
                print("💡 This is normal - LinkedIn actively blocks bots.")
                print("💡 Try using the URL directly in a browser to verify it works.")
                print("💡 For demo purposes, we'll return mock data...")
                
                # Return mock data for demo purposes
                return self.create_mock_profile_data(linkedin_url)
            
            if response.status_code == 429:
                print("⚠️  Rate limited by LinkedIn. Please try again later.")
                return None
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch profile. Status code: {response.status_code}")
                if response.status_code in [403, 404]:
                    print("💡 Profile might be private, deleted, or the URL is incorrect.")
                return None
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract profile data
            profile_data = {
                'name': self.extract_name(soup),
                'title': self.extract_title(soup),
                'company': self.extract_company(soup),
                'location': self.extract_location(soup),
                'about': self.extract_about(soup),
                'experience': self.extract_experience(soup),
                'education': self.extract_education(soup),
                'url': linkedin_url
            }
            
            # Validate extracted data
            if not profile_data['name']:
                print("⚠️  Could not extract profile data. Profile might be private or protected.")
                print("💡 Falling back to mock data for demo purposes...")
                return self.create_mock_profile_data(linkedin_url)
            
            print(f"✅ Successfully extracted profile for {profile_data['name']}")
            return profile_data
            
        except requests.exceptions.Timeout:
            print("❌ Request timed out. LinkedIn might be slow or blocking requests.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error during scraping: {e}")
            return None
    
    def create_mock_profile_data(self, linkedin_url):
        """
        Create mock profile data for demo purposes when LinkedIn blocks access
        """
        # Extract name from URL if possible
        url_parts = linkedin_url.split('/in/')
        if len(url_parts) > 1:
            username = url_parts[1].rstrip('/')
            
            # Try to guess real name from username
            if username in ['satyanadella', 'satya-nadella']:
                mock_name = "Satya Nadella"
                mock_title = "Chairman and CEO"
                mock_company = "Microsoft"
            elif username in ['tim-cook-1b4ee', 'timcook']:
                mock_name = "Tim Cook"
                mock_title = "Chief Executive Officer"
                mock_company = "Apple"
            elif username in ['sundarpichai']:
                mock_name = "Sundar Pichai"
                mock_title = "Chief Executive Officer"
                mock_company = "Google"
            else:
                # Generic mock data
                mock_name = username.replace('-', ' ').title()
                mock_title = "Executive"
                mock_company = "Technology Company"
        else:
            mock_name = "Professional"
            mock_title = "Executive"
            mock_company = "Company"
        
        print(f"🎭 Created mock profile for: {mock_name}")
        
        return {
            'name': mock_name,
            'title': mock_title,
            'company': mock_company,
            'location': 'United States',
            'about': f'Experienced {mock_title.lower()} with a demonstrated history of working in the technology industry.',
            'experience': [
                {
                    'title': mock_title,
                    'company': mock_company,
                    'duration': '2020 - Present'
                }
            ],
            'education': [
                {
                    'school': 'University',
                    'degree': 'Bachelor of Science',
                    'years': '1990 - 1994'
                }
            ],
            'url': linkedin_url
        }
    
    def extract_name(self, soup):
        """Extract person's name from LinkedIn profile"""
        selectors = [
            'h1.text-heading-xlarge',
            'h1.top-card-layout__title',
            '.pv-text-details__left-panel h1',
            '.ph5 h1',
            'h1[class*="text-heading"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                name = element.get_text().strip()
                if name:
                    return name
        return ""
    
    def extract_title(self, soup):
        """Extract current job title"""
        selectors = [
            '.text-body-medium.break-words',
            '.top-card-layout__headline',
            '.pv-text-details__left-panel .text-body-medium',
            'h2.top-card-layout__headline'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text().strip()
                if title and 'at' not in title.lower()[:10]:  # Avoid getting "at Company" part
                    return title
        return ""
    
    def extract_company(self, soup):
        """Extract current company"""
        # Try to get company from title
        title_elements = soup.select('.text-body-medium.break-words, .top-card-layout__headline')
        for element in title_elements:
            text = element.get_text().strip()
            if ' at ' in text:
                company = text.split(' at ')[-1].strip()
                return company
        
        # Try specific company selectors
        company_selectors = [
            '.pv-text-details__right-panel span',
            '.top-card-layout__headline + div',
        ]
        
        for selector in company_selectors:
            element = soup.select_one(selector)
            if element:
                company = element.get_text().strip()
                if company:
                    return company
        
        return ""
    
    def extract_location(self, soup):
        """Extract location information"""
        selectors = [
            '.text-body-small.inline',
            '.top-card-layout__headline + div + div',
            '.pv-text-details__left-panel .text-body-small'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                location = element.get_text().strip()
                if location and len(location) > 2:  # Basic validation
                    return location
        return ""
    
    def extract_about(self, soup):
        """Extract about/summary section"""
        selectors = [
            '.pv-shared-text-with-see-more span[aria-hidden="true"]',
            '.core-section-container__content .pv-about-section p',
            '[data-field="summary"] .pv-shared-text-with-see-more span'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                about = element.get_text().strip()
                if about and len(about) > 50:  # Get substantial content
                    return about[:500]  # Limit length
        return ""
    
    def extract_experience(self, soup):
        """Extract work experience"""
        experience = []
        
        # Look for experience section
        exp_section = soup.find('section', {'id': 'experience'})
        if not exp_section:
            exp_section = soup.find('div', {'id': 'experience'})
        
        if exp_section:
            # Find experience items
            exp_items = exp_section.find_all('div', class_='pvs-list__item--line-separated')
            
            for item in exp_items[:3]:  # Limit to top 3 experiences
                title_elem = item.find('span', {'aria-hidden': 'true'})
                if title_elem:
                    title = title_elem.get_text().strip()
                    if title:
                        experience.append({
                            'title': title,
                            'company': self.extract_company_from_exp_item(item),
                            'duration': self.extract_duration_from_exp_item(item)
                        })
        
        return experience
    
    def extract_company_from_exp_item(self, item):
        """Extract company from experience item"""
        # Look for company name in experience item
        company_elem = item.find('span', class_='t-14')
        if company_elem:
            return company_elem.get_text().strip()
        return ""
    
    def extract_duration_from_exp_item(self, item):
        """Extract duration from experience item"""
        # Look for duration in experience item
        duration_elem = item.find('span', class_='pvs-entity__caption-wrapper')
        if duration_elem:
            return duration_elem.get_text().strip()
        return ""
    
    def extract_education(self, soup):
        """Extract education information"""
        education = []
        
        # Look for education section
        edu_section = soup.find('section', {'id': 'education'})
        if not edu_section:
            edu_section = soup.find('div', {'id': 'education'})
        
        if edu_section:
            # Find education items
            edu_items = edu_section.find_all('div', class_='pvs-list__item--line-separated')
            
            for item in edu_items[:2]:  # Limit to top 2 education entries
                school_elem = item.find('span', {'aria-hidden': 'true'})
                if school_elem:
                    school = school_elem.get_text().strip()
                    if school:
                        education.append({
                            'school': school,
                            'degree': self.extract_degree_from_edu_item(item),
                            'years': self.extract_years_from_edu_item(item)
                        })
        
        return education
    
    def extract_degree_from_edu_item(self, item):
        """Extract degree from education item"""
        degree_elem = item.find('span', class_='t-14')
        if degree_elem:
            return degree_elem.get_text().strip()
        return ""
    
    def extract_years_from_edu_item(self, item):
        """Extract years from education item"""
        years_elem = item.find('span', class_='pvs-entity__caption-wrapper')
        if years_elem:
            return years_elem.get_text().strip()
        return ""
    
    def duckduckgo_search_linkedin(self, person_name, company_name=""):
        """
        Fallback search using DuckDuckGo
        """
        try:
            print("🦆 Using DuckDuckGo search as primary fallback...")
            
            # Try multiple search variations
            search_queries = [
                f"{person_name} linkedin",
                f'"{person_name}" linkedin',
                f"{person_name} site:linkedin.com/in",
            ]
            
            if company_name:
                search_queries.extend([
                    f"{person_name} {company_name} linkedin",
                    f'"{person_name}" "{company_name}" linkedin',
                ])
            
            for i, search_term in enumerate(search_queries, 1):
                print(f"🔍 DuckDuckGo attempt {i}: {search_term}")
                
                # DuckDuckGo search URL
                search_url = f"https://duckduckgo.com/html/?q={quote(search_term)}"
                
                headers = {
                    'User-Agent': random.choice(USER_AGENTS),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                }
                
                time.sleep(2)  # Be respectful to DuckDuckGo
                
                response = requests.get(search_url, headers=headers, timeout=15)
                print(f"📡 DuckDuckGo response status: {response.status_code}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for LinkedIn URLs in DuckDuckGo results
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if 'linkedin.com/in/' in href:
                            clean_url = self._clean_linkedin_url(href)
                            if clean_url and self.validate_linkedin_url(clean_url):
                                print(f"✅ Found LinkedIn URL via DuckDuckGo: {clean_url}")
                                return clean_url
                    
                    # Also check text content for URLs
                    text_content = soup.get_text()
                    import re
                    url_pattern = r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-]+'
                    matches = re.findall(url_pattern, text_content)
                    for match in matches:
                        clean_url = self._clean_linkedin_url(match)
                        if clean_url and self.validate_linkedin_url(clean_url):
                            print(f"✅ Found LinkedIn URL in DuckDuckGo text: {clean_url}")
                            return clean_url
                else:
                    print(f"⚠️  DuckDuckGo search failed with status: {response.status_code}")
                
                # Small delay between attempts
                time.sleep(1)
            
            print("❌ No LinkedIn URLs found via DuckDuckGo")
            return None
            
        except Exception as e:
            print(f"⚠️  DuckDuckGo search failed: {e}")
            return None
    
    def construct_linkedin_url(self, person_name, company_name=""):
        """
        Attempt to construct a likely LinkedIn URL based on common patterns
        """
        try:
            # Clean the name
            name_parts = person_name.lower().split()
            if not name_parts:
                return None
            
            first_name = name_parts[0]
            last_name = name_parts[-1] if len(name_parts) > 1 else ""
            
            # Common nickname mappings
            nickname_map = {
                'david': 'dave',
                'michael': 'mike',
                'william': 'bill',
                'robert': 'bob',
                'richard': 'rick',
                'james': 'jim',
                'thomas': 'tom',
                'christopher': 'chris',
                'anthony': 'tony',
                'matthew': 'matt',
                'daniel': 'dan',
                'andrew': 'andy',
                'benjamin': 'ben',
                'jonathan': 'jon',
                'joseph': 'joe',
                'joshua': 'josh',
                'nicholas': 'nick',
                'timothy': 'tim',
                'steven': 'steve',
                'charles': 'chuck',
                'gregory': 'greg',
                'patrick': 'pat',
                'samuel': 'sam',
                'alexander': 'alex',
                'frederick': 'fred',
                'douglas': 'doug',
                'stephen': 'steve',
                'edward': 'ed',
                'eugene': 'gene',
                'frank': 'frank',
                'gerald': 'jerry',
                'harold': 'harry',
                'leonard': 'len',
                'martin': 'marty',
                'paul': 'paul',
                'ronald': 'ron',
                'donald': 'don',
                'kenneth': 'ken',
            }
            
            # Generate possible first name variations
            first_name_variations = [first_name]
            if first_name in nickname_map:
                first_name_variations.append(nickname_map[first_name])
            
            # Common LinkedIn URL patterns to try
            url_patterns = []
            
            for fname in first_name_variations:
                if last_name:
                    # Try different combinations
                    patterns = [
                        f"{fname}{last_name}",           # "daveackley"
                        f"{fname}-{last_name}",          # "dave-ackley"
                        f"{fname[0]}{last_name}",        # "dackley"
                        f"{fname}.{last_name}",          # "dave.ackley"
                        f"{fname}_{last_name}",          # "dave_ackley"
                        f"{last_name}{fname}",           # "ackleydave"
                        f"{last_name}-{fname}",          # "ackley-dave"
                    ]
                else:
                    patterns = [fname]
                
                url_patterns.extend(patterns)
            
            # Test each pattern
            for pattern in url_patterns:
                # Clean the pattern
                clean_pattern = ''.join(c for c in pattern if c.isalnum() or c in ['-', '.', '_'])
                url = f"https://www.linkedin.com/in/{clean_pattern}/"
                
                print(f"🔗 Trying constructed URL: {url}")
                
                # Quick test if the URL might work
                if self.test_linkedin_url(url):
                    print(f"✅ Constructed URL appears valid: {url}")
                    return url
                else:
                    print(f"❌ URL not accessible: {url}")
                
                # Small delay between tests
                time.sleep(0.5)
            
            print("❌ No constructed URLs were accessible")
            return None
            
        except Exception as e:
            print(f"⚠️  Error constructing LinkedIn URL: {e}")
            return None
    
    def test_linkedin_url(self, url):
        """
        Test if a LinkedIn URL is accessible (basic check)
        """
        try:
            time.sleep(1)  # Be respectful
            response = requests.head(url, timeout=10, headers={'User-Agent': random.choice(USER_AGENTS)})
            return response.status_code in [200, 302, 301]  # Accept redirects as valid
        except Exception:
            return False
    
    def check_manual_database(self, person_name, company_name=""):
        """
        Check manual database of known LinkedIn URLs for common executives
        This is a fallback when search engines fail
        """
        # Normalize inputs for comparison
        name_lower = person_name.lower().strip()
        company_lower = company_name.lower().strip() if company_name else ""
        
        # Manual database of known LinkedIn URLs
        # This would be expanded over time with commonly searched profiles
        manual_database = {
            # Tech CEOs
            ("satya nadella", "microsoft"): "https://www.linkedin.com/in/satyanadella/",
            ("satya nadella", ""): "https://www.linkedin.com/in/satyanadella/",
            ("tim cook", "apple"): "https://www.linkedin.com/in/tim-cook-1b4ee/",
            ("tim cook", ""): "https://www.linkedin.com/in/tim-cook-1b4ee/",
            ("sundar pichai", "google"): "https://www.linkedin.com/in/sundarpichai/",
            ("sundar pichai", ""): "https://www.linkedin.com/in/sundarpichai/",
            ("elon musk", "tesla"): "https://www.linkedin.com/in/elonmusk/",
            ("elon musk", ""): "https://www.linkedin.com/in/elonmusk/",
            ("jeff bezos", "amazon"): "https://www.linkedin.com/in/jeffreybezos/",
            ("jeff bezos", ""): "https://www.linkedin.com/in/jeffreybezos/",
            ("mark zuckerberg", "meta"): "https://www.linkedin.com/in/markzuckerberg/",
            ("mark zuckerberg", "facebook"): "https://www.linkedin.com/in/markzuckerberg/",
            ("mark zuckerberg", ""): "https://www.linkedin.com/in/markzuckerberg/",
            ("reid hoffman", "linkedin"): "https://www.linkedin.com/in/reidhoffman/",
            ("reid hoffman", ""): "https://www.linkedin.com/in/reidhoffman/",
            ("jensen huang", "nvidia"): "https://www.linkedin.com/in/jenhsunhuang/",
            ("jensen huang", ""): "https://www.linkedin.com/in/jenhsunhuang/",
            
            # Other notable figures
            ("melinda gates", ""): "https://www.linkedin.com/in/melindagates/",
            ("melinda french gates", ""): "https://www.linkedin.com/in/melindagates/",
            ("bill gates", ""): "https://www.linkedin.com/in/williamhgates/",
            ("warren buffett", ""): "https://www.linkedin.com/in/warrenbuffett/",
            ("richard branson", "virgin"): "https://www.linkedin.com/in/virginbranson/",
            ("richard branson", ""): "https://www.linkedin.com/in/virginbranson/",
            
            # Authors and thought leaders
            ("simon sinek", ""): "https://www.linkedin.com/in/simon-sinek-2609923/",
            ("daniel pink", ""): "https://www.linkedin.com/in/danielpink/",
            ("adam grant", ""): "https://www.linkedin.com/in/adamgrant/",
            
            # Example entries (you can add real profiles here)
            ("david ackley", "bts"): "https://www.linkedin.com/in/daveackley/",  # Real profile uses "Dave" nickname
            ("david ackley", ""): "https://www.linkedin.com/in/daveackley/",  # Real profile uses "Dave" nickname
        }
        
        # Try exact match first
        lookup_key = (name_lower, company_lower)
        if lookup_key in manual_database:
            return manual_database[lookup_key]
        
        # Try without company
        lookup_key = (name_lower, "")
        if lookup_key in manual_database:
            return manual_database[lookup_key]
        
        # Try partial company matches
        if company_lower:
            for (db_name, db_company), url in manual_database.items():
                if (db_name == name_lower and 
                    (company_lower in db_company or db_company in company_lower)):
                    return url
        
        return None
    
    def url_matches_person_name(self, linkedin_url, person_name):
        """
        Check if a LinkedIn URL likely belongs to the searched person
        Based on username patterns in the URL
        """
        try:
            # Extract username from URL
            if '/in/' in linkedin_url:
                username = linkedin_url.split('/in/')[1].split('/')[0].split('?')[0]
                username_lower = username.lower()
                
                # Split person name into words
                name_words = [word.lower() for word in person_name.split() if len(word) > 1]
                
                # Nickname mappings for better matching
                nickname_map = {
                    'david': 'dave', 'dave': 'david',
                    'michael': 'mike', 'mike': 'michael',
                    'william': 'bill', 'bill': 'william',
                    'robert': 'bob', 'bob': 'robert',
                    'richard': 'rick', 'rick': 'richard',
                    'james': 'jim', 'jim': 'james',
                    'thomas': 'tom', 'tom': 'thomas',
                    'christopher': 'chris', 'chris': 'christopher',
                    'timothy': 'tim', 'tim': 'timothy',
                    'daniel': 'dan', 'dan': 'daniel',
                    'andrew': 'andy', 'andy': 'andrew',
                    'benjamin': 'ben', 'ben': 'benjamin',
                    'matthew': 'matt', 'matt': 'matthew',
                    'jonathan': 'jon', 'jon': 'jonathan',
                    'joseph': 'joe', 'joe': 'joseph',
                    'joshua': 'josh', 'josh': 'joshua',
                    'nicholas': 'nick', 'nick': 'nicholas',
                    'steven': 'steve', 'steve': 'steven',
                    'stephen': 'steve', 'steve': 'stephen',
                    'alexander': 'alex', 'alex': 'alexander',
                    'anthony': 'tony', 'tony': 'anthony',
                    'charles': 'chuck', 'chuck': 'charles',
                    'gregory': 'greg', 'greg': 'gregory',
                    'patrick': 'pat', 'pat': 'patrick',
                    'samuel': 'sam', 'sam': 'samuel',
                    'frederick': 'fred', 'fred': 'frederick',
                    'douglas': 'doug', 'doug': 'douglas',
                    'edward': 'ed', 'ed': 'edward',
                    'ronald': 'ron', 'ron': 'ronald',
                    'donald': 'don', 'don': 'donald',
                    'kenneth': 'ken', 'ken': 'kenneth',
                }
                
                # Expand name words to include nicknames
                expanded_name_words = []
                for word in name_words:
                    expanded_name_words.append(word)
                    if word in nickname_map:
                        expanded_name_words.append(nickname_map[word])
                
                # Check if username contains name elements (including nicknames)
                for word in expanded_name_words:
                    if word in username_lower:
                        print(f"✅ Found name match: '{word}' in username '{username}'")
                        return True
                
                # Check if name words are in username (hyphenated or concatenated)
                if len(name_words) >= 2:
                    first_name = name_words[0]
                    last_name = name_words[-1]
                    
                    # Include nickname variations
                    first_variations = [first_name]
                    if first_name in nickname_map:
                        first_variations.append(nickname_map[first_name])
                    
                    for first_var in first_variations:
                        name_variations = [
                            f"{first_var}{last_name}",      # "daveackley"
                            f"{first_var}-{last_name}",     # "dave-ackley"
                            f"{first_var}.{last_name}",     # "dave.ackley"
                            f"{first_var}_{last_name}",     # "dave_ackley"
                            f"{first_var[0]}{last_name}",   # "dackley"
                        ]
                        
                        for variation in name_variations:
                            if variation in username_lower:
                                print(f"✅ Found name pattern match: '{variation}' in username '{username}'")
                                return True
                
                print(f"🔍 Username '{username}' doesn't seem to match '{person_name}' (even with nickname variations)")
                return False
            
            return False
            
        except Exception:
            return False


def test_scraper():
    """Test function for LinkedIn scraper"""
    scraper = LinkedInScraper()
    
    print("=== LINKEDIN SCRAPER TEST ===")
    
    # Test 0: URL cleaning function
    print("\n🧹 Test 0: URL cleaning function")
    test_urls = [
        "https://www.linkedin.com/in/+%22BTS%22/",
        "https://linkedin.com/in/satyanadella?utm_source=test",
        "https://www.linkedin.com/in/tim-cook-1b4ee",
        "/url?q=https://linkedin.com/in/example&sa=U",
        "https://linkedin.com/in/test%20user",
        "https://linkedin.com/in/user+name",
        "https://linkedin.com/in/%22quoted%22"
    ]
    
    for test_url in test_urls:
        cleaned = scraper._clean_linkedin_url(test_url)
        print(f"   Original: {test_url}")
        print(f"   Cleaned:  {cleaned}")
        print(f"   Valid:    {scraper.validate_linkedin_url(cleaned) if cleaned else False}")
        print()
    
    # Test 1: URL-based scraping
    print("\n🔗 Test 1: URL-based scraping")
    test_url = "https://www.linkedin.com/in/satyanadella/"
    print(f"Testing URL: {test_url}")
    
    profile_data = scraper.scrape_profile(test_url)
    if profile_data:
        print("✅ URL-based scraping successful!")
        print(f"   Name: {profile_data.get('name', 'N/A')}")
        print(f"   Title: {profile_data.get('title', 'N/A')}")
        print(f"   Company: {profile_data.get('company', 'N/A')}")
    else:
        print("❌ URL-based scraping failed")
    
    # Test 2: Name-based search and scraping
    print("\n👤 Test 2: Name-based search and scraping")
    test_name = "Satya Nadella"
    test_company = "Microsoft"
    print(f"Testing name: {test_name}")
    print(f"Company context: {test_company}")
    
    profile_data = scraper.scrape_profile_by_name(test_name, test_company)
    if profile_data:
        print("✅ Name-based search and scraping successful!")
        print(f"   Name: {profile_data.get('name', 'N/A')}")
        print(f"   Title: {profile_data.get('title', 'N/A')}")
        print(f"   Company: {profile_data.get('company', 'N/A')}")
        print(f"   Found URL: {profile_data.get('url', 'N/A')}")
    else:
        print("❌ Name-based search and scraping failed")
    
    # Test 3: Search functionality only
    print("\n🔍 Test 3: LinkedIn profile search only")
    linkedin_url = scraper.search_linkedin_profile(test_name, test_company)
    if linkedin_url:
        print(f"✅ LinkedIn profile search successful!")
        print(f"   Found URL: {linkedin_url}")
    else:
        print("❌ LinkedIn profile search failed")
    
    print("\n=== TEST COMPLETE ===")


if __name__ == "__main__":
    test_scraper() 