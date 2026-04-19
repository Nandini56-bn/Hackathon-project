"""
Hindsight Memory System for SEO Agent
Stores and recalls past interactions, suggestions, and improvements
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class HindsightMemory:
    """
    Memory system that stores:
    - Website analysis history
    - Past suggestions and their effectiveness
    - Keywords used and their performance
    - Ranking changes and improvements
    """
    
    def __init__(self, memory_dir: str = "./data/memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.analysis_file = self.memory_dir / "analysis_history.json"
        self.suggestions_file = self.memory_dir / "suggestions.json"
        self.keywords_file = self.memory_dir / "keywords.json"
        self.improvements_file = self.memory_dir / "improvements.json"
        
        # Initialize files if they don't exist
        for file_path in [self.analysis_file, self.suggestions_file, 
                          self.keywords_file, self.improvements_file]:
            if not file_path.exists():
                file_path.write_text(json.dumps({}))
    
    def store_analysis(self, website_url: str, analysis_data: Dict[str, Any]) -> None:
        """Store a website analysis with timestamp"""
        data = json.loads(self.analysis_file.read_text())
        
        if website_url not in data:
            data[website_url] = []
        
        analysis_data["timestamp"] = datetime.now().isoformat()
        data[website_url].append(analysis_data)
        
        self.analysis_file.write_text(json.dumps(data, indent=2))
    
    def get_analysis_history(self, website_url: str) -> List[Dict[str, Any]]:
        """Retrieve all past analyses for a website"""
        data = json.loads(self.analysis_file.read_text())
        return data.get(website_url, [])
    
    def store_suggestion(self, website_url: str, suggestion: Dict[str, Any]) -> None:
        """Store a suggestion with metadata"""
        data = json.loads(self.suggestions_file.read_text())
        
        if website_url not in data:
            data[website_url] = []
        
        suggestion["id"] = f"sug_{len(data.get(website_url, []))}"
        suggestion["timestamp"] = datetime.now().isoformat()
        suggestion["effectiveness"] = 0  # Will be updated based on results
        
        data[website_url].append(suggestion)
        self.suggestions_file.write_text(json.dumps(data, indent=2))
    
    def get_suggestions(self, website_url: str) -> List[Dict[str, Any]]:
        """Retrieve all past suggestions for a website"""
        data = json.loads(self.suggestions_file.read_text())
        return data.get(website_url, [])
    
    def store_keyword_performance(self, website_url: str, keyword: str, 
                                  rank: int, search_volume: int) -> None:
        """Store keyword performance metrics"""
        data = json.loads(self.keywords_file.read_text())
        
        if website_url not in data:
            data[website_url] = {}
        
        if keyword not in data[website_url]:
            data[website_url][keyword] = []
        
        data[website_url][keyword].append({
            "timestamp": datetime.now().isoformat(),
            "rank": rank,
            "search_volume": search_volume
        })
        
        self.keywords_file.write_text(json.dumps(data, indent=2))
    
    def get_keyword_performance(self, website_url: str, keyword: str) -> List[Dict]:
        """Get performance history for a specific keyword"""
        data = json.loads(self.keywords_file.read_text())
        return data.get(website_url, {}).get(keyword, [])
    
    def calculate_improvement(self, website_url: str) -> Dict[str, Any]:
        """
        Calculate overall improvement metrics
        Returns: improvement percentage, days analyzed, keywords improved
        """
        history = self.get_analysis_history(website_url)
        
        if len(history) < 2:
            return {
                "improvement_percentage": 0,
                "days_analyzed": 0,
                "keywords_improved": 0,
                "initial_score": 0,
                "current_score": 0
            }
        
        first_analysis = history[0]
        last_analysis = history[-1]
        
        initial_score = first_analysis.get("seo_score", 0)
        current_score = last_analysis.get("seo_score", 0)
        improvement = current_score - initial_score
        improvement_percentage = (improvement / initial_score * 100) if initial_score > 0 else 0
        
        # Calculate days difference
        first_date = datetime.fromisoformat(first_analysis["timestamp"])
        last_date = datetime.fromisoformat(last_analysis["timestamp"])
        days_analyzed = (last_date - first_date).days
        
        # Count keywords improved
        keywords_improved = self._count_keywords_improved(website_url)
        
        return {
            "improvement_percentage": round(improvement_percentage, 2),
            "improvement_points": round(improvement, 2),
            "days_analyzed": days_analyzed,
            "keywords_improved": keywords_improved,
            "initial_score": round(initial_score, 2),
            "current_score": round(current_score, 2),
            "analyses_performed": len(history)
        }
    
    def _count_keywords_improved(self, website_url: str) -> int:
        """Count how many keywords have improved"""
        data = json.loads(self.keywords_file.read_text())
        keywords = data.get(website_url, {})
        improved_count = 0
        
        for keyword, history in keywords.items():
            if len(history) >= 2:
                initial_rank = history[0]["rank"]
                current_rank = history[-1]["rank"]
                if current_rank < initial_rank:  # Lower rank = better
                    improved_count += 1
        
        return improved_count
    
    def get_learning_insights(self, website_url: str) -> Dict[str, Any]:
        """
        Generate insights from memory to improve future suggestions
        """
        suggestions = self.get_suggestions(website_url)
        history = self.get_analysis_history(website_url)
        
        # Find effective suggestions
        effective_suggestions = []
        for suggestion in suggestions:
            if suggestion.get("effectiveness", 0) > 0.7:
                effective_suggestions.append(suggestion)
        
        # Most common issues found
        common_issues = {}
        for analysis in history:
            issues = analysis.get("issues", [])
            for issue in issues:
                common_issues[issue] = common_issues.get(issue, 0) + 1
        
        return {
            "total_suggestions": len(suggestions),
            "effective_suggestions": len(effective_suggestions),
            "most_common_issues": dict(sorted(common_issues.items(), 
                                            key=lambda x: x[1], reverse=True)[:5]),
            "improvement_metrics": self.calculate_improvement(website_url),
            "recommendations_for_improvement": self._generate_recommendations(website_url)
        }
    
    def _generate_recommendations(self, website_url: str) -> List[str]:
        """Generate AI recommendations based on memory"""
        insights = json.loads(self.improvements_file.read_text())
        site_insights = insights.get(website_url, {})
        
        recommendations = []
        
        # Check if title has been improved
        if site_insights.get("title_improved"):
            recommendations.append("Keep optimizing titles based on top-performing keywords")
        
        # Check if meta descriptions helped
        if site_insights.get("meta_description_helped"):
            recommendations.append("Continue focusing on compelling meta descriptions")
        
        # Check if keywords have improved
        if site_insights.get("keywords_improved_count", 0) > 0:
            recommendations.append("Focus on the keywords that showed improvement in past iterations")
        
        if not recommendations:
            recommendations.append("Start implementing basic SEO best practices on your website")
            recommendations.append("Monitor ranking changes for each suggestion")
        
        return recommendations
    
    def store_improvement_metric(self, website_url: str, metric_name: str, 
                                 value: bool) -> None:
        """Store metrics about what improvements worked"""
        data = json.loads(self.improvements_file.read_text())
        
        if website_url not in data:
            data[website_url] = {}
        
        data[website_url][metric_name] = value
        self.improvements_file.write_text(json.dumps(data, indent=2))
    
    def reset_memory(self, website_url: str) -> None:
        """Reset memory for a specific website"""
        for file_path in [self.analysis_file, self.suggestions_file, 
                          self.keywords_file, self.improvements_file]:
            data = json.loads(file_path.read_text())
            if website_url in data:
                del data[website_url]
            file_path.write_text(json.dumps(data, indent=2))
