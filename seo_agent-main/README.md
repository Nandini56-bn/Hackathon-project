# 🤖 SEO & Citation Agent - Complete Implementation

A true **agentic AI system** that analyzes websites for SEO, provides citations, learns from past actions, and improves recommendations over time using Hindsight Memory.

## 🎯 Project Overview

This is **NOT a simple chatbot**. It's a complete agentic system that:

- ✅ **Thinks & Reasons**: Uses Groq LLM for intelligent decision-making
- ✅ **Remembers**: Stores all analyses in Hindsight Memory
- ✅ **Learns**: Improves recommendations based on past suggestions
- ✅ **Provides Citations**: Every recommendation is cited with sources
- ✅ **Tracks Progress**: Shows SEO improvements over time
- ✅ **Makes Decisions Dynamically**: Tool selection based on reasoning

## 🏗️ Project Structure

```
seo agent/
├── backend/
│   └── main.py                 # FastAPI backend with all endpoints
├── frontend/
│   └── index.html             # Modern, responsive UI
├── agent/
│   └── seo_agent.py           # Core agent logic with LLM integration
├── tools/
│   └── seo_tools.py           # SEO analysis, scraping, keyword tools
├── memory/
│   └── hindsight_memory.py    # Hindsight memory system
├── config/
│   └── settings.py            # Configuration settings
├── data/
│   └── memory/                # Memory storage (auto-created)
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- pip (Python package manager)
- Groq API key (free at https://console.groq.com)
- Optional: OpenAI API key (for GPT-4 upgrade)

### 2. Installation

```bash
# Navigate to project directory
cd "c:\Users\Lenovo\OneDrive\Desktop\seo agent"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
# Windows: notepad .env
# You need at minimum:
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the System

**Terminal 1 - Start Backend:**
```bash
cd backend
python main.py
```

You should see:
```
🚀 Starting SEO Agent API Server...
📍 Server: http://127.0.0.1:8000
🔗 API Docs: http://127.0.0.1:8000/docs
📊 Groq LLM: ✅ Available
```

**Terminal 2 - Open Frontend:**
```bash
# Option A: Open in browser
start frontend\index.html

# Option B: Use Python's built-in server
cd frontend
python -m http.server 8001
# Then open http://localhost:8001
```

## 💡 How It Works

### The Agentic Loop

```
User Input
    ↓
Agent Analyzes Query
    ↓
Decide Which Tools to Use
    ↓
Execute Tools (SEO Analysis, Web Scraping, Keyword Analysis)
    ↓
Check Hindsight Memory (Past Analyses)
    ↓
Use Groq LLM for Reasoning
    ↓
Generate Recommendations with Citations
    ↓
Store Learnings in Memory
    ↓
Display Results & Improvement Metrics
    ↓
Next Analysis is Smarter (Learning Loop)
```

### Memory System (Hindsight)

The agent stores:

1. **Analysis History**: All previous website analyses
2. **Suggestions**: What was recommended and if it worked
3. **Keyword Performance**: How keywords ranked over time
4. **Improvement Metrics**: Overall progress tracking
5. **Learning Insights**: Patterns of what works

Sample memory structure:
```json
{
  "website": "https://example.com",
  "analyses": [
    {
      "timestamp": "2024-01-15T10:00:00",
      "seo_score": 45,
      "issues": ["Missing meta description", "Poor heading structure"],
      "recommendations": ["Add meta description", "Improve H1 tag"]
    },
    {
      "timestamp": "2024-01-20T10:00:00",
      "seo_score": 62,
      "improvements": ["+17 points", "Meta description added"],
      "new_recommendations": ["Focus on keywords", "Improve page speed"]
    }
  ]
}
```

## 🧠 Agent Components

### 1. **SEO Analyzer Tool** (`tools/seo_tools.py`)

Analyzes:
- Title tag (length, optimization)
- Meta descriptions
- Heading structure (H1, H2, H3)
- Image alt text
- Internal/external links
- Mobile-friendliness indicators
- Schema markup
- Page speed estimate

**Issues Detected:**
- Missing or duplicate H1 tags
- Title too short/long
- Meta description missing/too long
- Images without alt text
- Broken links
- Missing schema markup

### 2. **Web Scraper Tool**

Extracts:
- Page content
- Meta tags
- Headings
- Links
- Images

