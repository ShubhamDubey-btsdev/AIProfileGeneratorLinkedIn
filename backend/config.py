"""
Configuration file for AI Profile Generator
Add your API keys here or set them as environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# API Keys - Replace with your actual keys or set as environment variables
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'your_news_api_key_here')

# Azure OpenAI Settings
AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY', '')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://aiconversations.openai.azure.com/')  
AZURE_OPENAI_VERSION = os.getenv('AZURE_OPENAI_VERSION', '2025-01-01-preview')  # API version
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4.1')  # Your model deployment name

# LinkedIn Scraping Settings
LINKEDIN_DELAY = 3  # Delay between requests in seconds
LINKEDIN_TIMEOUT = 10  # Request timeout in seconds

# User Agent for web scraping (rotate these for better success)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

# News API Settings
NEWS_SEARCH_DAYS = 30  # How many days back to search for news
MAX_NEWS_ARTICLES = 5  # Maximum number of articles to fetch

# AI Model Settings
MAX_TOKENS = 1500
TEMPERATURE = 0.3

# Output formatting
CONSOLE_WIDTH = 60  # Width for console output formatting 