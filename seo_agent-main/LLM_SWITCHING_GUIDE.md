# 🔄 Automatic LLM Provider Switching Guide

## Overview

The SEO Agent now has **intelligent automatic switching** between LLM providers. If one provider fails or is unavailable, the system seamlessly switches to another without any user intervention.

---

## 🎯 How It Works

### Initialization Phase (Startup)
When the application starts:

1. **Detects Available Providers**
   - Checks if OpenAI API key is provided → tries to initialize
   - Checks if Groq API key is provided → tries to initialize
   - Displays which providers are available

2. **Sets Primary Provider**
   - Uses the provider specified in `PRIMARY_LLM` setting (`.env`)
   - If primary provider fails, uses the available fallback

3. **Displays Status**
   ```
   ✅ OpenAI (GPT-4) - Available
   ✅ Groq (Llama) - Available
   📌 Active Provider: OpenAI
   📌 Available Fallback Providers: openai, groq
   ```

### Runtime Phase (During Analysis)
When analyzing websites:

1. **Tries Primary Provider**
   - Sends request to OpenAI (or Groq, depending on settings)

2. **Auto-Switches on Failure**
   - If it fails (API error, rate limit, network issue):
   ```
   ⚠️ OpenAI failed: Rate limit exceeded... Switching to Groq...
   🔄 Switched to Groq provider
   ```
   - Automatically retries with the fallback provider

3. **Graceful Degradation**
   - If both providers fail → uses basic recommendations
   - No errors shown to user, analysis completes successfully

---

## 📋 Configuration

### `.env` File

```env
# Primary LLM to use first
PRIMARY_LLM=openai

# API Keys (leave empty to disable)
OPENAI_API_KEY=sk-proj-your-api-key-here
GROQ_API_KEY=gsk-your-api-key-here
```

### Scenarios

#### ✅ Both Providers Available
- Primary provider (OpenAI) is used
- Groq available as fallback
- **Status**: Fully redundant, most reliable

#### ✅ Only Primary Available
- Uses OpenAI only
- No fallback available
- **Status**: Works but no redundancy

#### ✅ Only Fallback Available
- Primary unavailable, automatically uses Groq
- **Status**: Works but depends on one provider

#### ⚠️ Neither Provider Available
- Uses basic recommendations (no AI)
- **Status**: Limited functionality

---

## 🚀 Switching Providers Manually

### Option 1: Edit `.env`
Change `PRIMARY_LLM` and restart:
```env
PRIMARY_LLM=groq  # Switch to Groq
```

### Option 2: Restart Application
```bash
python run_all.py
```

---

## 💰 Cost Comparison

| Provider | Cost | Speed | Quality |
|----------|------|-------|---------|
| **Groq** | Free | Fast | Good |
| **OpenAI (GPT-4)** | Paid (~$0.03-0.06/analysis) | Normal | Excellent |

### When to Use Each:
- **Groq**: Budget-conscious, high-volume analyses
- **OpenAI**: Premium quality, important decisions

---

## 🔧 Technical Details

### Available Providers Check
```python
# Startup
available_providers = ["openai", "groq"]

# During analysis
if provider_fails:
    switch_to_other_provider()
```

### Automatic Fallback Chain
```
OpenAI (Primary)
    ↓ (if fails)
Groq (Fallback)
    ↓ (if fails)
Basic Recommendations (No AI)
```

### Error Handling
- **API Errors**: Automatically switches provider
- **Network Errors**: Retries with fallback
- **Rate Limits**: Switches to other provider
- **Invalid Keys**: Marks provider as unavailable
- **All Fail**: Gracefully uses basic recommendations

---

## 📊 Monitoring

### Startup Output
Shows which providers are initialized:
```
🔧 Initializing LLM Providers...
============================================================
✅ OpenAI (GPT-4) - Available
✅ Groq (Llama) - Available

✅ Active Provider: OPENAI
📌 Available Fallback Providers: openai, groq
============================================================
```

### During Analysis
If switching occurs:
```
⚠️ OpenAI failed: Connection timeout... Switching to Groq...
🔄 Switched to Groq provider
```

---

## ✨ Benefits

✅ **Reliability**: Never down if you have multiple providers  
✅ **Cost-Effective**: Use free provider as primary  
✅ **User-Friendly**: Automatic, no manual intervention  
✅ **Transparent**: Clear messages when switching  
✅ **Degradation**: Falls back to basic recommendations if all fail  

---

## 🐛 Troubleshooting

### Both Providers Show as "Not Available"
**Problem**: No API keys provided
**Solution**: Add at least one API key to `.env`

### Only One Provider Available
**Problem**: Missing API key for the other provider
**Solution**: Add API key to `.env` for redundancy

### Frequent Switching
**Problem**: Primary provider having issues
**Solution**: 
1. Check API status
2. Verify API key validity
3. Change `PRIMARY_LLM` to the more reliable provider

### Slow Analysis
**Problem**: Maybe using slower provider
**Solution**: Check which provider is active in startup messages

---

## 📞 Quick Reference

| Command | Purpose |
|---------|---------|
| `python run_all.py` | Start with automatic LLM selection |
| Edit `.env` → `PRIMARY_LLM=groq` | Force use Groq |
| Edit `.env` → `PRIMARY_LLM=openai` | Force use OpenAI |
| Check startup messages | See which providers are active |

---

**Version**: 2.0 with Automatic Provider Switching  
**Last Updated**: April 18, 2026
