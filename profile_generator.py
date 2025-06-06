#!/usr/bin/env python3
"""
AI Profile Generator - Main Script
Command-line tool to generate AI-powered briefings from LinkedIn profiles

Usage: 
  python profile_generator.py <linkedin_url> [--verbose] [--context "meeting context"]
  python profile_generator.py --name "Person Name" [--company "Company"] [--verbose] [--context "meeting context"]
"""

import argparse
import sys
import time
from datetime import datetime
import re

# Import our modules
from linkedin_scraper import LinkedInScraper
from news_collector import NewsCollector
from ai_processor import AIProcessor
from config import CONSOLE_WIDTH


class ProfileGenerator:
    def __init__(self):
        self.linkedin_scraper = LinkedInScraper()
        self.news_collector = NewsCollector()
        self.ai_processor = AIProcessor()
        self.verbose = False
    
    def is_linkedin_url(self, input_string):
        """Check if input is a LinkedIn URL"""
        return ('linkedin.com' in input_string.lower() and 
                ('/in/' in input_string or '/pub/' in input_string))
    
    def generate_profile_from_url(self, linkedin_url, meeting_context="", verbose=False):
        """Generate profile briefing from LinkedIn URL"""
        self.verbose = verbose
        
        print("=" * CONSOLE_WIDTH)
        print("🤖 AI PROFILE GENERATOR")
        print("=" * CONSOLE_WIDTH)
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔗 LinkedIn URL: {linkedin_url}")
        if meeting_context:
            print(f"📋 Meeting Context: {meeting_context}")
        print("=" * CONSOLE_WIDTH)
        
        # Step 1: Scrape LinkedIn Profile
        print("\n📍 STEP 1: EXTRACTING LINKEDIN DATA")
        print("-" * 40)
        
        linkedin_data = self.linkedin_scraper.scrape_profile(linkedin_url)
        if not linkedin_data:
            print("❌ Failed to extract LinkedIn data. Cannot proceed.")
            return None
        
        return self._complete_profile_generation(linkedin_data, meeting_context)
    
    def generate_profile_from_name(self, person_name, company_name="", meeting_context="", verbose=False):
        """Generate profile briefing by searching for person by name"""
        self.verbose = verbose
        
        print("=" * CONSOLE_WIDTH)
        print("🤖 AI PROFILE GENERATOR - NAME SEARCH")
        print("=" * CONSOLE_WIDTH)
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👤 Person Name: {person_name}")
        if company_name:
            print(f"🏢 Company: {company_name}")
        if meeting_context:
            print(f"📋 Meeting Context: {meeting_context}")
        print("=" * CONSOLE_WIDTH)
        
        # Step 1: Search for LinkedIn Profile
        print("\n🔍 STEP 1: SEARCHING FOR LINKEDIN PROFILE")
        print("-" * 40)
        
        linkedin_data = self.linkedin_scraper.scrape_profile_by_name(
            person_name, company_name
        )
        
        if not linkedin_data:
            print("❌ Failed to find or extract LinkedIn data. Cannot proceed.")
            print("💡 Try providing more specific information or a direct LinkedIn URL.")
            return None
        
        return self._complete_profile_generation(linkedin_data, meeting_context)
    
    def _complete_profile_generation(self, linkedin_data, meeting_context):
        """Complete the profile generation process after LinkedIn data is obtained"""
        
        if self.verbose:
            self.print_linkedin_summary(linkedin_data)
        
        # Step 2: Collect News Articles
        print(f"\n📰 STEP 2: COLLECTING NEWS ARTICLES")
        print("-" * 40)
        
        news_articles = self.news_collector.search_person_news(
            linkedin_data.get('name', ''),
            linkedin_data.get('company', ''),
            linkedin_data.get('title', '')
        )
        
        if self.verbose and news_articles:
            self.print_news_summary(news_articles)
        
        # Step 3: Generate AI Briefing
        print(f"\n🤖 STEP 3: GENERATING AI BRIEFING")
        print("-" * 40)
        
        briefing = self.ai_processor.generate_briefing(
            linkedin_data, 
            news_articles, 
            meeting_context
        )
        
        if not briefing:
            print("❌ Failed to generate briefing.")
            return None
        
        # Step 4: Display Results
        print(f"\n✅ BRIEFING GENERATION COMPLETE")
        print("=" * CONSOLE_WIDTH)
        
        self.display_briefing(linkedin_data, briefing, news_articles)
        
        return briefing
    
    def print_linkedin_summary(self, linkedin_data):
        """Print summary of extracted LinkedIn data"""
        print(f"✅ Extracted profile for: {linkedin_data.get('name', 'Unknown')}")
        print(f"   Title: {linkedin_data.get('title', 'N/A')}")
        print(f"   Company: {linkedin_data.get('company', 'N/A')}")
        print(f"   Location: {linkedin_data.get('location', 'N/A')}")
        if linkedin_data.get('experience'):
            print(f"   Experience entries: {len(linkedin_data['experience'])}")
        if linkedin_data.get('education'):
            print(f"   Education entries: {len(linkedin_data['education'])}")
    
    def print_news_summary(self, news_articles):
        """Print summary of collected news articles"""
        print(f"✅ Found {len(news_articles)} relevant news articles:")
        for i, article in enumerate(news_articles[:3], 1):
            print(f"   {i}. {article['title'][:60]}..." if len(article['title']) > 60 else f"   {i}. {article['title']}")
            print(f"      Source: {article['source']} | Score: {article['relevance_score']}")
    
    def display_briefing(self, linkedin_data, briefing, news_articles):
        """Display the complete briefing in formatted output"""
        
        # Header with person info
        print("\n🎯 AI PROFILE BRIEFING")
        print("=" * CONSOLE_WIDTH)
        print(f"PERSON: {linkedin_data.get('name', 'Unknown')}")
        print(f"TITLE: {linkedin_data.get('title', 'N/A')}")
        print(f"COMPANY: {linkedin_data.get('company', 'N/A')}")
        print(f"LINKEDIN: {linkedin_data.get('url', 'N/A')}")
        print(f"CONFIDENCE SCORE: {briefing.get('confidence_score', 0)}/100")
        print()
        
        # Executive Summary
        self.print_section("EXECUTIVE SUMMARY", briefing.get('executive_summary', ''))
        
        # Key Insights
        self.print_list_section("KEY INSIGHTS", briefing.get('key_insights', []))
        
        # Conversation Starters
        self.print_list_section("CONVERSATION STARTERS", briefing.get('conversation_starters', []))
        
        # Recent Activity
        if briefing.get('recent_activity'):
            self.print_section("RECENT NEWS & ACTIVITIES", briefing.get('recent_activity'))
        
        # Meeting Preparation
        self.print_list_section("MEETING PREPARATION NOTES", briefing.get('meeting_preparation', []))
        
        # Strategic Notes
        if briefing.get('strategic_notes'):
            self.print_list_section("STRATEGIC NOTES", briefing.get('strategic_notes', []))
        
        # News Articles Detail
        if news_articles and self.verbose:
            self.print_news_details(news_articles)
        
        # Footer
        print("=" * CONSOLE_WIDTH)
        print(f"⏰ Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔗 Powered by AI Profile Generator")
        print("=" * CONSOLE_WIDTH)
    
    def print_section(self, title, content):
        """Print a section with title and content"""
        print(f"\n📋 {title}")
        print("=" * CONSOLE_WIDTH)
        if content:
            # Wrap long text
            words = content.split()
            line = ""
            for word in words:
                if len(line + word) < CONSOLE_WIDTH - 2:
                    line += word + " "
                else:
                    print(line.strip())
                    line = word + " "
            if line:
                print(line.strip())
        else:
            print("No information available.")
    
    def print_list_section(self, title, items):
        """Print a section with bulleted list items"""
        print(f"\n📋 {title}")
        print("=" * CONSOLE_WIDTH)
        if items:
            for item in items:
                if item.strip():
                    # Wrap long items
                    if len(item) <= CONSOLE_WIDTH - 4:
                        print(f"• {item}")
                    else:
                        words = item.split()
                        line = "• "
                        for word in words:
                            if len(line + word) < CONSOLE_WIDTH - 2:
                                line += word + " "
                            else:
                                print(line.strip())
                                line = "  " + word + " "
                        if line.strip() != "•":
                            print(line.strip())
        else:
            print("No items available.")
    
    def print_news_details(self, news_articles):
        """Print detailed news articles information"""
        print(f"\n📰 DETAILED NEWS ARTICLES")
        print("=" * CONSOLE_WIDTH)
        
        for i, article in enumerate(news_articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Source: {article['source']}")
            try:
                pub_date = datetime.strptime(article['published_at'][:10], '%Y-%m-%d')
                formatted_date = pub_date.strftime('%B %d, %Y')
                print(f"   Date: {formatted_date}")
            except:
                print(f"   Date: {article['published_at'][:10]}")
            
            print(f"   Relevance Score: {article['relevance_score']}")
            if article.get('description'):
                desc = article['description'][:200] + "..." if len(article['description']) > 200 else article['description']
                print(f"   Description: {desc}")
            print(f"   URL: {article['url']}")


def main():
    """Main function to handle command line arguments and run the generator"""
    
    parser = argparse.ArgumentParser(
        description='Generate AI-powered profile briefings from LinkedIn URLs or person names',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using LinkedIn URL:
  python profile_generator.py https://linkedin.com/in/johndoe
  python profile_generator.py https://linkedin.com/in/janedoe --verbose
  python profile_generator.py https://linkedin.com/in/ceo --context "Partnership meeting"
  
  # Using person name:  
  python profile_generator.py --name "John Doe"
  python profile_generator.py --name "Jane Smith" --company "Microsoft" --verbose
  python profile_generator.py --name "CEO Name" --company "TechCorp" --context "Investment meeting"
  
API Keys Required:
  - Azure OpenAI API key for briefing generation
  - News API key for article collection
  
Add your API keys to config.py or set as environment variables:
  - AZURE_OPENAI_KEY
  - NEWS_API_KEY
        """
    )
    
    parser.add_argument(
        'linkedin_url',
        nargs='?',  # Make it optional
        help='LinkedIn profile URL (e.g., https://linkedin.com/in/username)'
    )
    
    parser.add_argument(
        '--name', '-n',
        type=str,
        help='Person name to search for LinkedIn profile'
    )
    
    parser.add_argument(
        '--company', '-co',
        type=str,
        help='Company name to help with LinkedIn profile search'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress and additional information'
    )
    
    parser.add_argument(
        '--context', '-c',
        type=str,
        default='',
        help='Meeting context or purpose (e.g., "Partnership discussion")'
    )
    
    args = parser.parse_args()
    
    # Validate input - must have either URL or name
    if not args.linkedin_url and not args.name:
        print("❌ Error: Please provide either a LinkedIn URL or a person name")
        print("   Examples:")
        print("   python profile_generator.py https://linkedin.com/in/username")
        print("   python profile_generator.py --name \"John Doe\" --company \"Microsoft\"")
        sys.exit(1)
    
    # Create generator instance
    generator = ProfileGenerator()
    
    # Validate LinkedIn URL format if provided
    if args.linkedin_url and not generator.is_linkedin_url(args.linkedin_url):
        print("❌ Error: Please provide a valid LinkedIn profile URL")
        print("   Format: https://linkedin.com/in/username")
        sys.exit(1)
    
    try:
        start_time = time.time()
        
        # Choose method based on input
        if args.linkedin_url:
            print("🔗 Using LinkedIn URL method...")
            result = generator.generate_profile_from_url(
                args.linkedin_url,
                args.context,
                args.verbose
            )
        else:  # args.name is provided
            print("👤 Using name search method...")
            result = generator.generate_profile_from_name(
                args.name,
                args.company or "",
                args.context,
                args.verbose
            )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result:
            print(f"\n⏱️  Total processing time: {duration:.1f} seconds")
            print("✅ Profile briefing completed successfully!")
        else:
            print("\n❌ Profile generation failed. Please check the input and try again.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 