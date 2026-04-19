# ⚡ QUICK START GUIDE (5 Minutes to Running)

## 📋 Pre-Requirements

- Windows, Mac, or Linux
- Python 3.9+ installed
- At least one API key:
  - **Groq** (free): https://console.groq.com
  - **OpenAI** (paid): https://openai.com

## 🎯 NEW: Automatic LLM Provider Switching

✨ **The agent automatically switches between LLM providers if one fails!**

- Primary provider (set in `.env`): OpenAI (GPT-4) or Groq (Llama)
- Fallback provider: Automatically used if primary fails
- **No manual intervention needed** - the system handles it automatically!

📖 See [LLM_SWITCHING_GUIDE.md](LLM_SWITCHING_GUIDE.md) for detailed info

---

## ⚡ EASIEST WAY: Run Everything with One Command

### Windows:
```bash
# Double-click: run_all.bat
# OR in terminal:
run_all.bat
```

### Mac/Linux:
```bash
python run_all.py
```

This will start **BOTH backend and frontend automatically!** Then just:
1. Open browser to: **http://localhost:8080**
2. Start analyzing websites!

---

## 🚀 Step 1: Setup (2 minutes)

### Windows:
```bash
# Double-click: setup.bat
# OR run in terminal:
cd "c:\Users\Lenovo\OneDrive\Desktop\seo agent"
setup.bat
```

This will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create necessary directories
- ✅ Create .env file

### Mac/Linux:
```bash
cd ~/Desktop/seo\ agent
python3 -m venv venv
source venv/bin/activate  # Or: . venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
mkdir -p data/memory
```

## 🔑 Step 2: Add API Key (1 minute)

You need **at least one** API key (both is recommended for redundancy):

### Option A: Groq (FREE)
1. Get Groq API key:
   - Go to https://console.groq.com
   - Sign up (free)
   - Create API key

2. Open `.env` file and add:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Option B: OpenAI (PAID - for better AI quality)
1. Get OpenAI API key:
   - Go to https://openai.com
   - Create account and add payment
   - Create API key

2. Open `.env` file and add:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PRIMARY_LLM=openai
   ```

### Option C: BOTH (RECOMMENDED for reliability)
```
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
PRIMARY_LLM=openai        # OpenAI is primary
```
System will auto-switch to Groq if OpenAI fails!

3. Save file

## 🖥️ Step 3: Start Backend (30 seconds)

### Windows:
```bash
# Double-click: run_backend.bat
# OR in terminal:
run_backend.bat
```

### Mac/Linux:
```bash
source venv/bin/activate
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

**Keep this terminal open!**

## 🌐 Step 4: Open Frontend (30 seconds)

**Option A: Direct (Easiest)**
```
Just open: frontend/index.html in your browser
```

**Option B: Via Terminal**
```bash
# Open new terminal in the seo agent folder
run_frontend.bat

# Then go to: http://localhost:8001
```

## ✨ Step 5: Start Analyzing!

1. **Enter a website URL:**
   ```
   https://www.example.com
   ```

2. **Click "Analyze"**

3. **Wait for results** (30 seconds)

4. **View:**
   - SEO Score (0-100)
   - Issues Found
   - Recommendations
   - Improvement Metrics

## 🧪 Quick Test

```bash
# In a new terminal, run:
python test_agent.py

# This demonstrates:
# ✅ Website analysis
# ✅ Memory storage
# ✅ Learning over time
# ✅ Ranking improvements
# ✅ LLM reasoning
```

## 📊 Try These Features

1. **Analyze Same Site Twice:**
   - See how agent remembers first analysis
   - Check memory shows 2 analyses

2. **Enable Simulated Improvements:**
   - Check box: "Simulate ranking improvements"
   - See simulated 5-day keyword rankings

3. **Check Memory Status:**
   - Click "Memory" button
   - See how agent learns over time

4. **View Different Tabs:**
   - Overview: Score breakdown
   - Issues: Current problems
   - Recommendations: AI suggestions with sources
   - Memory: Agent's learning status
   - Improvements: Progress tracking

## 🔗 Important URLs

- **Frontend:** http://localhost:8001 or open `frontend/index.html`
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **API Health:** http://localhost:8000/health

## 🆘 Troubleshooting

### "Connection refused" error
→ Backend not running. Start backend first (Step 3)

### API key error
→ Check `.env` file has `GROQ_API_KEY=...`

### "Page not found"
→ Make sure you're using correct URL (backend:8000, frontend:8001)

### Port already in use
→ Change port in `config/settings.py` BACKEND_PORT

## 📈 What Happens Behind the Scenes

```
Step 1: You enter website URL
   ↓
Step 2: Backend receives request
   ↓
Step 3: Agent analyzes website (SEO metrics)
   ↓
Step 4: Agent checks memory (past analyses)
   ↓
Step 5: Agent uses Groq LLM (AI reasoning)
   ↓
Step 6: Agent generates recommendations (with citations)
   ↓
Step 7: Agent stores everything in memory
   ↓
Step 8: Frontend displays results
```

## 🎯 Next Steps

After getting it running:

1. **Analyze multiple websites** - See how agent handles different sites
2. **Check memory** - Analyze same site again to see learning
3. **Review recommendations** - Actually implement some!
4. **Simulate improvements** - See how agent would improve results
5. **Read full README.md** - Understand all features

## 🎓 Understanding the Agent

### The 3 Key Components

1. **Analysis Tools**
   - Analyzes website SEO factors
   - Generates initial recommendations
   - Detects issues

2. **Memory System (Hindsight)**
   - Remembers all past analyses
   - Tracks keyword performance
   - Calculates improvements
   - Generates insights

3. **LLM (Groq AI)**
   - Reasons about recommendations
   - Prioritizes actions
   - Generates explanations
   - Improves over time

### Why It's Agentic

✅ **Thinks:** Uses AI to reason about what to do  
✅ **Decides:** Chooses which tools to use  
✅ **Acts:** Executes tools systematically  
✅ **Remembers:** Stores everything in memory  
✅ **Learns:** Improves recommendations based on memory  

## 📞 Support

- Check error messages in browser console (F12)
- Check backend terminal for server errors
- Verify API key in `.env`
- Make sure ports 8000 and 8001 are available

## 🎉 You're All Set!

```
Your SEO Agent is now running and learning!

As you use it more:
→ It remembers past analyses
→ It identifies patterns
→ It improves recommendations
→ It tracks your progress

The agent gets smarter with every analysis! 🚀
```

---

**Questions?** Check `README.md` for full documentation.
