# 🏗️ SYSTEM ARCHITECTURE & DESIGN

## 📐 Overall Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (index.html)                     │
│                   Modern, Responsive React-like UI               │
│                  Dashboard | Analysis | Memory Views             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ HTTP REST API
                       │ http://localhost:8000
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                    FASTAPI BACKEND (main.py)                     │
│                                                                   │
│    POST /api/analyze          → Triggers agent analysis           │
│    GET  /api/memory/{url}     → Retrieves memory status           │
│    POST /api/simulate-improvement → Simulates improvements        │
│    GET  /health               → Health check                      │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌─────────────┐ ┌────────────┐ ┌──────────────┐
│  SEO AGENT   │ │  MEMORY    │ │  TOOLS       │
│              │ │  (Insight) │ │              │
│ • Analyzes   │ │            │ │ • Analyzer   │
│ • Decides    │ │ • Stores   │ │ • Scraper    │
│ • Uses LLM   │ │ • Recalls  │ │ • Keywords   │
│ • Reasons    │ │ • Learns   │ │ • Citations  │
│ • Prioritizes│ │ • Improves │ │              │
└─────────────┘ └────────────┘ └──────────────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
    ┌────────┐    ┌─────────┐    ┌──────────┐
    │ GROQ   │    │ JSON    │    │ Website  │
    │ LLM    │    │ Files   │    │ (Fetch)  │
    │        │    │         │    │          │
    │ • Ask  │    │ • memory│    │ • HTML   │
    │ • Reas │    │ • data  │    │ • Meta   │
    │ • Gen  │    │ • config│    │ • Links  │
    └────────┘    └─────────┘    └──────────┘
```

## 🧩 Component Breakdown

### 1. Frontend (`frontend/index.html`)

**Purpose:** User interface for website analysis

**Features:**
- Responsive design (mobile-friendly)
- Real-time updates with JavaScript
- Multiple tabs for organized display
- Visual SEO score with color coding
- Memory status viewer
- Improvement tracking dashboard

**Interaction Flow:**
```
User Input (URL)
    ↓
Validate URL
    ↓
Send to Backend (/api/analyze)
    ↓
Show Loading Spinner
    ↓
Receive Results
    ↓
Display with Formatting
    ↓
Show in Tabs: Overview | Issues | Recommendations | Memory | Improvements
```

### 2. Backend (`backend/main.py`)

**Purpose:** REST API server for agent coordination

**Endpoints:**
- `POST /api/analyze` - Main analysis
- `GET /api/memory/{url}` - Memory status
- `POST /api/simulate-improvement` - Ranking simulation
- `POST /api/batch-analyze` - Multiple websites
- `GET /api/memory-stats` - Overall stats
- `DELETE /api/memory/{url}` - Clear memory

**Responsibilities:**
- Route requests to agent
- Handle CORS
- Validate input
- Format responses
- Error handling

### 3. Agent (`agent/seo_agent.py`)

**Purpose:** Core decision-making and reasoning engine

**Key Methods:**
```python
analyze_website(url)                    # Main analysis function
_generate_recommendations_with_llm()    # LLM reasoning
_generate_final_report()                # Compile results
simulate_ranking_improvement()          # Demo improvements
get_agent_memory_status()               # Memory report
```

**Decision Flow:**
```
Input: Website URL
    ↓
Fetch & Analyze Website (Tools)
    ↓
Check Memory (Past Analyses)
    ↓
Generate Baseline Recommendations (Rules)
    ↓
Use LLM for AI Reasoning
    ↓
Combine with Learning Insights
    ↓
Generate Citations
    ↓
Store in Memory
    ↓
Return Comprehensive Report
```

### 4. Tools (`tools/seo_tools.py`)

**Purpose:** Specialized functions for analysis

**Tools:**

#### SEOAnalyzerTool
```
analyze_website(url)
├──> _analyze_title()              → Check title tag
├──> _analyze_meta_description()   → Check meta tag
├──> _analyze_headings()           → Check H1, H2, H3
├──> _analyze_keywords()           → Extract keywords
├──> _analyze_images()             → Check alt text
├──> _analyze_links()              → Count links
├──> _analyze_mobile_friendly()    → Mobile check
├──> _analyze_page_speed_estimate()→ Speed estimate
├──> _analyze_schema_markup()      → Check schema
└──> _calculate_seo_score()        → Final score
```

**Scoring Formula:**
```
Final Score = 
    Title (15%) +
    Meta Description (10%) +
    Headings (15%) +
    Keywords (15%) +
    Images (10%) +
    Links (10%) +
    Mobile (10%) +
    Speed (10%) +
    Schema (5%)
