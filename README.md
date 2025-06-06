# AI Profile Generator

> Generate AI-powered briefings about people before meetings using LinkedIn profiles and real-time news data.

## 🎯 Overview

The AI Profile Generator is a command-line tool that extracts LinkedIn profile data, fetches recent news articles, and uses Azure OpenAI to generate comprehensive briefings for business meetings. Perfect for consultants, sales professionals, and anyone who needs quick intelligence about meeting contacts.

**New Feature**: You can now search for LinkedIn profiles by **person name** in addition to using direct LinkedIn URLs!

## ✨ Features

- **Dual Search Methods**: Search by LinkedIn URL OR person name + company
- **LinkedIn Profile Extraction**: Scrapes public LinkedIn profiles ethically
- **Google Search Integration**: Finds LinkedIn profiles automatically by name
- **Real-time News Integration**: Fetches recent articles using News API
- **AI-Powered Analysis**: Uses Azure OpenAI GPT models for intelligent briefings
- **Professional Output**: Formatted console output perfect for quick reading
- **Configurable Context**: Add meeting context for tailored insights
- **Verbose Mode**: Detailed progress and additional information

## 🛠 Installation

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI API key
- News API key (free tier available)

### Quick Setup

1. **Clone or download the project files**:
   ```bash
   # Create project directory
   mkdir ai-profile-generator
   cd ai-profile-generator
   
   # Copy all the Python files to this directory
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**:
   
   Edit `config.py` and add your API keys:
   ```python
   AZURE_OPENAI_KEY = "your_azure_openai_key_here"
   AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
   AZURE_OPENAI_DEPLOYMENT = "your-deployment-name"
   NEWS_API_KEY = "your_news_api_key_here"
   ```
   
   **OR** set environment variables:
   ```bash
   export AZURE_OPENAI_KEY="your_azure_openai_key_here"
   export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
   export NEWS_API_KEY="your_news_api_key_here"
   ```

## 🔑 API Keys Setup

### Azure OpenAI API Key
1. Go to [Azure Portal](https://portal.azure.com/)
2. Create or access your Azure OpenAI Service
3. Get your API key, endpoint, and deployment name
4. Cost: ~$0.01-0.05 per profile generation

### News API Key
1. Go to [NewsAPI.org](https://newsapi.org/)
2. Sign up for free account
3. Get your API key
4. Free tier: 1000 requests per day

## 🚀 Usage

### Method 1: Using LinkedIn URL

```bash
# Basic usage with LinkedIn URL
python profile_generator.py https://linkedin.com/in/username

# With meeting context
python profile_generator.py https://linkedin.com/in/username --context "Partnership discussion"

# Verbose mode
python profile_generator.py https://linkedin.com/in/username --verbose
```

### Method 2: Using Person Name (NEW!)

```bash
# Basic name search
python profile_generator.py --name "John Doe"

# With company context (recommended for better accuracy)
python profile_generator.py --name "Satya Nadella" --company "Microsoft"

# With meeting context and verbose mode
python profile_generator.py --name "Tim Cook" --company "Apple" --context "Partnership meeting" --verbose
```

### Advanced Examples

```bash
# Search for CEO without knowing LinkedIn URL
python profile_generator.py --name "Sundar Pichai" --company "Google"

# Search with partial company info
python profile_generator.py --name "Reid Hoffman" --company "LinkedIn"

# Meeting-specific context
python profile_generator.py --name "Melinda Gates" --context "Philanthropic partnership discussion"
```

### Help
```bash
python profile_generator.py --help
```

## 📋 Example Output

```
============================================================
🤖 AI PROFILE GENERATOR - NAME SEARCH
============================================================
⏰ Started at: 2024-01-15 14:30:25
👤 Person Name: Satya Nadella
🏢 Company: Microsoft
============================================================

🔍 STEP 1: SEARCHING FOR LINKEDIN PROFILE
----------------------------------------
🔍 Searching for LinkedIn profile of: Satya Nadella
   Company context: Microsoft
🌐 Google search query: "Satya Nadella" site:linkedin.com/in/ "Microsoft"
✅ Found 3 potential LinkedIn profiles
📍 Found LinkedIn URL: https://www.linkedin.com/in/satyanadella/
🔍 Scraping LinkedIn profile...
✅ Successfully extracted profile for Satya Nadella

📰 STEP 2: COLLECTING NEWS ARTICLES
----------------------------------------
📰 Searching for news about Satya Nadella...
✅ Found 3 relevant news articles

🤖 STEP 3: GENERATING AI BRIEFING
----------------------------------------
🤖 Generating AI briefing with Azure OpenAI...
✅ AI briefing generated successfully!

✅ BRIEFING GENERATION COMPLETE
============================================================

🎯 AI PROFILE BRIEFING
============================================================
PERSON: Satya Nadella
TITLE: Chief Executive Officer
COMPANY: Microsoft
LINKEDIN: https://www.linkedin.com/in/satyanadella/
CONFIDENCE SCORE: 92/100