### 3. **Keyword Analyzer Tool**

- Identifies keywords from content
- Calculates frequency
- Provides difficulty estimates
- Mock competitor analysis

### 4. **Citation Generator**

Generates cited recommendations:
```
"Recommendation: Add meta description"
Citation: "Based on SEO Best Practices & Industry Standards"
Source: https://moz.com/learn/seo
```

### 5. **Hindsight Memory**

Stores and retrieves:
- Analysis history
- Past suggestions
- Keyword performance
- Improvement calculations
- Learning insights

Methods:
- `store_analysis()` - Save website analysis
- `get_analysis_history()` - Retrieve past analyses
- `store_suggestion()` - Save a recommendation
- `calculate_improvement()` - Track progress
- `get_learning_insights()` - Generate ML-based recommendations

## 🔌 API Endpoints

### Core Endpoints

**POST /api/analyze**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d "{
    \"website_url\": \"https://example.com\",
    \"simulate_improvement\": true,
    \"improvement_days\": 5
  }"
```

Response:
```json
{
  "seo_score": 65.4,
  "issues_found": [...],
  "recommendations": [...],
  "improvement_metrics": {
    "improvement_percentage": 18.5,
    "keywords_improved": 3,
    "current_score": 65.4
  }
}
```

**GET /api/memory/{website_url}**
```bash
curl http://localhost:8000/api/memory/example.com
```

Returns:
- analyses_performed
- suggestions_made
- improvement_metrics
- learning_insights

**POST /api/simulate-improvement**
```bash
curl -X POST http://localhost:8000/api/simulate-improvement \
  -d "website_url=example.com&days=5"
```

**GET /api/memory-stats**
```bash
curl http://localhost:8000/api/memory-stats
```

**DELETE /api/memory/{website_url}**
```bash
curl -X DELETE http://localhost:8000/api/memory/example.com
```

## 🎨 Frontend Features

### Dashboard

- **SEO Score Display**: Color-coded score (0-100)
- **Issues Panel**: Lists all SEO issues found
- **Recommendations**: Shows AI-generated recommendations with sources
- **Memory Status**: Shows how many analyses the agent has performed
- **Improvement Tracking**: Shows progress over time
- **Simulated Improvements**: Demonstrates learning capability

### Recommendation Types

1. **Automatic**: From analysis rules
2. **LLM Generated**: From Groq AI reasoning
3. **Learned**: From past improvements

## 📊 Learning Demonstration

### Example: Day 1 vs Day 5

**Day 1 - First Analysis**
- SEO Score: 45
- Issues: 8
- Title missing, meta description too short, no H1 tag

**Day 5 - After Improvements**
- SEO Score: 62 (+17 points)
- Issues: 5 (-3)
- Keywords improved: 3 out of 5

Memory shows:
```
"Improvement: +37.7% over 5 days"
"Effective strategies: Added meta descriptions, Optimized titles"
"Recommendations for future: Focus on keywords showing improvement"
```

## 🔑 Key Features

### 1. True Agentic Behavior

The agent:
- Decides which tools to call based on context
- Reasons about results using LLM
- Prioritizes recommendations
- Learns from outcomes

### 2. Memory Integration

- Stores everything in `data/memory/`
- Retrieves past analyses
- Identifies patterns
- Improves over time

### 3. LLM-Powered Reasoning

Uses Groq LLM to:
- Generate custom recommendations
- Consider past attempts
- Explain reasoning
- Provide nuanced suggestions

### 4. Citation System

Every recommendation includes:
- The action
- The reason (citation)
- Source reference
- Expected impact

### 5. Real-time Tracking

Shows:
- SEO score progression
- Keyword rankings over time
- Issue resolution
- Effectiveness metrics

## 🧪 Testing the System

### Test 1: Basic Analysis

```
1. Open frontend/index.html
2. Enter: https://www.example.com
3. Click "Analyze"
4. View SEO score and recommendations
```

### Test 2: Memory & Learning

```
1. Analyze a website first time
2. Check "Memory Status"
3. Analyze same website again
4. Memory shows: "2 analyses performed"
5. See learning insights
```

### Test 3: Simulated Improvement

```
1. Enable "Simulate ranking improvements"
2. Set to 5 days
3. Analyze
4. View "Improvements" tab
5. See simulated keyword rankings
```

### Test 4: API Direct Testing

```
# Health check
curl http://localhost:8000/health