```

#### WebScraperTool
```
scrape_page(url)
→ Extracts: Title, Meta tags, Content, Headings
```

#### KeywordAnalyzerTool
```
analyze_keywords(text)
→ Finds top keywords, frequencies, difficulty levels

get_competitor_keywords()
→ Returns mock competitor data
```

#### CitationGeneratorTool
```
generate_citation(recommendation)
→ Creates cited recommendation

generate_report_with_citations(analysis)
→ Adds citations to entire report
```

### 5. Memory (`memory/hindsight_memory.py`)

**Purpose:** Store and recall agent learnings

**Storage Structure:**
```
data/memory/
├── analysis_history.json    → All analyses per website
├── suggestions.json         → All suggestions made
├── keywords.json            → Keyword performance over time
└── improvements.json        → What worked/didn't work
```

**Key Methods:**
```
store_analysis()                             → Save analysis
get_analysis_history()                       → Retrieve history
store_suggestion()                           → Save recommendation
get_suggestions()                            → Retrieve suggestions
store_keyword_performance()                  → Track keywords
get_keyword_performance()                    → Retrieve keyword data
calculate_improvement()                      → Calculate progress
get_learning_insights()                      → Generate insights
_generate_recommendations()                  → Suggest actions
store_improvement_metric()                   → Track effectiveness
```

**Data Example:**
```json
{
  "https://example.com": [
    {
      "timestamp": "2024-01-15T10:00:00",
      "seo_score": 45,
      "issues": ["Missing meta description", "No H1 tag"],
      "title": "Example"
    },
    {
      "timestamp": "2024-01-20T10:00:00",
      "seo_score": 62,
      "issues": ["Poor heading structure"],
      "title": "Example | Home"
    }
  ]
}
```

## 🤖 Agentic Decision Making

### Step-by-Step Reasoning

```
1. PERCEIVE
   └─ Receive website URL and analysis request

2. ANALYZE
   ├─ Extract website content
   ├─ Identify SEO issues
   └─ Generate initial recommendations

3. RECALL
   ├─ Query memory for past analyses
   ├─ Check keyword performance history
   └─ Identify patterns and improvements

4. REASON
   ├─ Send analysis to LLM:
   │  "Here's the current state, here's the history, what should we focus on?"
   ├─ LLM considers:
   │  • Current issues (from analysis)
   │  • Past attempts (from memory)
   │  • What worked before (from memory)
   │  • Industry best practices
   └─ LLM generates prioritized recommendations

5. DECIDE
   ├─ Combine:
   │  • Rule-based recommendations (from analysis)
   │  • LLM-generated recommendations (from reasoning)
   │  • Learning-based recommendations (from memory)
   └─ Prioritize actions

6. ACT
   ├─ Generate citations for each recommendation
   ├─ Simulate potential improvements if requested
   └─ Prepare comprehensive report

7. STORE
   ├─ Save analysis in memory
   ├─ Record effectiveness metrics
   ├─ Update keyword performance
   └─ Generate new learning insights

8. REPORT
   └─ Send results to frontend with all details
```

## 🧠 Memory Learning Mechanism

### How the Agent Learns

```
Analysis #1 (Day 1)
├─ Score: 45
├─ Issues Found: [8 issues]
└─ Recommendations: [5 recommendations]
    ↓
    Memory stores everything
    ↓
Implementation (hypothetical)
├─ User implements recommendations
└─ Website improves
    ↓
Analysis #2 (Day 5)
├─ Score: 62 (+17 points)
├─ Issues Found: [5 issues] (-3)
└─ New Recommendations: [Improved based on learning]
    ↓
Memory analyzes patterns
├─ Which issues were fixed? (Those recommendations worked!)
├─ Which issues remain? (Focus here next time)
├─ What new issues appeared? (New challenge)
└─ Generate learning insights
    ↓
Analysis #3 (Day 10)
├─ Agent uses learning insights
├─ Prioritizes based on what worked before
├─ Suggests similar actions that helped
└─ Score: 75 (+30 from start)
    ↓
