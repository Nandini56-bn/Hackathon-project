"""
Test script to demonstrate automatic LLM provider switching
Shows how the agent handles provider failures gracefully
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.seo_agent import SEOAgent

def test_automatic_switching():
    """Test automatic LLM provider switching"""
    
    print("\n" + "=" * 70)
    print("🧪 AUTOMATIC LLM PROVIDER SWITCHING TEST")
    print("=" * 70)
    
    # Initialize agent - will show which providers are available
    print("\n📍 Initializing SEO Agent...")
    agent = SEOAgent()
    
    print("\n" + "=" * 70)
    print("📊 PROVIDER STATUS:")
    print("=" * 70)
    print(f"🔵 Primary LLM: {agent.primary_llm.upper()}")
    print(f"🟢 Current Provider: {agent.llm_provider.upper() if agent.llm_provider else 'NONE'}")
    print(f"📌 Available Providers: {', '.join([p.upper() for p in agent.available_providers]) if agent.available_providers else 'NONE'}")
    
    # Test analysis with a simple website
    print("\n" + "=" * 70)
    print("🌐 TESTING ANALYSIS WITH PROVIDER SWITCHING:")
    print("=" * 70)
    
    test_urls = [
        "https://www.google.com",
        "https://www.github.com",
    ]
    
    for url in test_urls:
        print(f"\n📍 Analyzing: {url}")
        try:
            result = agent.analyze_website(url)
            
            if result.get("success"):
                print(f"✅ Analysis successful!")
                print(f"   📊 SEO Score: {result.get('seo_score', 'N/A')}/100")
                print(f"   🔍 Issues Found: {len(result.get('issues', []))}")
                print(f"   💡 Recommendations: {len(result.get('recommendations', []))}")
                
                # Show which provider was used
                recs = result.get('recommendations', [])
                if recs and isinstance(recs[0], dict) and 'source' in recs[0]:
                    print(f"   🤖 Provider Used: {recs[0].get('source', 'Unknown')}")
            else:
                print(f"❌ Analysis failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error during analysis: {str(e)[:100]}")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
    print("\n💡 Notes:")
    print("   • If one provider fails, check the switching messages above")
    print("   • The system will automatically try the fallback provider")
    print("   • See LLM_SWITCHING_GUIDE.md for configuration options")
    print("\n")

if __name__ == "__main__":
    test_automatic_switching()
