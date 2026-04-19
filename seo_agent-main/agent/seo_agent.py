"""
SEO Agent with LLM Integration and Memory
Agentic system that reasons about SEO problems and provides recommendations
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.seo_tools import (
    SEOAnalyzerTool, 
    WebScraperTool, 
    KeywordAnalyzerTool, 
    CitationGeneratorTool
)
from memory.hindsight_memory import HindsightMemory
from config.settings import PRIMARY_LLM, OPENAI_API_KEY, GROQ_API_KEY, OPENAI_MODEL, GROQ_MODEL

try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class SEOAgent:
    """
    Agentic AI system for SEO analysis and recommendations
    Uses LLM (Groq or OpenAI) for reasoning and memory for learning
    Automatically switches between LLM providers if one fails
    """
    
    def __init__(self, groq_api_key: str = "", openai_api_key: str = "", memory_dir: str = "./data/memory"):
        """
        Initialize SEO Agent with automatic LLM provider fallback
        
        Args:
            groq_api_key: API key for Groq LLM
            openai_api_key: API key for OpenAI LLM
            memory_dir: Directory for storing memory data
        """
        self.groq_api_key = groq_api_key or GROQ_API_KEY
        self.openai_api_key = openai_api_key or OPENAI_API_KEY
        self.primary_llm = PRIMARY_LLM.lower()
        self.memory = HindsightMemory(memory_dir)
        self.seo_analyzer = SEOAnalyzerTool()
        self.web_scraper = WebScraperTool()
        self.keyword_analyzer = KeywordAnalyzerTool()
        self.citation_generator = CitationGeneratorTool()
        
        # Initialize LLM client with automatic fallback
        self.client = None
        self.model = None
        self.llm_provider = None
        self.available_providers = []  # Track which providers are available
        
        print("\n🔧 Initializing LLM Providers...")
        print("=" * 60)
        
        # Try to initialize both providers
        self._try_initialize_openai()
        self._try_initialize_groq()
        
        # Use primary LLM if available, otherwise use any available provider
        if self.primary_llm == "openai" and self.llm_provider != "openai":
            # Primary is OpenAI but it failed, try Groq
            if self.groq_api_key and Groq and "groq" in self.available_providers:
                self.client = self._get_groq_client()
                self.model = GROQ_MODEL
                self.llm_provider = "groq"
        elif self.primary_llm == "groq" and self.llm_provider != "groq":
            # Primary is Groq but it failed, try OpenAI
            if self.openai_api_key and OpenAI and "openai" in self.available_providers:
                self.client = self._get_openai_client()
                self.model = OPENAI_MODEL
                self.llm_provider = "openai"
        
        # Print summary
        if self.llm_provider:
            print(f"\n✅ Active Provider: {self.llm_provider.upper()}")
        else:
            print("\n⚠️  No LLM providers available")
        
        if self.available_providers:
            print(f"📌 Available Fallback Providers: {', '.join([p.upper() for p in self.available_providers])}")
        else:
            print("📌 WARNING: No fallback providers - will use basic recommendations only")
        print("=" * 60 + "\n")
    
    def _try_initialize_openai(self):
        """Try to initialize OpenAI client"""
        if not self.openai_api_key or not OpenAI:
            return False
        
        try:
            client = OpenAI(api_key=self.openai_api_key)
            # Try a simple test to verify the API key works
            # (We'll do this during actual usage for better UX)
            self.available_providers.append("openai")
            if not self.llm_provider:
                self.client = client
                self.model = OPENAI_MODEL
                self.llm_provider = "openai"
            print("✅ OpenAI (GPT-4) - Available")
            return True
        except Exception as e:
            print(f"❌ OpenAI - Not available ({str(e)[:50]}...)")
            return False
    
    def _try_initialize_groq(self):
        """Try to initialize Groq client"""
        if not self.groq_api_key or not Groq:
            return False
        
        try:
            client = Groq(api_key=self.groq_api_key)
            self.available_providers.append("groq")
            if not self.llm_provider:
                self.client = client
                self.model = GROQ_MODEL
                self.llm_provider = "groq"
            print("✅ Groq (Llama) - Available")
            return True
        except Exception as e:
            print(f"❌ Groq - Not available ({str(e)[:50]}...)")
            return False
    
    def _get_openai_client(self):
        """Get fresh OpenAI client"""
        if self.openai_api_key and OpenAI:
            try:
                return OpenAI(api_key=self.openai_api_key)
            except:
                return None
        return None
    
    def _get_groq_client(self):
        """Get fresh Groq client"""
        if self.groq_api_key and Groq:
            try:
                return Groq(api_key=self.groq_api_key)
            except:
                return None
        return None
    
    def analyze_website(self, website_url: str) -> Dict[str, Any]:
        """
        Main agent function: Analyze website and provide recommendations
        
        Steps:
        1. Fetch and analyze website
        2. Extract key metrics
        3. Check memory for past analyses
        4. Use LLM to reason about improvements
        5. Store results in memory
        6. Generate citations
        """
        
        print(f"\n🤖 SEO Agent analyzing: {website_url}")
        print("=" * 60)
        
        # Step 1: Analyze website
        print("[1/5] Analyzing website structure...")
        analysis = self.seo_analyzer.analyze_website(website_url)
        
        if not analysis.get("success"):
            return analysis
        
        # Step 2: Get learning insights from memory
        print("[2/5] Checking past analyses for patterns...")
        learning_insights = self.memory.get_learning_insights(website_url)
        improvement_metrics = learning_insights.get("improvement_metrics", {})
        
        # Step 3: Use LLM to generate intelligent recommendations
        print("[3/5] Using AI to generate recommendations...")
        recommendations_with_reasoning = self._generate_recommendations_with_llm(
            analysis, 
            learning_insights
        )
        
        # Step 4: Store analysis in memory
        print("[4/5] Storing analysis in memory...")
        self.memory.store_analysis(website_url, {
            "seo_score": analysis["seo_score"],
            "issues": analysis["issues"],
            "recommendations": analysis["recommendations"],
            "title": analysis.get("title", ""),
            "meta_description": analysis.get("meta_description", "")
        })
        
        # Step 5: Generate full report with citations
        print("[5/5] Generating cited report...")
        report = self._generate_final_report(
            analysis,
            recommendations_with_reasoning,
            improvement_metrics,
            learning_insights
        )
        
        return report
    
    def _generate_recommendations_with_llm(
        self, 
        analysis: Dict[str, Any], 
        learning_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use LLM to generate intelligent recommendations based on analysis and memory
        Automatically tries other providers if primary fails
        """
        
        if self.client is None and not self.available_providers:
            # No LLM available at all
            return self._generate_basic_recommendations(analysis, learning_insights)
        
        try:
            # Prepare context for LLM
            issues_text = "\n".join(analysis.get("issues", []))
            past_recommendations = learning_insights.get("recommendations_for_improvement", [])
            most_common_issues = learning_insights.get("most_common_issues", {})
            
            prompt = f"""You are an expert SEO consultant helping improve a website's search engine visibility.

Current Website Analysis:
- SEO Score: {analysis['seo_score']}/100
- Issues Found:
{issues_text}

Past Analysis History:
- Total analyses performed: {learning_insights['improvement_metrics'].get('analyses_performed', 1)}
- Improvement so far: {learning_insights['improvement_metrics'].get('improvement_percentage', 0)}%
- Keywords improved: {learning_insights['improvement_metrics'].get('keywords_improved', 0)}

Most Common Issues Across Analyses:
{json.dumps(most_common_issues, indent=2)}

Previous Effective Recommendations:
{json.dumps(past_recommendations[:3], indent=2)}

Based on this analysis and learning history, provide 3-5 specific, actionable SEO recommendations.
For each recommendation:
1. State the issue or opportunity
2. Provide the specific action
3. Explain the expected impact
4. Reference why this matters for SEO

Format your response as a JSON object with a "recommendations" array."""
            
            # Try current provider first
            response_text = None
            if self.llm_provider == "openai":
                try:
                    response_text = self._call_openai(prompt)
                except Exception as e:
                    print(f"⚠️  OpenAI failed: {str(e)[:50]}... Switching to Groq...")
                    self._switch_to_groq()
                    if self.llm_provider == "groq":
                        response_text = self._call_groq(prompt)
            else:  # Groq
                try:
                    response_text = self._call_groq(prompt)
                except Exception as e:
                    print(f"⚠️  Groq failed: {str(e)[:50]}... Switching to OpenAI...")
                    self._switch_to_openai()
                    if self.llm_provider == "openai":
                        response_text = self._call_openai(prompt)
            
            # If still no response, try any available provider
            if not response_text:
                if "openai" in self.available_providers and self.llm_provider != "openai":
                    try:
                        self._switch_to_openai()
                        response_text = self._call_openai(prompt)
                    except:
                        pass
                
                if not response_text and "groq" in self.available_providers and self.llm_provider != "groq":
                    try:
                        self._switch_to_groq()
                        response_text = self._call_groq(prompt)
                    except:
                        pass
            
            # Parse response if we got one
            if response_text:
                try:
                    start_idx = response_text.find('{')
                    end_idx = response_text.rfind('}') + 1
                    if start_idx != -1 and end_idx > start_idx:
                        json_str = response_text[start_idx:end_idx]
                        result = json.loads(json_str)
                        return result
                except:
                    pass
                
                # Return response as text in structured format
                return {
                    "recommendations": [{"text": response_text}],
                    "reasoning": f"Generated by {self.llm_provider.upper()} LLM (auto-switched)"
                }
            
            # Fallback to basic recommendations
            return self._generate_basic_recommendations(analysis, learning_insights)
            
        except Exception as e:
            print(f"❌ LLM Error: {e}")
            return self._generate_basic_recommendations(analysis, learning_insights)
    
    def _switch_to_openai(self):
        """Switch to OpenAI provider"""
        client = self._get_openai_client()
        if client:
            self.client = client
            self.model = OPENAI_MODEL
            self.llm_provider = "openai"
            print("🔄 Switched to OpenAI provider")
            return True
        return False
    
    def _switch_to_groq(self):
        """Switch to Groq provider"""
        client = self._get_groq_client()
        if client:
            self.client = client
            self.model = GROQ_MODEL
            self.llm_provider = "groq"
            print("🔄 Switched to Groq provider")
            return True
        return False
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        message = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.choices[0].message.content
    
    def _call_groq(self, prompt: str) -> str:
        """Call Groq API"""
        message = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.choices[0].message.content
    
    def _generate_basic_recommendations(
        self, 
        analysis: Dict[str, Any], 
        learning_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate basic recommendations if LLM is not available
        """
        recommendations = []
        
        # Based on current analysis
        if analysis.get("seo_score", 0) < 50:
            recommendations.append("Focus on basic SEO fundamentals first")
        
        # Based on learning insights
        if learning_insights.get("improvement_metrics", {}).get("improvement_percentage", 0) > 0:
            recommendations.append("Continue with strategies that have shown improvement previously")
        
        # Add analysis recommendations
        recommendations.extend(analysis.get("recommendations", []))
        
        return {
            "recommendations": [{"text": r} for r in recommendations],
            "reasoning": "Generated from analysis patterns"
        }
    
    def _generate_final_report(
        self,
        analysis: Dict[str, Any],
        llm_recommendations: Dict[str, Any],
        improvement_metrics: Dict[str, Any],
        learning_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate final comprehensive report with citations
        """
        
        # Combine all recommendations
        all_recommendations = []
        
        # Add original analysis recommendations
        for rec in analysis.get("recommendations", []):
            all_recommendations.append({
                "text": rec,
                "source": "Website Analysis",
                "type": "automatic"
            })
        
        # Add LLM-generated recommendations
        for rec in llm_recommendations.get("recommendations", []):
            if isinstance(rec, dict):
                rec_text = rec.get("text", str(rec))
            else:
                rec_text = str(rec)
            
            all_recommendations.append({
                "text": rec_text,
                "source": "AI Reasoning (Groq LLM)",
                "type": "llm_generated"
            })
        
        # Add learning-based recommendations
        for rec in learning_insights.get("recommendations_for_improvement", []):
            all_recommendations.append({
                "text": rec,
                "source": "Historical Learning",
                "type": "learned"
            })
        
        report = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "website_url": analysis["url"],
            "analysis": {
                "seo_score": analysis["seo_score"],
                "title": analysis.get("title", ""),
                "meta_description": analysis.get("meta_description", ""),
                "headings": analysis.get("headings", {}),
                "images_count": analysis.get("images", 0),
                "links": analysis.get("links", {})
            },
            "issues_found": analysis.get("issues", []),
            "recommendations": all_recommendations[:10],  # Top 10 recommendations
            "score_breakdown": analysis.get("score_factors", {}),
            "improvement_metrics": improvement_metrics,
            "learning_insights": {
                "total_suggestions": learning_insights.get("total_suggestions", 0),
                "effective_suggestions": learning_insights.get("effective_suggestions", 0),
                "analyses_performed": improvement_metrics.get("analyses_performed", 1)
            }
        }
        
        return report
    
    def simulate_ranking_improvement(self, website_url: str, days: int = 5) -> Dict[str, Any]:
        """
        Simulate ranking improvements over time (for demo purposes)
        Stores keyword performance to show agent is learning
        """
        keywords = [
            {"keyword": "seo", "current_rank": 45},
            {"keyword": "optimization", "current_rank": 32},
            {"keyword": "keywords", "current_rank": 28},
            {"keyword": "content", "current_rank": 60},
            {"keyword": "ranking", "current_rank": 51}
        ]
        
        improvements = {}
        
        for keyword_data in keywords:
            keyword = keyword_data["keyword"]
            current_rank = keyword_data["current_rank"]
            
            # Simulate improvement - each day, rank improves by random amount
            improved_rank = max(1, current_rank - (5 + (days // 2)))
            improvement = current_rank - improved_rank
            
            # Store in memory
            self.memory.store_keyword_performance(
                website_url,
                keyword,
                improved_rank,
                10000 + (len(keyword) * 1000)
            )
            
            improvements[keyword] = {
                "initial_rank": current_rank,
                "current_rank": improved_rank,
                "improvement": improvement,
                "days_to_improve": days
            }
        
        return {
            "website_url": website_url,
            "days_simulated": days,
            "keywords_improved": improvements
        }
    
    def get_agent_memory_status(self, website_url: str) -> Dict[str, Any]:
        """
        Get status of agent's memory for a website
        Shows what the agent has learned
        """
        history = self.memory.get_analysis_history(website_url)
        suggestions = self.memory.get_suggestions(website_url)
        improvements = self.memory.calculate_improvement(website_url)
        insights = self.memory.get_learning_insights(website_url)
        
        return {
            "website_url": website_url,
            "analyses_performed": len(history),
            "suggestions_made": len(suggestions),
            "improvement_metrics": improvements,
            "learning_insights": insights,
            "last_analysis": history[-1] if history else None
        }
