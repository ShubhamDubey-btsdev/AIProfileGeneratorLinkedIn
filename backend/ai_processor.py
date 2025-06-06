"""
AI Processor for Profile Generator
Uses Azure OpenAI to generate comprehensive briefings from LinkedIn and news data
"""

import requests
import json
import os
from datetime import datetime
from config import AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_VERSION, AZURE_OPENAI_DEPLOYMENT, MAX_TOKENS, TEMPERATURE


class AIProcessor:
    def __init__(self):
        self.azure_key = AZURE_OPENAI_KEY
        self.azure_endpoint = AZURE_OPENAI_ENDPOINT
        self.azure_version = AZURE_OPENAI_VERSION
        self.deployment_name = AZURE_OPENAI_DEPLOYMENT
        
        # Build the API URL for Azure OpenAI
        if self.azure_endpoint and self.azure_endpoint.endswith('/'):
            base_url = self.azure_endpoint[:-1]
        else:
            base_url = self.azure_endpoint
            
        self.api_url = f"{base_url}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.azure_version}"
        
        if self.validate_api_key():
            print("✅ Azure OpenAI configuration validated successfully")
            self.client_ready = True
        else:
            print("⚠️  Azure OpenAI credentials not configured. Please add them to config.py")
            self.client_ready = False
    
    def validate_api_key(self):
        """Check if Azure OpenAI credentials are configured"""
        return (self.azure_key and self.azure_key != 'your_azure_openai_key_here' and
                self.azure_endpoint and 'your-resource-name' not in self.azure_endpoint and
                self.deployment_name and self.deployment_name != 'your-deployment-name')
    
    def generate_briefing(self, linkedin_data, news_articles, meeting_context=""):
        """
        Generate comprehensive briefing using Azure OpenAI via direct HTTP calls
        Returns structured briefing data
        """
        if not self.client_ready:
            return self.create_fallback_briefing(linkedin_data, news_articles)
        
        print("🤖 Generating AI briefing with Azure OpenAI...")
        
        try:
            # Build comprehensive prompt
            prompt = self.build_prompt(linkedin_data, news_articles, meeting_context)
            
            # Prepare the request payload
            payload = {
                "messages": [
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS,
                "response_format": {"type": "json_object"}
            }
            
            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_key
            }
            
            # Make the API call
            print(f"🌐 Making request to: {self.api_url}")
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                response_data = response.json()
                briefing_text = response_data['choices'][0]['message']['content']
                briefing_data = json.loads(briefing_text)
                
                print("✅ AI briefing generated successfully!")
                return self.validate_and_format_briefing(briefing_data)
            else:
                print(f"❌ Azure OpenAI API error. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return self.create_fallback_briefing(linkedin_data, news_articles)
                
        except requests.exceptions.Timeout:
            print("⚠️  Request timed out. Azure OpenAI might be slow.")
            return self.create_fallback_briefing(linkedin_data, news_articles)
        except json.JSONDecodeError as e:
            print(f"⚠️  Could not parse AI response: {e}")
            return self.create_fallback_briefing(linkedin_data, news_articles)
        except Exception as e:
            error_msg = str(e).lower()
            if "401" in str(e) or "authentication" in error_msg:
                print("❌ Azure OpenAI authentication failed. Check your API key and endpoint.")
            elif "429" in str(e) or "rate limit" in error_msg:
                print("⚠️  Azure OpenAI rate limit reached. Please try again later.")
            elif "404" in str(e) or "deployment" in error_msg:
                print(f"❌ Azure OpenAI deployment '{self.deployment_name}' not found. Check your deployment name.")
            else:
                print(f"❌ Azure OpenAI API error: {e}")
            
            return self.create_fallback_briefing(linkedin_data, news_articles)
    
    def get_system_prompt(self):
        """System prompt for Azure OpenAI to define its role and output format"""
        return """
        You are an expert business intelligence analyst who creates comprehensive briefings for professional meetings. 
        
        Your task is to analyze LinkedIn profile data and recent news articles to generate actionable insights for business meetings.
        
        Focus on:
        1. Professional background and key expertise
        2. Recent activities and news mentions
        3. Strategic conversation opportunities
        4. Meeting preparation insights
        5. Potential business opportunities or challenges
        
        Always respond with valid JSON in this exact structure:
        {
            "executive_summary": "Comprehensive 2-3 sentence overview",
            "key_insights": [
                "Insight 1 about their background",
                "Insight 2 about recent activities", 
                "Insight 3 about strategic relevance"
            ],
            "conversation_starters": [
                "Question or topic 1",
                "Question or topic 2",
                "Question or topic 3"
            ],
            "recent_activity": "Summary of recent news and activities",
            "meeting_preparation": [
                "Preparation point 1",
                "Preparation point 2",
                "Preparation point 3"
            ],
            "strategic_notes": [
                "Strategic observation 1",
                "Strategic observation 2"
            ],
            "confidence_score": 85
        }
        
        Make insights specific, actionable, and relevant for business meetings.
        """
    
    def build_prompt(self, linkedin_data, news_articles, meeting_context):
        """Build comprehensive prompt for Azure OpenAI"""
        
        # LinkedIn data section
        linkedin_section = f"""
        LINKEDIN PROFILE DATA:
        Name: {linkedin_data.get('name', 'N/A')}
        Title: {linkedin_data.get('title', 'N/A')}
        Company: {linkedin_data.get('company', 'N/A')}
        Location: {linkedin_data.get('location', 'N/A')}
        
        About: {linkedin_data.get('about', 'N/A')}
        
        Experience:
        """
        
        # Add experience details
        for exp in linkedin_data.get('experience', []):
            linkedin_section += f"- {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')} ({exp.get('duration', 'N/A')})\n"
        
        # Add education
        linkedin_section += "\nEducation:\n"
        for edu in linkedin_data.get('education', []):
            linkedin_section += f"- {edu.get('degree', 'N/A')} from {edu.get('school', 'N/A')} ({edu.get('years', 'N/A')})\n"
        
        # News articles section
        news_section = "\nRECENT NEWS ARTICLES:\n"
        if news_articles:
            for i, article in enumerate(news_articles, 1):
                news_section += f"""
                {i}. {article.get('title', 'N/A')}
                   Source: {article.get('source', 'N/A')}
                   Date: {article.get('published_at', 'N/A')[:10]}
                   Description: {article.get('description', 'N/A')}
                """
        else:
            news_section += "No recent news articles found."
        
        # Meeting context section
        context_section = f"\nMEETING CONTEXT:\n{meeting_context if meeting_context else 'General business meeting'}"
        
        # Combine all sections
        full_prompt = f"""
        Please analyze the following professional profile data and generate a comprehensive briefing:
        
        {linkedin_section}
        {news_section}
        {context_section}
        
        Generate a strategic briefing that will help prepare for an effective business meeting with this person.
        Focus on actionable insights, relevant conversation topics, and strategic preparation points.
        """
        
        return full_prompt
    
    def validate_and_format_briefing(self, briefing_data):
        """Validate and format the AI-generated briefing"""
        
        # Default structure
        formatted_briefing = {
            "executive_summary": "",
            "key_insights": [],
            "conversation_starters": [],
            "recent_activity": "",
            "meeting_preparation": [],
            "strategic_notes": [],
            "confidence_score": 0
        }
        
        # Update with AI data, ensuring proper types
        if isinstance(briefing_data, dict):
            formatted_briefing.update({
                "executive_summary": str(briefing_data.get("executive_summary", "")),
                "key_insights": self.ensure_list(briefing_data.get("key_insights", [])),
                "conversation_starters": self.ensure_list(briefing_data.get("conversation_starters", [])),
                "recent_activity": str(briefing_data.get("recent_activity", "")),
                "meeting_preparation": self.ensure_list(briefing_data.get("meeting_preparation", [])),
                "strategic_notes": self.ensure_list(briefing_data.get("strategic_notes", [])),
                "confidence_score": int(briefing_data.get("confidence_score", 75))
            })
        
        return formatted_briefing
    
    def ensure_list(self, data):
        """Ensure data is a list of strings"""
        if isinstance(data, list):
            return [str(item) for item in data if item]
        elif isinstance(data, str):
            return [data] if data else []
        else:
            return []
    
    def create_fallback_briefing(self, linkedin_data, news_articles):
        """Create a basic briefing when Azure OpenAI is not available"""
        print("📝 Creating fallback briefing...")
        
        name = linkedin_data.get('name', 'Unknown')
        title = linkedin_data.get('title', 'Unknown')
        company = linkedin_data.get('company', 'Unknown')
        
        # Basic executive summary
        exec_summary = f"{name} is {title} at {company}."
        if linkedin_data.get('location'):
            exec_summary += f" Based in {linkedin_data['location']}."
        
        # Basic insights from LinkedIn data
        insights = []
        if title:
            insights.append(f"Currently serving as {title}")
        if company:
            insights.append(f"Working at {company}")
        if linkedin_data.get('experience'):
            insights.append(f"Has {len(linkedin_data['experience'])} previous roles listed")
        
        # Basic conversation starters
        conversation_starters = [
            f"Tell me about your role as {title}" if title else "Tell me about your current role",
            f"How is {company} adapting to current market conditions?" if company else "How is your company doing?",
            "What are your biggest priorities this quarter?"
        ]
        
        # Recent activity from news
        recent_activity = "Recent news analysis not available."
        if news_articles:
            recent_activity = f"Found {len(news_articles)} recent news mentions. "
            if news_articles[0].get('title'):
                recent_activity += f"Latest: '{news_articles[0]['title']}'"
        
        # Basic meeting preparation
        meeting_prep = [
            f"Research {company} current initiatives" if company else "Research their company",
            "Prepare questions about their industry challenges",
            "Review recent market trends in their sector"
        ]
        
        return {
            "executive_summary": exec_summary,
            "key_insights": insights[:3],  # Limit to 3
            "conversation_starters": conversation_starters,
            "recent_activity": recent_activity,
            "meeting_preparation": meeting_prep,
            "strategic_notes": [
                "AI analysis not available - this is a basic profile summary",
                "Consider researching additional background before meeting"
            ],
            "confidence_score": 40  # Lower confidence for fallback
        }
    
    def enhance_briefing_with_context(self, briefing, additional_context):
        """Enhance an existing briefing with additional context"""
        if not self.client_ready or not additional_context:
            return briefing
        
        print("🔄 Enhancing briefing with additional context...")
        
        try:
            enhancement_prompt = f"""
            Current briefing summary: {briefing.get('executive_summary', '')}
            
            Additional context: {additional_context}
            
            Please enhance the briefing by incorporating this new information.
            Return the same JSON structure with updated insights.
            """
            
            response = requests.post(
                self.api_url,
                json={
                    "messages": [
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": enhancement_prompt}
                    ],
                    "temperature": 0.2,  # Lower temperature for enhancement
                    "max_tokens": 800,
                    "response_format": {"type": "json_object"}
                },
                headers={
                    "Content-Type": "application/json",
                    "api-key": self.azure_key
                },
                timeout=60
            )
            
            if response.status_code == 200:
                enhanced_data = response.json()['choices'][0]['message']['content']
                return self.validate_and_format_briefing(json.loads(enhanced_data))
            else:
                print(f"❌ Azure OpenAI API error. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return briefing
        except requests.exceptions.Timeout:
            print("⚠️  Request timed out. Azure OpenAI might be slow.")
            return briefing


def test_ai_processor():
    """Test function for the AI processor"""
    processor = AIProcessor()
    
    # Sample LinkedIn data
    sample_linkedin = {
        'name': 'John Doe',
        'title': 'Chief Technology Officer',
        'company': 'TechCorp',
        'location': 'San Francisco, CA',
        'about': 'Experienced technology leader with 15+ years in software development and team management.',
        'experience': [
            {'title': 'CTO', 'company': 'TechCorp', 'duration': '2020 - Present'},
            {'title': 'VP Engineering', 'company': 'StartupCorp', 'duration': '2017 - 2020'}
        ],
        'education': [
            {'degree': 'MS Computer Science', 'school': 'Stanford University', 'years': '2005 - 2007'}
        ]
    }
    
    # Sample news articles
    sample_news = [
        {
            'title': 'TechCorp Announces Major AI Initiative',
            'source': 'TechCrunch',
            'published_at': '2024-01-15',
            'description': 'Company reveals new artificial intelligence strategy led by CTO John Doe'
        }
    ]
    
    print("Testing Azure OpenAI AI processor...")
    briefing = processor.generate_briefing(sample_linkedin, sample_news, "Partnership discussion meeting")
    
    if briefing:
        print("✅ AI processor test successful!")
        print(f"Executive Summary: {briefing['executive_summary'][:100]}...")
        print(f"Key Insights: {len(briefing['key_insights'])} insights generated")
        print(f"Confidence Score: {briefing['confidence_score']}")
    else:
        print("❌ AI processor test failed!")


if __name__ == "__main__":
    test_ai_processor() 