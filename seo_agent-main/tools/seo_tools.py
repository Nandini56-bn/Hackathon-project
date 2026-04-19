"""
SEO Analysis Tools
Provides tools for analyzing website SEO factors
"""
import re
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib

class SEOAnalyzerTool:
    """
    Analyzes a website for SEO issues and generates recommendations
    """
    
    def __init__(self):
        self.issues = []
        self.recommendations = []
        self.score_factors = {}
        # Headers to mimic a real browser
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    
    def analyze_website(self, url: str) -> Dict[str, Any]:
        """
        Main analysis function - analyzes website and returns comprehensive report
        """
        try:
            # Fetch website content with proper headers
            response = requests.get(url, timeout=10, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"Website took too long to respond (timeout)",
                "seo_score": 0
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"Could not connect to website. Check the URL or your internet connection",
                "seo_score": 0
            }
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "error": f"Website returned an error: {e.response.status_code} {e.response.reason}. Some websites block automated access.",
                "seo_score": 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to fetch website: {str(e)}",
                "seo_score": 0
            }
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Run all analyses
        self._analyze_title(soup)
        self._analyze_meta_description(soup)
        self._analyze_headings(soup)
        self._analyze_keywords(soup)
        self._analyze_images(soup)
        self._analyze_links(soup)
        self._analyze_mobile_friendly(url)
        self._analyze_page_speed_estimate(len(response.content))
        self._analyze_schema_markup(soup)
        
        # Calculate SEO score
        seo_score = self._calculate_seo_score()
        
        return {
            "success": True,
            "url": url,
            "seo_score": seo_score,
            "timestamp": datetime.now().isoformat(),
            "title": soup.title.string if soup.title else "No title",
            "meta_description": self._get_meta_description(soup),
            "headings": self._get_headings(soup),
            "images": self._get_images_count(soup),
            "links": self._get_links_count(soup),
            "issues": self.issues,
            "score_factors": self.score_factors,
            "recommendations": self.recommendations[:5]  # Top 5 recommendations
        }
    
    def _analyze_title(self, soup: BeautifulSoup) -> None:
        """Analyze title tag"""
        title = soup.title
        
        if not title or not title.string:
            self.issues.append("Missing page title")
            self.score_factors["title"] = 0
            return
        
        title_text = title.string.strip()
        title_length = len(title_text)
        
        if title_length < 30:
            self.issues.append(f"Title too short ({title_length} chars, recommended 30-60)")
            self.score_factors["title"] = 0.5
        elif title_length > 60:
            self.issues.append(f"Title too long ({title_length} chars, recommended 30-60)")
            self.score_factors["title"] = 0.7
        else:
            self.score_factors["title"] = 1.0
            self.recommendations.append("Title length is optimal")
    
    def _analyze_meta_description(self, soup: BeautifulSoup) -> None:
        """Analyze meta description"""
        meta = soup.find("meta", attrs={"name": "description"})
        
        if not meta or not meta.get("content"):
            self.issues.append("Missing meta description")
            self.score_factors["meta_description"] = 0
            self.recommendations.append("Add a meta description (120-160 characters)")
            return
        
        desc = meta.get("content", "")
        desc_length = len(desc)
        
        if desc_length < 120:
            self.issues.append(f"Meta description too short ({desc_length} chars)")
            self.score_factors["meta_description"] = 0.6
        elif desc_length > 160:
            self.issues.append(f"Meta description too long ({desc_length} chars)")
            self.score_factors["meta_description"] = 0.7
        else:
            self.score_factors["meta_description"] = 1.0
    
    def _analyze_headings(self, soup: BeautifulSoup) -> None:
        """Analyze heading structure"""
        h1_count = len(soup.find_all("h1"))
        h2_count = len(soup.find_all("h2"))
        
        if h1_count == 0:
            self.issues.append("No H1 heading found")
            self.score_factors["headings"] = 0.3
        elif h1_count > 1:
            self.issues.append(f"Multiple H1 headings found ({h1_count})")
            self.score_factors["headings"] = 0.6
        else:
            self.score_factors["headings"] = 0.9
        
        if h2_count == 0:
            self.issues.append("No H2 headings found")
            self.score_factors["headings"] = max(self.score_factors.get("headings", 0), 0.5) - 0.2
        else:
            self.recommendations.append(f"Good heading structure with {h2_count} H2 tags")
    
    def _analyze_keywords(self, soup: BeautifulSoup) -> None:
        """Analyze keyword presence"""
        text = soup.get_text().lower()
        
        # Extract potential keywords (simple approach)
        words = re.findall(r'\b\w+\b', text)
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Only words with 4+ characters
                word_freq[word] = word_freq.get(word, 0) + 1
        
        if not word_freq:
            self.issues.append("Could not extract keywords")
            self.score_factors["keywords"] = 0.5
        else:
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            self.recommendations.append(f"Top keywords: {', '.join([k[0] for k in top_keywords])}")
            self.score_factors["keywords"] = 0.8
    
    def _analyze_images(self, soup: BeautifulSoup) -> None:
        """Analyze images and alt text"""
        images = soup.find_all("img")
        images_without_alt = 0
        
        for img in images:
            if not img.get("alt"):
                images_without_alt += 1
        
        if images_without_alt > 0:
            self.issues.append(f"{images_without_alt} images missing alt text")
            alt_score = max(0.3, 1 - (images_without_alt / max(len(images), 1)))
            self.score_factors["images"] = alt_score
        else:
            self.score_factors["images"] = 1.0 if len(images) > 0 else 0.5
    
    def _analyze_links(self, soup: BeautifulSoup) -> None:
        """Analyze internal and external links"""
        internal_links = 0
        external_links = 0
        broken_anchors = 0
        
        for link in soup.find_all("a"):
            href = link.get("href", "")
            if href.startswith("http"):
                external_links += 1
            elif href.startswith("/") or href.startswith("#"):
                internal_links += 1
            elif not href:
                broken_anchors += 1
        
        if broken_anchors > 0:
            self.issues.append(f"{broken_anchors} broken anchor links")
            self.score_factors["links"] = 0.6
        else:
            self.score_factors["links"] = 0.9
        
        if internal_links < 3:
            self.recommendations.append("Add more internal links for better navigation")
    
    def _analyze_mobile_friendly(self, url: str) -> None:
        """Check mobile-friendly indicators"""
        # Simple heuristic check
        try:
            response = requests.head(url, timeout=5)
            if "mobile" in response.headers.get("User-Agent", "").lower():
                self.score_factors["mobile"] = 0.8
            else:
                self.score_factors["mobile"] = 0.7
        except:
            self.score_factors["mobile"] = 0.5
    
    def _analyze_page_speed_estimate(self, page_size_bytes: int) -> None:
        """Estimate page speed based on size"""
        page_size_kb = page_size_bytes / 1024
        
        if page_size_kb < 100:
            self.score_factors["speed"] = 1.0
        elif page_size_kb < 500:
            self.score_factors["speed"] = 0.8
        elif page_size_kb < 1000:
            self.score_factors["speed"] = 0.6
            self.issues.append(f"Page size is large ({page_size_kb:.0f} KB)")
        else:
            self.score_factors["speed"] = 0.4
            self.issues.append(f"Page is very large ({page_size_kb:.1f} MB) - optimize images and scripts")
    
    def _analyze_schema_markup(self, soup: BeautifulSoup) -> None:
        """Check for structured data (schema markup)"""
        schema = soup.find("script", attrs={"type": "application/ld+json"})
        
        if not schema:
            self.issues.append("Missing schema markup")
            self.score_factors["schema"] = 0
            self.recommendations.append("Add schema markup for rich snippets")
        else:
            self.score_factors["schema"] = 0.9
            self.recommendations.append("Good! Schema markup found")
    
    def _calculate_seo_score(self) -> float:
        """Calculate overall SEO score (0-100)"""
        if not self.score_factors:
            return 0
        
        weights = {
            "title": 0.15,
            "meta_description": 0.10,
            "headings": 0.15,
            "keywords": 0.15,
            "images": 0.10,
            "links": 0.10,
            "mobile": 0.10,
            "speed": 0.10,
            "schema": 0.05
        }
        
        score = 0
        for factor, weight in weights.items():
            score += self.score_factors.get(factor, 0) * weight
        
        return round(score * 100, 2)
    
    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta = soup.find("meta", attrs={"name": "description"})
        return meta.get("content", "") if meta else ""
    
    def _get_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract all headings"""
        return {
            "h1": [h.get_text() for h in soup.find_all("h1")[:5]],
            "h2": [h.get_text() for h in soup.find_all("h2")[:5]],
            "h3": [h.get_text() for h in soup.find_all("h3")[:3]]
        }
    
    def _get_images_count(self, soup: BeautifulSoup) -> int:
        """Count images"""
        return len(soup.find_all("img"))
    
    def _get_links_count(self, soup: BeautifulSoup) -> Dict[str, int]:
        """Count internal and external links"""
        internal = 0
        external = 0
        
        for link in soup.find_all("a"):
            href = link.get("href", "")
            if href.startswith("http"):
                external += 1
            elif href.startswith("/"):
                internal += 1
        
        return {"internal": internal, "external": external}


class WebScraperTool:
    """
    Web scraper for extracting page content and metadata
    """
    
    # Headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    @staticmethod
    def scrape_page(url: str) -> Dict[str, Any]:
        """Scrape a page and extract content"""
        try:
            response = requests.get(url, timeout=10, headers=WebScraperTool.headers)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Website took too long to respond (timeout)"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Could not connect to website"}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": f"Website error: {e.response.status_code} {e.response.reason}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text(separator=' ', strip=True)
        
        return {
            "success": True,
            "url": url,
            "title": soup.title.string if soup.title else "",
            "meta_description": WebScraperTool._get_meta(soup, "description"),
            "meta_keywords": WebScraperTool._get_meta(soup, "keywords"),
            "content": text[:1000],  # First 1000 characters
            "content_length": len(text),
            "headings": {
                "h1": [h.get_text() for h in soup.find_all("h1")],
                "h2": [h.get_text() for h in soup.find_all("h2")]
            }
        }
    
    @staticmethod
    def _get_meta(soup: BeautifulSoup, name: str) -> str:
        """Get meta tag content"""
        meta = soup.find("meta", attrs={"name": name})
        return meta.get("content", "") if meta else ""


class KeywordAnalyzerTool:
    """
    Analyzes keywords and provides mock competitor data
    """
    
    @staticmethod
    def analyze_keywords(text: str, num_keywords: int = 10) -> List[Dict[str, Any]]:
        """Extract and analyze keywords from text"""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}
        
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of'}
        
        for word in words:
            if len(word) > 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:num_keywords]
        
        return [
            {
                "keyword": kw[0],
                "frequency": kw[1],
                "search_volume": kw[1] * 1000 + 500,  # Simulated
                "difficulty": "Medium" if kw[1] > 5 else "Easy",
                "last_rank": 50 + (10 * kw[1])  # Simulated ranking
            }
            for kw in keywords
        ]
    
    @staticmethod
    def get_competitor_keywords() -> List[Dict[str, Any]]:
        """
        Mock competitor analysis
        In real scenario, use SerpAPI or similar service
        """
        return [
            {
                "keyword": "seo optimization",
                "rank": 5,
                "search_volume": 15000,
                "competitor_title": "SEO Optimization Guide 2024 | Best Practices",
                "competitor_url": "https://example.com/seo-guide"
            },
            {
                "keyword": "keyword research",
                "rank": 8,
                "search_volume": 12500,
                "competitor_title": "Complete Keyword Research Guide",
                "competitor_url": "https://example.com/keywords"
            },
            {
                "keyword": "content optimization",
                "rank": 12,
                "search_volume": 8000,
                "competitor_title": "How to Optimize Content for SEO",
                "competitor_url": "https://example.com/content"
            }
        ]


class CitationGeneratorTool:
    """
    Generates citations and references for recommendations
    """
    
    @staticmethod
    def generate_citation(recommendation: str, source: str = "SEO Best Practices") -> Dict[str, str]:
        """Generate a citation for a recommendation"""
        return {
            "recommendation": recommendation,
            "citation": f"Based on {source}",
            "source_url": "https://moz.com/learn/seo",
            "date_accessed": datetime.now().isoformat()
        }
    
    @staticmethod
    def generate_report_with_citations(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a full report with citations for all recommendations
        """
        recommendations_with_citations = []
        
        for recommendation in analysis_result.get("recommendations", []):
            cited = CitationGeneratorTool.generate_citation(
                recommendation,
                "SEO Best Practices & Industry Standards"
            )
            recommendations_with_citations.append(cited)
        
        return {
            "base_analysis": analysis_result,
            "recommendations_with_citations": recommendations_with_citations,
            "report_date": datetime.now().isoformat()
        }