# Get API docs
http://localhost:8000/docs

# Test analysis
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"website_url":"https://example.com"}'
```

## 🛠️ Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is in use
# Windows: netstat -ano | findstr :8000
# Kill process and retry
```

### Groq API not working

```bash
# Verify API key in .env
# Check: https://console.groq.com
# Test with curl:
curl https://api.groq.com/health -H "Authorization: Bearer YOUR_KEY"
```

### Frontend can't connect to backend

```bash
# Make sure backend is running on port 8000
# Check CORS settings in config/settings.py
# Browser console will show exact error
```

### Memory not persisting

```bash
# Check data/memory/ directory exists
# Ensure application has write permissions
# Memory files are in JSON format - check for errors
```

## 📈 Metrics Explained

### SEO Score

Weighted calculation:
- Title: 15%
- Meta description: 10%
- Headings: 15%
- Keywords: 15%
- Images: 10%
- Links: 10%
- Mobile: 10%
- Speed: 10%
- Schema: 5%

### Improvement Percentage

```
(Current Score - Initial Score) / Initial Score * 100
```

### Keywords Improved

Count of keywords where rank decreased (1 = better, 100 = worse)

## 🚀 Advanced Configuration

### Use OpenAI GPT-4

Edit `config/settings.py`:

```python
PRIMARY_LLM = "openai"
OPENAI_MODEL = "gpt-4"
```

Add to `.env`:
```
OPENAI_API_KEY=sk-...
```

### Use Different Groq Model

Edit `config/settings.py`:

```python
GROQ_MODEL = "qwen-32b"  # or gpt-oss-120b
```

### Adjust Memory Directory

Edit `config/settings.py`:

```python
MEMORY_DIR = "/path/to/memory"
```

## 📝 Code Examples

### Using Agent Programmatically

```python
from agent.seo_agent import SEOAgent

# Initialize
agent = SEOAgent(groq_api_key="your_key")

# Analyze website
result = agent.analyze_website("https://example.com")

# Check memory
memory_status = agent.get_agent_memory_status("https://example.com")

# Get insights
insights = agent.memory.get_learning_insights("https://example.com")
```

### Direct Memory Access

```python
from memory.hindsight_memory import HindsightMemory

memory = HindsightMemory()

# Store analysis
memory.store_analysis(
    "https://example.com",
    {"seo_score": 65, "issues": [...]}
)

# Get history
history = memory.get_analysis_history("https://example.com")

# Calculate improvements
improvements = memory.calculate_improvement("https://example.com")
```

## 📚 Documentation

- **Agent Logic**: See `agent/seo_agent.py` for reasoning flow
- **Memory System**: See `memory/hindsight_memory.py` for storage
- **Tools**: See `tools/seo_tools.py` for SEO analysis details
- **Backend**: See `backend/main.py` for API endpoints
- **Frontend**: See `frontend/index.html` for UI code

## 🎓 Learning Resources

### SEO Best Practices
- https://moz.com/learn/seo
- https://www.search.gov
- https://developers.google.com/search

### Agentic AI Concepts
- Tool calling & function definitions
- Reasoning before acting
- Memory & context management
- Learning from past interactions

### Groq LLM
- https://console.groq.com
- Models: Mixtral, LLaMA, Qwen
- Fast inference with quality output

## 🤝 Contributing

To extend the system:

1. **Add New Tools**: Extend `tools/seo_tools.py`
2. **Add Memory Metrics**: Extend `memory/hindsight_memory.py`
3. **Add API Endpoints**: Extend `backend/main.py`
4. **Improve UI**: Modify `frontend/index.html`

## 📜 License

This project is provided as-is for educational and commercial use.

## 🎉 Summary

This is a **complete, production-ready agentic AI system** that:

✅ Performs intelligent website analysis  
✅ Uses LLM for reasoning and recommendations  
✅ Stores everything in persistent memory  
✅ Demonstrates continuous learning  
✅ Provides citations for all suggestions  
✅ Shows improvement tracking  
✅ Has modern, responsive UI  
✅ Includes comprehensive API  
✅ Is easily extensible  

**Start using it now and watch it get smarter over time!** 🚀

---

**Questions?** Check API docs at `http://localhost:8000/docs` after starting the backend.
