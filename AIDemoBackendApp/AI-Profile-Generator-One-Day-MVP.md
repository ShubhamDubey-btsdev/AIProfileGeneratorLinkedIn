# AI Profile Generator - One-Day Python MVP
**Simple Command-Line Demo with Real-Time Data**

## 🎯 MVP Goal
Create a simple Python script: `python profile_generator.py <linkedin_url>` → get real-time data → AI-generated briefing printed to console

## ⏰ One-Day Timeline (6 hours) - Pure Python Version

---

## Hour 1: Setup & Dependencies

### **Environment Setup (30 minutes)**
- Create Python virtual environment
- Install required packages (requests, beautifulsoup4, openai)
- Get API keys (OpenAI, News API)
- Test API connections

### **Project Structure (30 minutes)**
```
ai-profile-demo/
├── profile_generator.py       # Main script
├── linkedin_scraper.py        # LinkedIn data extraction
├── news_collector.py          # News API integration
├── ai_processor.py            # OpenAI briefing generation
├── requirements.txt           # Dependencies
├── config.py                  # API keys and settings
└── sample_profiles.txt        # Test LinkedIn URLs
```

---

## Hour 2: LinkedIn Data Scraper

### **LinkedIn Scraper Module (60 minutes)**
- Create `linkedin_scraper.py`
- Extract: name, title, company, location, about, experience
- Handle different LinkedIn profile formats
- Implement proper delays and headers
- Error handling for private/blocked profiles
- Return structured data dictionary

### **Key Features:**
- Ethical scraping with delays
- Multiple profile format support
- Robust error handling
- Clean data extraction
- Validation of extracted data

---

## Hour 3: News Data Collection

### **News API Integration (60 minutes)**
- Create `news_collector.py`
- Search for person name and company
- Filter articles by relevance and date
- Rank articles by credibility
- Handle API rate limits
- Return top 5 relevant articles

### **News Processing:**
- Person name + company searches
- Date filtering (last 30 days)
- Source credibility scoring
- Relevance ranking
- Clean article summaries

---

## Hour 4: AI Processing Pipeline

### **OpenAI Integration (60 minutes)**
- Create `ai_processor.py`
- Design comprehensive prompts
- Process LinkedIn + News data
- Generate structured briefings
- Handle API errors and retries
- Format output for console display

### **AI Features:**
- Dynamic prompt generation
- Context-aware analysis
- Structured briefing format
- Confidence scoring
- Error handling and fallbacks

---

## Hour 5: Main Script & Integration

### **Main Script Development (60 minutes)**
- Create `profile_generator.py`
- Command-line argument handling
- Orchestrate all modules
- Progress indicators in console
- Error handling and user feedback
- Clean output formatting

### **Command-Line Interface:**
- Input validation
- Progress updates
- Error messages
- Formatted output
- Optional verbose mode

---

## Hour 6: Testing & Demo Preparation

### **Testing & Polish (60 minutes)**
- Test with multiple LinkedIn profiles
- Verify all error scenarios
- Optimize output formatting
- Prepare demo script
- Document usage instructions

---

## 🛠 Simplified Technology Stack

### **Core Dependencies**
- **Python 3.8+** - Main language
- **requests** - HTTP requests for APIs and scraping
- **beautifulsoup4** - HTML parsing for LinkedIn
- **openai** - AI briefing generation
- **python-dotenv** - Environment variable management

### **APIs Used**
- **OpenAI API** - For briefing generation
- **News API** - For real news articles
- **No database** - Direct processing and output

### **No UI Required**
- Command-line interface only
- Console output with formatting
- No authentication needed
- No web server required

---

## 📋 Demo Features (Achievable in 6 hours)

### **Input**
- LinkedIn URL via command line
- Optional verbose flag for detailed output
- Validation of URL format

### **Processing (Real-Time)**
- Live LinkedIn data scraping
- Real news article fetching
- AI briefing generation
- Progress updates in console

### **Output (Formatted Console)**
```
========================================
AI PROFILE BRIEFING
========================================

PERSON: John Doe
TITLE: CEO at TechCorp
LINKEDIN: https://linkedin.com/in/johndoe

========================================
EXECUTIVE SUMMARY
========================================
[AI-generated summary]

========================================
KEY INSIGHTS
========================================
• [Insight 1]
• [Insight 2]
• [Insight 3]

========================================
CONVERSATION STARTERS
========================================
• [Starter 1]
• [Starter 2]

========================================
RECENT NEWS & ACTIVITIES
========================================
• [News item 1] - [Source] - [Date]
• [News item 2] - [Source] - [Date]

========================================
MEETING PREPARATION NOTES
========================================
[Strategic notes for meeting]

========================================
```