📋 EXECUTIVE SUMMARY
============================================================
Satya Nadella is the CEO of Microsoft, leading the company's
transformation into a cloud-first, AI-powered technology giant.
Under his leadership since 2014, Microsoft has become one of the
world's most valuable companies.

📋 KEY INSIGHTS
============================================================
• Transformed Microsoft's culture from "know-it-all" to "learn-it-all"
• Led Microsoft's successful pivot to cloud computing with Azure
• Champion of AI integration across Microsoft's product portfolio
• Strong advocate for inclusive technology and accessibility

📋 CONVERSATION STARTERS
============================================================
• Ask about Microsoft's AI strategy and recent OpenAI partnership
• Discuss the cultural transformation at Microsoft
• Explore thoughts on the future of hybrid work and productivity

📋 RECENT NEWS & ACTIVITIES
============================================================
Recent articles highlight Microsoft's continued AI investments and
Satya's thought leadership on responsible AI development. Notable
mentions include Microsoft's quarterly earnings and strategic
partnerships.

📋 MEETING PREPARATION NOTES
============================================================
• Research Microsoft's latest AI announcements and partnerships
• Prepare questions about digital transformation strategies
• Review Microsoft's recent financial performance and market position
• Consider discussing sustainability and corporate responsibility

============================================================
⏰ Generated at: 2024-01-15 14:30:45
🔗 Powered by AI Profile Generator
============================================================

⏱️  Total processing time: 18.2 seconds
✅ Profile briefing completed successfully!
```

## 📁 Project Structure

```
ai-profile-generator/
├── profile_generator.py    # Main script - command-line interface
├── linkedin_scraper.py     # LinkedIn profile data extraction
├── news_collector.py       # News API integration and article collection
├── ai_processor.py         # OpenAI integration and briefing generation
├── config.py              # Configuration and API keys
├── requirements.txt       # Python dependencies
├── sample_profiles.txt    # Test LinkedIn URLs for demo
└── README.md             # This file
```

## 🧪 Testing

Test with sample profiles:
```bash
# Test with a well-known public profile
python profile_generator.py https://www.linkedin.com/in/satyanadella/

# Test with verbose output
python profile_generator.py https://www.linkedin.com/in/sundarpichai/ --verbose

# Test with meeting context
python profile_generator.py https://www.linkedin.com/in/reidhoffman/ --context "Investment discussion"
```

See `sample_profiles.txt` for more test URLs.

## ⚠️ Important Notes

### Ethical Use
- Only use with public LinkedIn profiles
- Respect LinkedIn's terms of service
- Built-in rate limiting and delays
- No authentication bypass or private data access

### Limitations
- Works only with public LinkedIn profiles
- LinkedIn may block requests if used excessively
- News API has daily limits on free tier
- OpenAI API charges per request

### Error Handling
- Graceful fallbacks when APIs are unavailable
- Detailed error messages in verbose mode
- Automatic retry logic for temporary failures

## 🔧 Configuration Options

Edit `config.py` to customize:

```python
# LinkedIn scraping settings
LINKEDIN_DELAY = 3          # Delay between requests (seconds)
LINKEDIN_TIMEOUT = 10       # Request timeout

# News API settings
NEWS_SEARCH_DAYS = 30       # How far back to search for news
MAX_NEWS_ARTICLES = 5       # Maximum articles to fetch

# OpenAI settings
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4" if you have access
MAX_TOKENS = 1500               # Maximum response length
TEMPERATURE = 0.3               # Response creativity (0-1)

# Output formatting
CONSOLE_WIDTH = 60              # Console output width
```

## 🚀 Demo Presentation

Perfect for demonstrating to internal teams:

1. **Show the Problem**: "Manual research takes 30+ minutes per person"
2. **Live Demo**: Run with a real LinkedIn URL
3. **Highlight Results**: Point out AI insights and time savings
4. **Technical Explanation**: "Real LinkedIn scraping + News API + OpenAI"

## 🛡️ Security & Privacy

- No data storage - everything processed in memory
- API keys stored locally only
- No LinkedIn authentication required
- Respects public profile privacy settings

## 🆘 Troubleshooting

### Common Issues

**"LinkedIn scraping failed"**
- Check internet connection
- Verify LinkedIn URL format
- Profile might be private or blocked

**"OpenAI API error"**
- Verify API key in config.py
- Check OpenAI account credits
- Try again if rate limited

**"News API error"**
- Verify API key configuration
- Check daily usage limits
- Ensure proper internet connectivity

### Getting Help

1. Run with `--verbose` for detailed error information
2. Check API key configuration
3. Verify internet connectivity
4. Test with sample profiles first

## 📈 Future Enhancements

- Web interface with Flask/Django
- Database storage for profile history
- Team collaboration features
- CRM system integration
- Multi-language support
- Custom AI model training

## 📄 License

This project is for educational and internal business use. Please respect LinkedIn's terms of service and use responsibly.

---

**Built for the AI Profile Generator MVP Demo** 🚀 