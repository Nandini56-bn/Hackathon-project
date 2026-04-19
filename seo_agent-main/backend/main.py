"""
FastAPI Backend for SEO Agent
Provides REST API endpoints for the frontend
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.seo_agent import SEOAgent
from config.settings import (
    GROQ_API_KEY, 
    OPENAI_API_KEY,
    ALLOWED_ORIGINS,
    BACKEND_HOST,
    BACKEND_PORT
)

# Initialize FastAPI app
app = FastAPI(
    title="SEO & Citation Agent API",
    description="Agentic AI system for SEO analysis with memory and learning",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SEO Agent with both API keys
seo_agent = SEOAgent(groq_api_key=GROQ_API_KEY, openai_api_key=OPENAI_API_KEY)


# ============= Request/Response Models =============

class AnalysisRequest(BaseModel):
    """Request model for website analysis"""
    website_url: str
    simulate_improvement: bool = False
    improvement_days: int = 5


class AnalysisResponse(BaseModel):
    """Response model for analysis"""
    success: bool
    timestamp: str
    website_url: str
    seo_score: float
    issues_found: List[str]
    recommendations: List[Dict[str, Any]]
    improvement_metrics: Optional[Dict[str, Any]] = None


class MemoryStatusResponse(BaseModel):
    """Response model for memory status"""
    website_url: str
    analyses_performed: int
    suggestions_made: int
    improvement_metrics: Dict[str, Any]


# ============= API Endpoints =============

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "service": "SEO & Citation Agent API",
        "version": "1.0.0",
        "description": "Agentic AI system for SEO analysis with memory and learning",
        "endpoints": {
            "analyze": "/api/analyze",
            "memory_status": "/api/memory/{website_url}",
            "simulate_improvement": "/api/simulate-improvement",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SEO Agent API",
        "groq_available": seo_agent.client is not None
    }


@app.post("/api/analyze")
async def analyze_website(request: AnalysisRequest):
    """
    Analyze a website for SEO issues and get recommendations
    
    The agent will:
    1. Fetch and analyze the website
    2. Extract SEO metrics
    3. Check memory for past analyses
    4. Use LLM to generate intelligent recommendations
    5. Store results in memory for future learning
    6. Return comprehensive report with citations
    
    Args:
        website_url: The website to analyze
        simulate_improvement: Whether to simulate ranking improvements
        improvement_days: Number of days to simulate
    
    Returns:
        Comprehensive SEO analysis report with recommendations
    """
    
    if not request.website_url:
        raise HTTPException(status_code=400, detail="website_url is required")
    
    try:
        # Run analysis
        result = seo_agent.analyze_website(request.website_url)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        # Optionally simulate improvement
        if request.simulate_improvement:
            improvement = seo_agent.simulate_ranking_improvement(
                request.website_url,
                request.improvement_days
            )
            result["simulated_improvements"] = improvement
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/memory/{website_url}")
async def get_memory_status(website_url: str):
    """
    Get memory status for a website
    Shows what the agent has learned and past analyses
    
    Args:
        website_url: The website to get memory for
    
    Returns:
        Memory status including improvement metrics and learning insights
    """
    
    try:
        status = seo_agent.get_agent_memory_status(website_url)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve memory: {str(e)}")


@app.post("/api/simulate-improvement")
async def simulate_improvement(website_url: str, days: int = 5):
    """
    Simulate ranking improvements over time (for demo purposes)
    Shows how the agent learns and adapts
    
    Args:
        website_url: The website to simulate improvements for
        days: Number of days to simulate
    
    Returns:
        Simulated improvement data
    """
    
    if not website_url:
        raise HTTPException(status_code=400, detail="website_url is required")
    
    try:
        improvements = seo_agent.simulate_ranking_improvement(website_url, days)
        return improvements
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")


@app.post("/api/batch-analyze")
async def batch_analyze(websites: List[str]):
    """
    Analyze multiple websites in batch
    
    Args:
        websites: List of website URLs to analyze
    
    Returns:
        List of analysis results
    """
    
    if not websites:
        raise HTTPException(status_code=400, detail="websites list is required")
    
    results = []
    
    for url in websites[:10]:  # Limit to 10 per request
        try:
            result = seo_agent.analyze_website(url)
            results.append(result)
        except Exception as e:
            results.append({
                "success": False,
                "website_url": url,
                "error": str(e)
            })
    
    return {
        "total_websites": len(websites),
        "analyzed": len(results),
        "results": results
    }


@app.get("/api/memory-stats")
async def get_memory_stats():
    """
    Get overall memory statistics
    Shows how many websites the agent has analyzed
    """
    
    try:
        # Read memory files to get stats
        memory_dir = Path("./data/memory")
        
        analysis_file = memory_dir / "analysis_history.json"
        import json
        
        if analysis_file.exists():
            data = json.loads(analysis_file.read_text())
            websites_analyzed = len(data)
            total_analyses = sum(len(analyses) for analyses in data.values())
        else:
            websites_analyzed = 0
            total_analyses = 0
        
        return {
            "websites_analyzed": websites_analyzed,
            "total_analyses": total_analyses,
            "memory_system": "Hindsight Memory",
            "features": [
                "Stores analysis history",
                "Tracks keyword performance",
                "Calculates improvements",
                "Generates learning insights",
                "Powers LLM reasoning"
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "websites_analyzed": 0,
            "total_analyses": 0
        }


@app.delete("/api/memory/{website_url}")
async def clear_memory(website_url: str):
    """
    Clear memory for a specific website
    
    Args:
        website_url: The website to clear memory for
    
    Returns:
        Confirmation message
    """
    
    try:
        seo_agent.memory.reset_memory(website_url)
        return {
            "success": True,
            "message": f"Memory cleared for {website_url}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not clear memory: {str(e)}")


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting SEO Agent API Server...")
    print(f"📍 Server: http://{BACKEND_HOST}:{BACKEND_PORT}")
    print(f"🔗 API Docs: http://{BACKEND_HOST}:{BACKEND_PORT}/docs")
    print(f"📊 Groq LLM: {'✅ Available' if seo_agent.client else '⚠️ Not configured'}")
    print("=" * 60)
    
    uvicorn.run(app, host=BACKEND_HOST, port=BACKEND_PORT)
