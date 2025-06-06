"""
News Collector for AI Profile Generator
Fetches recent news articles about people and companies using News API
"""

import requests
import time
from datetime import datetime, timedelta
from urllib.parse import quote
from config import NEWS_API_KEY, NEWS_SEARCH_DAYS, MAX_NEWS_ARTICLES


class NewsCollector:
    def __init__(self):
        self.api_key = NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2"
        self.session = requests.Session()
    
    def validate_api_key(self):
        """Check if News API key is valid"""
        if not self.api_key or self.api_key == 'your_news_api_key_here':
            print("⚠️  News API key not configured. Please add your key to config.py")
            return False
        return True
    
    def search_person_news(self, person_name, company_name="", person_title=""):
        """
        Search for news articles about a specific person
        Returns list of relevant articles
        """
        if not self.validate_api_key():
            return []
        
        print(f"📰 Searching for news about {person_name}...")
        
        try:
            # Build search query
            query = self.build_search_query(person_name, company_name, person_title)
            print(f"🔍 Search query: {query}")
            
            # Calculate date range
            from_date = datetime.now() - timedelta(days=NEWS_SEARCH_DAYS)
            from_date_str = from_date.strftime('%Y-%m-%d')
            
            # Make API request
            params = {
                'q': query,
                'from': from_date_str,
                'sortBy': 'publishedAt',
                'language': 'en',
                'pageSize': MAX_NEWS_ARTICLES * 2,  # Get more to filter better
                'apiKey': self.api_key
            }
            
            response = self.session.get(f"{self.base_url}/everything", params=params)
            
            if response.status_code == 429:
                print("⚠️  News API rate limit reached. Please try again later.")
                return []
            
            if response.status_code == 401:
                print("❌ News API authentication failed. Check your API key.")
                return []
            
            if response.status_code != 200:
                print(f"❌ News API error. Status code: {response.status_code}")
                return []
            
            data = response.json()
            
            if data.get('status') != 'ok':
                print(f"❌ News API error: {data.get('message', 'Unknown error')}")
                return []
            
            articles = data.get('articles', [])
            
            if not articles:
                print("📰 No recent news articles found.")
                return []
            
            # Process and filter articles
            processed_articles = self.process_articles(articles, person_name, company_name)
            
            # Sort by relevance and return top articles
            processed_articles.sort(key=lambda x: x['relevance_score'], reverse=True)
            final_articles = processed_articles[:MAX_NEWS_ARTICLES]
            
            print(f"✅ Found {len(final_articles)} relevant news articles")
            return final_articles
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error while fetching news: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error in news collection: {e}")
            return []
    
    def build_search_query(self, person_name, company_name="", person_title=""):
        """Build search query for News API"""
        # Start with person name in quotes for exact match
        query_parts = [f'"{person_name}"']
        
        # Add company name if available
        if company_name:
            query_parts.append(f'"{company_name}"')
        
        # Add title-related keywords if available
        if person_title:
            # Extract key words from title
            title_words = person_title.lower().split()
            important_titles = ['ceo', 'cto', 'cfo', 'president', 'founder', 'director', 'manager']
            for word in title_words:
                if word in important_titles:
                    query_parts.append(word)
        
        # Join with OR to get broader results
        query = ' OR '.join(query_parts)
        
        # Add some business/professional context
        query += ' AND (business OR company OR executive OR announcement OR interview OR leadership)'
        
        return query
    
    def process_articles(self, articles, person_name, company_name):
        """Process and score articles for relevance"""
        processed = []
        
        for article in articles:
            try:
                # Basic article data
                processed_article = {
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'author': article.get('author', ''),
                }
                
                # Skip articles with missing essential data
                if not processed_article['title'] or not processed_article['url']:
                    continue
                
                # Calculate relevance score
                relevance_score = self.calculate_relevance_score(
                    processed_article, 
                    person_name, 
                    company_name
                )
                
                processed_article['relevance_score'] = relevance_score
                
                # Only include articles with decent relevance
                if relevance_score >= 10:
                    processed.append(processed_article)
                    
            except Exception as e:
                print(f"⚠️  Error processing article: {e}")
                continue
        
        return processed
    
    def calculate_relevance_score(self, article, person_name, company_name):
        """Calculate relevance score for an article"""
        score = 0
        
        # Combine title and description for analysis
        content = f"{article['title']} {article['description']}".lower()
        person_name_lower = person_name.lower()
        company_name_lower = company_name.lower() if company_name else ""
        
        # Person name mentions
        if person_name_lower in content:
            score += 30  # High score for person name
        
        # Company name mentions
        if company_name_lower and company_name_lower in content:
            score += 20
        
        # Recency bonus (more recent = higher score)
        try:
            pub_date = datetime.strptime(article['published_at'][:10], '%Y-%m-%d')
            days_ago = (datetime.now() - pub_date).days
            recency_score = max(0, 20 - days_ago)  # Up to 20 points for very recent
            score += recency_score
        except:
            pass  # Skip if date parsing fails
        
        # Source credibility bonus
        credible_sources = [
            'reuters', 'bloomberg', 'wall street journal', 'financial times',
            'techcrunch', 'forbes', 'business insider', 'cnbc', 'bbc',
            'associated press', 'axios', 'politico'
        ]
        
        source_name = article['source'].lower()
        for credible_source in credible_sources:
            if credible_source in source_name:
                score += 10
                break
        
        # Business relevance keywords
        business_keywords = [
            'ceo', 'executive', 'company', 'business', 'announces', 'appointed',
            'leadership', 'interview', 'strategy', 'investment', 'funding',
            'merger', 'acquisition', 'partnership', 'conference', 'speaking'
        ]
        
        for keyword in business_keywords:
            if keyword in content:
                score += 2
        
        # Negative scoring for irrelevant content
        negative_keywords = ['sports', 'entertainment', 'celebrity', 'gossip']
        for keyword in negative_keywords:
            if keyword in content:
                score -= 5
        
        return max(0, score)  # Ensure non-negative score
    
    def format_article_for_display(self, article):
        """Format article for console display"""
        try:
            pub_date = datetime.strptime(article['published_at'][:10], '%Y-%m-%d')
            formatted_date = pub_date.strftime('%B %d, %Y')
        except:
            formatted_date = article['published_at'][:10]
        
        return {
            'title': article['title'][:80] + '...' if len(article['title']) > 80 else article['title'],
            'source': article['source'],
            'date': formatted_date,
            'url': article['url'],
            'description': article['description'][:150] + '...' if article['description'] and len(article['description']) > 150 else article['description']
        }
    
    def get_company_news(self, company_name):
        """Get general news about a company"""
        if not company_name or not self.validate_api_key():
            return []
        
        print(f"🏢 Searching for company news about {company_name}...")
        
        try:
            query = f'"{company_name}" AND (announcement OR earnings OR product OR launch OR partnership)'
            
            from_date = datetime.now() - timedelta(days=NEWS_SEARCH_DAYS)
            from_date_str = from_date.strftime('%Y-%m-%d')
            
            params = {
                'q': query,
                'from': from_date_str,
                'sortBy': 'publishedAt',
                'language': 'en',
                'pageSize': 5,
                'apiKey': self.api_key
            }
            
            response = self.session.get(f"{self.base_url}/everything", params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                return self.process_articles(articles, "", company_name)[:3]  # Return top 3
            
            return []
            
        except Exception as e:
            print(f"❌ Error fetching company news: {e}")
            return []


def test_news_collector():
    """Test function for the news collector"""
    collector = NewsCollector()
    
    # Test with sample person
    test_person = "Satya Nadella"
    test_company = "Microsoft"
    
    print(f"Testing news collector for {test_person} at {test_company}")
    
    articles = collector.search_person_news(test_person, test_company, "CEO")
    
    if articles:
        print(f"✅ Found {len(articles)} articles!")
        for i, article in enumerate(articles[:2], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   Score: {article['relevance_score']}")
    else:
        print("❌ No articles found or API not configured")


if __name__ == "__main__":
    test_news_collector() 