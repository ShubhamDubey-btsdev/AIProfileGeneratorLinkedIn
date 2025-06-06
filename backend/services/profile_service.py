"""
Profile Service
Business logic layer that wraps the existing LinkedIn scraper, AI processor, and news collector
"""

import sys
import os
import time
from datetime import datetime

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from linkedin_scraper import LinkedInScraper
from ai_processor import AIProcessor
from news_collector import NewsCollector


class ProfileService:
    """Service class that orchestrates profile generation"""
    
    def __init__(self):
        self.linkedin_scraper = LinkedInScraper()
        self.ai_processor = AIProcessor()
        self.news_collector = NewsCollector()
    
    def generate_profile_from_url(self, linkedin_url, meeting_context=""):
        """
        Generate profile briefing from LinkedIn URL
        
        Args:
            linkedin_url: LinkedIn profile URL
            meeting_context: Context for the meeting
            
        Returns:
            dict: Profile data with briefing and metadata
        """
        start_time = time.time()
        search_method = "url_direct"
        
        try:
            # Step 1: Scrape LinkedIn Profile
            linkedin_data = self.linkedin_scraper.scrape_profile(linkedin_url)
            
            if not linkedin_data:
                return {
                    'linkedin_profile': None,
                    'briefing': None,
                    'news_articles': [],
                    'search_method': search_method,
                    'processing_time': time.time() - start_time,
                    'error': 'Failed to extract LinkedIn profile data'
                }
            
            # Complete the profile generation
            return self._complete_profile_generation(
                linkedin_data, meeting_context, search_method, start_time
            )
            
        except Exception as e:
            return {
                'linkedin_profile': None,
                'briefing': None,
                'news_articles': [],
                'search_method': search_method,
                'processing_time': time.time() - start_time,
                'error': f'Error processing LinkedIn URL: {str(e)}'
            }
    
    def generate_profile_from_name(self, person_name, company_name="", meeting_context=""):
        """
        Generate profile briefing by searching for person by name
        
        Args:
            person_name: Full name of the person
            company_name: Company name (optional)
            meeting_context: Context for the meeting
            
        Returns:
            dict: Profile data with briefing and metadata
        """
        start_time = time.time()
        search_method = "name_search"
        
        try:
            # Step 1: Search for LinkedIn Profile
            linkedin_data = self.linkedin_scraper.scrape_profile_by_name(
                person_name, company_name
            )
            
            if not linkedin_data:
                return {
                    'linkedin_profile': None,
                    'briefing': None,
                    'news_articles': [],
                    'search_method': search_method,
                    'processing_time': time.time() - start_time,
                    'error': 'Failed to find or extract LinkedIn profile'
                }
            
            # Determine the actual search method used
            linkedin_url = linkedin_data.get('url', '')
            if 'satyanadella' in linkedin_url or 'tim-cook' in linkedin_url:
                search_method = "manual_database"
            elif linkedin_data.get('name', '').lower() == person_name.lower():
                search_method = "search_success"
            else:
                search_method = "name_search"
            
            # Complete the profile generation
            return self._complete_profile_generation(
                linkedin_data, meeting_context, search_method, start_time
            )
            
        except Exception as e:
            return {
                'linkedin_profile': None,
                'briefing': None,
                'news_articles': [],
                'search_method': search_method,
                'processing_time': time.time() - start_time,
                'error': f'Error processing name search: {str(e)}'
            }
    
    def _complete_profile_generation(self, linkedin_data, meeting_context, search_method, start_time):
        """
        Complete the profile generation process after LinkedIn data is obtained
        
        Args:
            linkedin_data: LinkedIn profile data
            meeting_context: Meeting context
            search_method: Method used to find profile
            start_time: Start time for processing
            
        Returns:
            dict: Complete profile data with briefing
        """
        try:
            # Step 2: Collect News Articles
            news_articles = []
            try:
                news_articles = self.news_collector.search_person_news(
                    linkedin_data.get('name', ''),
                    linkedin_data.get('company', ''),
                    linkedin_data.get('title', '')
                )
            except Exception as e:
                print(f"News collection failed: {e}")
                # Continue without news articles
            
            # Step 3: Generate AI Briefing
            briefing = None
            try:
                briefing = self.ai_processor.generate_briefing(
                    linkedin_data,
                    news_articles,
                    meeting_context
                )
            except Exception as e:
                print(f"AI briefing generation failed: {e}")
                # Create a basic briefing
                briefing = self._create_basic_briefing(linkedin_data)
            
            return {
                'linkedin_profile': linkedin_data,
                'briefing': briefing,
                'news_articles': news_articles or [],
                'search_method': search_method,
                'processing_time': time.time() - start_time,
                'error': None
            }
            
        except Exception as e:
            return {
                'linkedin_profile': linkedin_data,
                'briefing': None,
                'news_articles': [],
                'search_method': search_method,
                'processing_time': time.time() - start_time,
                'error': f'Error completing profile generation: {str(e)}'
            }
    
    def _create_basic_briefing(self, linkedin_data):
        """
        Create a basic briefing when AI processing fails
        
        Args:
            linkedin_data: LinkedIn profile data
            
        Returns:
            dict: Basic briefing structure
        """
        name = linkedin_data.get('name', 'Unknown')
        title = linkedin_data.get('title', 'Professional')
        company = linkedin_data.get('company', 'Organization')
        
        return {
            'executive_summary': f"{name} is a {title} at {company} with professional experience in their field.",
            'key_insights': [
                f"Current role: {title}",
                f"Organization: {company}",
                f"Professional background available on LinkedIn"
            ],
            'conversation_starters': [
                f"What's your experience like at {company}?",
                "What are your thoughts on current industry trends?",
                "How has your role evolved over time?"
            ],
            'recent_activity': "Recent activity information not available.",
            'meeting_preparation': [
                "Review their LinkedIn profile for common connections",
                "Research their company's recent developments",
                "Prepare industry-specific talking points"
            ],
            'strategic_notes': [
                "Professional with relevant industry experience",
                "Consider exploring mutual business interests"
            ],
            'confidence_score': 60
        }
    
    def search_linkedin_profile_only(self, person_name, company_name=""):
        """
        Search for LinkedIn profile without generating full briefing
        
        Args:
            person_name: Full name of the person
            company_name: Company name (optional)
            
        Returns:
            dict: Search result with LinkedIn URL if found
        """
        start_time = time.time()
        
        try:
            linkedin_url = self.linkedin_scraper.search_linkedin_profile(
                person_name, company_name
            )
            
            search_method = "manual_database" if linkedin_url else "search_failed"
            
            return {
                'linkedin_url': linkedin_url,
                'person_name': person_name,
                'company_name': company_name,
                'search_method': search_method,
                'processing_time': time.time() - start_time,
                'found': bool(linkedin_url)
            }
            
        except Exception as e:
            return {
                'linkedin_url': None,
                'person_name': person_name,
                'company_name': company_name,
                'search_method': 'search_error',
                'processing_time': time.time() - start_time,
                'found': False,
                'error': str(e)
            }
    
    def validate_linkedin_url(self, url):
        """
        Validate if a URL is a valid LinkedIn profile URL
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if valid LinkedIn URL
        """
        try:
            return self.linkedin_scraper.validate_linkedin_url(url)
        except Exception:
            return False
    
    def get_service_status(self):
        """
        Get status of all service components
        
        Returns:
            dict: Status of each component
        """
        return {
            'linkedin_scraper': {
                'available': True,
                'description': 'LinkedIn profile extraction and search'
            },
            'ai_processor': {
                'available': self.ai_processor.client_ready,
                'description': 'Azure OpenAI integration for briefing generation'
            },
            'news_collector': {
                'available': self.news_collector.api_key_configured,
                'description': 'News API integration for recent articles'
            }
        } 