Over time: Agent gets smarter with each iteration!
```

## 🔄 Request-Response Flow

### Example: Analyze Website

```
FRONTEND
│
├─ User types URL: https://example.com
├─ User clicks "Analyze"
├─ JavaScript validates URL
└─ POST to /api/analyze with JSON:
   {
     "website_url": "https://example.com",
     "simulate_improvement": true,
     "improvement_days": 5
   }
   │
   └─────────────────────────────┐
                                 │
                          BACKEND
                                 │
   ┌─────────────────────────────┘
   │
   ├─ Receive request
   ├─ Validate input
   ├─ Call: seo_agent.analyze_website(url)
   │
   └─ SEO Agent process:
      ├─ 1. Fetch website
      ├─ 2. Extract SEO metrics
      ├─ 3. Query memory for history
      ├─ 4. Use LLM to reason
      ├─ 5. Generate recommendations
      ├─ 6. Store in memory
      └─ 7. Compile report
         │
         └─ JSON Response:
            {
              "success": true,
              "seo_score": 65.4,
              "issues_found": [...],
              "recommendations": [...],
              "improvement_metrics": {...},
              "simulated_improvements": {...}
            }
   │
   └─────────────────────────────┐
                                 │
      ┌──────────────────────────┘
      │
  FRONTEND
      │
      ├─ Receive response
      ├─ Parse JSON
      ├─ Update score circle (color-coded)
      ├─ Populate tabs:
      │  ├─ Overview (metrics)
      │  ├─ Issues
      │  ├─ Recommendations
      │  ├─ Memory Status
      │  └─ Improvements
      └─ Display to user
```

## 🔐 LLM Integration

### Groq API Usage

```
Agent gathers context:
├─ Current website analysis
├─ Past analyses from memory
├─ Most common issues
└─ Previous effective recommendations

Agent creates prompt:
│
└─ "You are an SEO expert. Here's the current state:
    [website metrics]
    
    Here's the history:
    [past analyses]
    
    Here's what worked before:
    [effective recommendations]
    
    What are the top 3-5 recommendations?"

Send to Groq LLM
│
└─ LLM generates:
   ├─ Prioritized recommendations
   ├─ Reasoning for each
   ├─ Expected impact
   └─ Estimated difficulty

Agent processes response:
├─ Parse JSON (if structured)
├─ Add citations
├─ Combine with other recommendations
└─ Return to user
```

## 📊 Performance Considerations

### Optimization

1. **Caching**
   - Memory reduces re-analysis need
   - Patterns cached in insights

2. **Async Operations**
   - Frontend stays responsive
   - Spinner shows activity

3. **Lazy Loading**
   - Memory loaded on demand
   - Large histories handled efficiently

4. **Batch Processing**
   - `/api/batch-analyze` for multiple URLs
   - Processes up to 10 at a time

## 🔧 Configuration Points

### Settings (`config/settings.py`)

```python
# LLM Configuration
PRIMARY_LLM = "groq"                    # "groq" or "openai"
GROQ_MODEL = "mixtral-8x7b-32768"      # Groq model choice

# Scoring Thresholds
MIN_TITLE_LENGTH = 30
MAX_TITLE_LENGTH = 60
MIN_META_DESCRIPTION_LENGTH = 120
MAX_META_DESCRIPTION_LENGTH = 160

# Memory
MEMORY_DIR = "./data/memory"            # Where to store data

# Backend
BACKEND_PORT = 8000                    # API port
```

## 🚀 Scalability

### Current Design Handles

- ✅ Single websites
- ✅ Batch analysis (up to 10)
- ✅ Large memory (JSON-based, append-only)
- ✅ Multiple concurrent users

### Future Scaling

- Database instead of JSON
- Redis for caching
- Task queue (Celery) for async jobs
- Distributed memory
- Load balancing

## 🎯 Design Philosophy

### Core Principles

1. **Agentic**: Makes decisions, not just reports
2. **Memorable**: Learns from all interactions
3. **Reasoned**: Uses LLM for smart recommendations
4. **Cited**: All recommendations backed by evidence
5. **Transparent**: Shows its reasoning and memory
6. **Efficient**: Doesn't re-analyze needlessly
7. **Extensible**: Easy to add new tools/metrics

---

This architecture enables true AI agentic behavior: thinking, deciding, learning, and improving over time.
