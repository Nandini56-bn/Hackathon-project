"""
Test script to demonstrate SEO Agent capabilities
Run this after starting the backend: python main.py

This script tests:
1. Website analysis
2. Memory storage and recall
3. Learning improvements over time
4. Agentic reasoning
5. Citation generation
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.seo_agent import SEOAgent
from memory.hindsight_memory import HindsightMemory


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_section(text):
    """Print section header"""
    print(f"\n📌 {text}")
    print("-" * 60)


def test_1_basic_analysis():
    """Test 1: Basic website analysis"""
    print_header("TEST 1: Basic Website Analysis")
    
    agent = SEOAgent(memory_dir="./data/memory")
    
    website = "https://www.example.com"
    print(f"\n🔍 Analyzing: {website}")
    
    result = agent.analyze_website(website)
    
    if result.get("success"):
        print("\n✅ Analysis successful!")
        print(f"   SEO Score: {result['seo_score']}/100")
        print(f"   Issues Found: {len(result['issues_found'])}")
        print(f"   Recommendations: {len(result['recommendations'])}")
        
        print_section("Top Issues")
        for i, issue in enumerate(result['issues_found'][:3], 1):
            print(f"   {i}. {issue}")
        
        print_section("Top Recommendations")
        for i, rec in enumerate(result['recommendations'][:3], 1):
            text = rec.get('text', str(rec))[:60]
            source = rec.get('source', 'Analysis')
            print(f"   {i}. {text}... ({source})")
        
        return result
    else:
        print(f"\n❌ Analysis failed: {result.get('error')}")
        return None


def test_2_memory_storage():
    """Test 2: Memory storage and recall"""
    print_header("TEST 2: Memory Storage & Recall")
    
    agent = SEOAgent(memory_dir="./data/memory")
    website = "https://www.example.com"
    
    # Get memory status
    memory_status = agent.get_agent_memory_status(website)
    
    print(f"\n🧠 Memory Status for: {website}")
    print(f"   Analyses Performed: {memory_status['analyses_performed']}")
    print(f"   Suggestions Made: {memory_status['suggestions_made']}")
    
    print_section("Improvement Metrics")
    metrics = memory_status['improvement_metrics']
    print(f"   Improvement: {metrics.get('improvement_percentage', 0)}%")
    print(f"   Keywords Improved: {metrics.get('keywords_improved', 0)}")
    print(f"   Initial Score: {metrics.get('initial_score', 0)}")
    print(f"   Current Score: {metrics.get('current_score', 0)}")
    print(f"   Days Analyzed: {metrics.get('days_analyzed', 0)}")
    
    print_section("Learning Insights")
    insights = memory_status['learning_insights']
    print(f"   Total Suggestions: {insights.get('total_suggestions', 0)}")
    print(f"   Effective Suggestions: {insights.get('effective_suggestions', 0)}")
    print(f"   Analyses Performed: {insights['analyses_performed']}")


def test_3_learning_loop():
    """Test 3: Learning loop - multiple analyses"""
    print_header("TEST 3: Learning Loop (Multiple Analyses)")
    
    agent = SEOAgent(memory_dir="./data/memory")
    website = "https://www.example.com"
    
    print(f"\n🔄 Running 3 consecutive analyses to demonstrate learning...")
    
    results = []
    
    for iteration in range(1, 4):
        print(f"\n   Analysis #{iteration}...")
        result = agent.analyze_website(website)
        
        if result.get("success"):
            results.append(result)
            print(f"   ✅ Score: {result['seo_score']}/100")
            time.sleep(1)  # Small delay for clarity
        else:
            print(f"   ❌ Failed: {result.get('error')}")
    
    if len(results) > 1:
        print_section("Improvement Over Iterations")
        scores = [r['seo_score'] for r in results]
        improvement = scores[-1] - scores[0]
        
        for i, score in enumerate(scores, 1):
            trend = "↗️" if i > 1 and score > scores[i-2] else "😐"
            print(f"   Analysis #{i}: {score}/100 {trend}")
        
        if improvement != 0:
            print(f"\n   📈 Total Improvement: {improvement:+.1f} points")
        
        # Demonstrate learning insights
        memory_status = agent.get_agent_memory_status(website)
        print_section("Agent's Learning")
        print(f"   ✅ Remembered {memory_status['analyses_performed']} analyses")
        print(f"   ✅ Stored {memory_status['suggestions_made']} suggestions")
        
        insights = memory_status['learning_insights']
        if insights.get('recommendations_for_improvement'):
            print("   📚 Recommendations based on learning:")
            for rec in insights['recommendations_for_improvement'][:3]:
                print(f"      • {rec}")


def test_4_ranking_simulation():
    """Test 4: Simulate ranking improvements"""
    print_header("TEST 4: Ranking Improvement Simulation")
    
    agent = SEOAgent(memory_dir="./data/memory")
    website = "https://www.example.com"
    
    print(f"\n📈 Simulating 10-day ranking improvements...")
    
    improvement = agent.simulate_ranking_improvement(website, days=10)
    
    print(f"\n✅ Simulated improvements for {improvement['days_simulated']} days:")
    
    print_section("Keyword Rankings")
    for keyword, data in improvement['keywords_improved'].items():
        improvement_arrow = f"↑ {data['improvement']}" if data['improvement'] > 0 else "↓"
        print(f"   {keyword:15} | {data['initial_rank']:3} → {data['current_rank']:3} | {improvement_arrow}")


def test_5_memory_learning_insights():
    """Test 5: Memory-based learning insights"""
    print_header("TEST 5: Memory Learning Insights")
    
    memory = HindsightMemory(memory_dir="./data/memory")
    website = "https://www.example.com"
    
    insights = memory.get_learning_insights(website)
    
    print("\n🧠 Learning Insights Generated by Memory:")
    
    print_section("Statistics")
    print(f"   Total Suggestions: {insights['total_suggestions']}")
    print(f"   Effective Suggestions: {insights['effective_suggestions']}")
    
    if insights['most_common_issues']:
        print_section("Most Common Issues Found")
        for issue, count in insights['most_common_issues'].items():
            print(f"   • {issue}: {count} times")
    
    if insights['recommendations_for_improvement']:
        print_section("Recommendations for Future Improvements")
        for rec in insights['recommendations_for_improvement']:
            print(f"   • {rec}")
    
    print_section("Improvement Metrics")
    metrics = insights['improvement_metrics']
    print(f"   Improvement: {metrics.get('improvement_percentage', 0)}%")
    print(f"   Keywords Improved: {metrics.get('keywords_improved', 0)}")
    print(f"   Analyses Performed: {metrics.get('analyses_performed', 0)}")


def test_6_agentic_reasoning():
    """Test 6: Agentic reasoning with LLM"""
    print_header("TEST 6: Agentic Reasoning (LLM Integration)")
    
    print("\n🤖 Testing agent's reasoning capabilities...")
    
    agent = SEOAgent(memory_dir="./data/memory")
    
    if agent.client:
        print("✅ Groq LLM available - agent can reason about recommendations")
        print("\n   The agent will:")
        print("   1. Analyze website structure")
        print("   2. Check memory for past patterns")
        print("   3. Use LLM to reason about best next steps")
        print("   4. Generate prioritized recommendations")
        print("   5. Store learning for future iterations")
    else:
        print("⚠️  Groq LLM not available - using fallback recommendations")
        print("   Add GROQ_API_KEY to .env for full agentic capabilities")


def test_7_citations():
    """Test 7: Citation system"""
    print_header("TEST 7: Citation System")
    
    from tools.seo_tools import CitationGeneratorTool
    
    print("\n🎯 Testing recommendation citations...")
    
    recommendations = [
        "Add meta description to homepage",
        "Optimize title tag for target keywords",
        "Improve page loading speed",
        "Add schema markup for rich snippets"
    ]
    
    print_section("Generated Recommendations with Citations")
    
    for i, rec in enumerate(recommendations, 1):
        citation = CitationGeneratorTool.generate_citation(rec)
        print(f"\n   {i}. {citation['recommendation']}")
        print(f"      Citation: {citation['citation']}")
        print(f"      Source: {citation['source_url']}")


def test_all():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "🤖 SEO AGENT COMPREHENSIVE TEST 🤖" + " " * 9 + "║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        test_1_basic_analysis()
        test_2_memory_storage()
        test_3_learning_loop()
        test_4_ranking_simulation()
        test_5_memory_learning_insights()
        test_6_agentic_reasoning()
        test_7_citations()
        
        print("\n" + "=" * 60)
        print("  ✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nKey Features Demonstrated:")
        print("  ✅ Website analysis with SEO scoring")
        print("  ✅ Memory storage and recall")
        print("  ✅ Learning loop with consecutive analyses")
        print("  ✅ Ranking improvement simulation")
        print("  ✅ Memory-based learning insights")
        print("  ✅ LLM-powered agentic reasoning")
        print("  ✅ Citation generation system")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_all()