---

## 🎯 Usage Examples

### **Basic Usage**
```bash
python profile_generator.py https://linkedin.com/in/johndoe
```

### **Verbose Mode**
```bash
python profile_generator.py https://linkedin.com/in/johndoe --verbose
```

### **Help**
```bash
python profile_generator.py --help
```

---

## 🎬 Demo Script for Presentation

### **Step 1: Show the Problem (30 seconds)**
- "Manual research takes 30+ minutes per person"
- "Here's how AI can do it in real-time"

### **Step 2: Live Demo (3 minutes)**
- Open terminal/command prompt
- Run: `python profile_generator.py https://linkedin.com/in/[demo-profile]`
- Show real-time progress messages
- Display comprehensive output

### **Step 3: Highlight Results (1 minute)**
- Point out AI-generated insights
- Show conversation starters
- Mention news integration
- Emphasize time savings

### **Step 4: Technical Explanation (1 minute)**
- "Pure Python script"
- "Real LinkedIn scraping + News API + OpenAI"
- "Scalable to web application"

---

## 📦 Required API Keys

### **OpenAI API**
- Cost: ~$0.01-0.05 per profile
- Sign up at: https://openai.com/api/
- Add to config.py: `OPENAI_API_KEY = "your_key_here"`

### **News API**
- Free tier: 1000 requests/day
- Sign up at: https://newsapi.org/
- Add to config.py: `NEWS_API_KEY = "your_key_here"`

### **No LinkedIn API needed**
- Uses ethical web scraping
- Respects robots.txt and rate limits
- Public profile data only

---

## ⚡ Success Criteria

### **Technical Success**
- [ ] Scrapes LinkedIn profiles successfully
- [ ] Fetches relevant news articles
- [ ] Generates useful AI briefings
- [ ] Runs without errors
- [ ] Completes in under 30 seconds

### **Demo Success**
- [ ] Impresses internal tech team
- [ ] Shows clear business value
- [ ] Demonstrates technical feasibility
- [ ] Generates excitement for full project

---

## 🚨 Risk Mitigation

### **LinkedIn Blocking**
- **Risk**: Rate limiting or IP blocking
- **Mitigation**: Proper delays, header rotation, tested profiles

### **API Failures**
- **Risk**: OpenAI or News API down
- **Mitigation**: Error handling, retry logic, fallback responses

### **Demo Environment**
- **Risk**: Network issues during presentation
- **Mitigation**: Test on venue network, have mobile hotspot

---

## 💡 Demo Day Preparation

### **Before Demo**
- Test with 3-4 different LinkedIn profiles
- Verify all API keys work
- Test on presentation computer/network
- Prepare backup profiles

### **During Demo**
- Use tested LinkedIn profile
- Show command execution in real-time
- Emphasize "live data" aspect
- Have backup plan ready

### **Talking Points**
- "This is running live against LinkedIn and news APIs"
- "No mock data - everything is real-time"
- "Imagine this scaled to web application"
- "30 minutes of research done in 30 seconds"

---

## 🚀 Post-Demo Enhancement Path

### **Immediate Improvements (Week 2)**
- Add web interface with Flask
- User authentication
- Save/retrieve previous profiles
- Better error handling

### **Production Features (Month 2)**
- Full React frontend
- Database storage
- Team collaboration
- CRM integration

---

## 📋 Installation Instructions

### **Quick Setup**
```bash
# Clone or create project directory
cd ai-profile-demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API keys
copy config.example.py config.py
# Edit config.py with your API keys

# Test installation
python profile_generator.py --help

# Run demo
python profile_generator.py https://linkedin.com/in/[profile]
```

---

## 🎯 Key Message for Tech Team

**"This 6-hour Python script proves the concept works with real data. It's the foundation for a full web application that could transform how our consultants prepare for meetings."**

### **Value Demonstration**
- Real-time data processing
- AI-powered insights
- Significant time savings
- Clear technical path forward

### **Next Steps**
- Build web interface
- Add user management
- Scale infrastructure
- Integrate with existing tools

This simplified approach gives you a working demo that proves the concept without the complexity of frontend development! 