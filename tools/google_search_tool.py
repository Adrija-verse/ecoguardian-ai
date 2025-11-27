"""
Google Search Tool - EcoGuardian AI
Built-in tool for searching climate news, research papers, and real-time environmental data.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Configure logging
logger = logging.getLogger(__name__)


class GoogleSearchTool:
    """
    Tool for performing web searches to gather current environmental information.
    """
    
    def __init__(self, api_key: Optional[str] = None, search_engine_id: Optional[str] = None):
        """Initialize the Google Search Tool."""
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.search_history = []
        logger.info("GoogleSearchTool initialized")
    
    async def search(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """Perform a search query and return results."""
        logger.info(f"Performing search: '{query}'")
        
        search_result = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "num_results": num_results,
            "results": [],
            "status": "completed"
        }
        
        try:
            await asyncio.sleep(0.2)  # Simulate API latency
            search_result["results"] = self._generate_simulated_results(query, num_results)
            self.search_history.append(search_result)
            logger.info(f"Search completed: {len(search_result['results'])} results found")
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            search_result["status"] = "failed"
            search_result["error"] = str(e)
        
        return search_result
    
    # ✅ FIXED: Now properly accepts TWO positional arguments
    async def search_climate_news(self, location: str = "Global", topic: str = "climate change") -> Dict[str, Any]:
        """
        Search for recent climate and environmental news.
        
        Args:
            location: Geographic location to search for (default: "Global")
            topic: Topic to search for (default: "climate change")
        
        Returns:
            Dict containing search results
        """
        query = f"{topic} environmental news {location} latest"
        return await self.search(query, num_results=5)
    
    async def search_pollution_data(self, location: str) -> Dict[str, Any]:
        """Search for pollution and air quality data."""
        query = f"air pollution air quality data {location} current"
        return await self.search(query, num_results=5)
    
    def _generate_simulated_results(self, query: str, num_results: int) -> List[Dict]:
        """Generate simulated search results."""
        results = []
        
        # Extract location/topic from query for more relevant results
        query_terms = query.split()
        location = "Global"
        
        # Try to extract location from query
        for i, term in enumerate(query_terms):
            if term.lower() in ["news", "latest", "environmental"]:
                if i > 0:
                    location = query_terms[i-1]
                    break
        
        result_templates = [
            {
                "title": f"Climate Change Impact on {location} - Latest Report 2024",
                "snippet": "Recent studies show significant environmental changes affecting urban ecosystems. Temperature increases and pollution levels require immediate action.",
                "url": "https://example.com/climate-report-2024",
                "source": "Environmental Science Journal",
                "rank": 1,
                "relevance_score": 1.0
            },
            {
                "title": f"Environmental News: {location} Green Initiative Launched",
                "snippet": "City launches comprehensive sustainability program aimed at reducing emissions by 30% over the next decade through renewable energy and green infrastructure.",
                "url": "https://example.com/green-initiative",
                "source": "Green Tech Today",
                "rank": 2,
                "relevance_score": 0.9
            },
            {
                "title": f"Air Quality Index - {location} Real-time Data",
                "snippet": "Current AQI readings show moderate pollution levels. PM2.5 concentrations monitored across 15 stations throughout the metropolitan area.",
                "url": "https://example.com/aqi-data",
                "source": "Air Quality Monitoring Network",
                "rank": 3,
                "relevance_score": 0.8
            },
            {
                "title": f"Urban Sustainability: {location}'s Path to Carbon Neutrality",
                "snippet": "Experts outline roadmap for achieving net-zero emissions by 2040, including electric vehicle adoption and building energy efficiency improvements.",
                "url": "https://example.com/carbon-neutral",
                "source": "Urban Development Review",
                "rank": 4,
                "relevance_score": 0.75
            },
            {
                "title": f"Public Health Alert: {location} Air Quality Concerns",
                "snippet": "Health officials recommend limiting outdoor activities as pollution levels exceed safe thresholds. Vulnerable populations should take precautions.",
                "url": "https://example.com/health-alert",
                "source": "Public Health Department",
                "rank": 5,
                "relevance_score": 0.7
            }
        ]
        
        for i in range(min(num_results, len(result_templates))):
            result = result_templates[i].copy()
            result["rank"] = i + 1
            result["relevance_score"] = round(1.0 - (i * 0.1), 2)
            results.append(result)
        
        return results
    
    def extract_key_information(self, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key information from search results."""
        extracted = {
            "query": search_results.get("query"),
            "timestamp": search_results.get("timestamp"),
            "key_findings": [],
            "sources": []
        }
        
        for result in search_results.get("results", []):
            extracted["key_findings"].append({
                "title": result.get("title"),
                "summary": result.get("snippet"),
                "relevance": result.get("relevance_score", 0)
            })
            extracted["sources"].append(result.get("url"))
        
        return extracted
    
    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent search history."""
        return self.search_history[-limit:]
    
    def clear_history(self):
        """Clear search history."""
        self.search_history.clear()
        logger.info("Search history cleared")


# Global instance
google_search_tool = GoogleSearchTool()