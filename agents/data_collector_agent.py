"""
EcoGuardian AI - Data Collector Agent (FIXED)
Parallel agent that fetches environmental data from multiple sources
"""

import asyncio
from typing import Dict, Any, List
from tools.weather_api_tool import weather_api
from tools.carbon_calculator import carbon_calculator
from memory.session_manager import memory_bank
from observability.logger import eco_logger

class DataCollectorAgent:
    """
    Parallel Agent: Collects environmental data from multiple sources simultaneously
    Demonstrates parallel agent execution for efficiency
    """
    
    def __init__(self):
        self.name = "DataCollectorAgent"
        self.version = "1.0"
        self.tools = {
            "weather_api": weather_api,
            "carbon_calculator": carbon_calculator
        }
        
        eco_logger.log_agent_action(
            self.name,
            "INITIALIZED",
            {"version": self.version, "tools": list(self.tools.keys())}
        )
    
    # ✅ FIXED: Changed to async method
    async def collect_city_data(self, city: str, coordinates: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Collect comprehensive environmental data for a city
        Uses parallel execution to fetch data efficiently
        
        Args:
            city: City name
            coordinates: Optional dict with 'lat' and 'lon'
        
        Returns:
            Aggregated environmental data
        """
        eco_logger.log_agent_action(
            self.name,
            "START_COLLECTION",
            {"city": city, "has_coordinates": coordinates is not None}
        )
        
        # ✅ FIXED: Now properly awaits async method
        results = await self._parallel_collect(city, coordinates)
        
        # Aggregate results
        aggregated_data = self._aggregate_data(city, results)
        
        # Store in memory bank for future reference
        memory_bank.store(
            "city_profiles",
            city.lower(),
            aggregated_data
        )
        
        eco_logger.log_agent_action(
            self.name,
            "COLLECTION_COMPLETE",
            {
                "city": city,
                "data_sources": list(results.keys()),
                "aqi": aggregated_data.get("air_quality", {}).get("aqi")
            }
        )
        
        return aggregated_data
    
    async def _parallel_collect(self, city: str, coordinates: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Execute parallel data collection tasks
        This demonstrates parallel agent pattern for concurrent operations
        """
        tasks = []
        
        # Task 1: Fetch current weather
        tasks.append(self._fetch_weather(city))
        
        # Task 2: Fetch weather forecast
        tasks.append(self._fetch_forecast(city))
        
        # Task 3: Fetch air quality
        weather_result = await self._fetch_weather(city)
        if weather_result.get("success") and "coordinates" in weather_result:
            coords = weather_result["coordinates"]
            tasks.append(self._fetch_air_quality(coords["lat"], coords["lon"]))
        elif coordinates:
            tasks.append(self._fetch_air_quality(coordinates.get("lat", 0), coordinates.get("lon", 0)))
        
        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "weather": results[0] if len(results) > 0 else {},
            "forecast": results[1] if len(results) > 1 else {},
            "air_quality": results[2] if len(results) > 2 else {}
        }
    
    async def _fetch_weather(self, city: str) -> Dict[str, Any]:
        """Async wrapper for weather API call"""
        return await asyncio.to_thread(weather_api.get_weather, city)
    
    async def _fetch_forecast(self, city: str) -> Dict[str, Any]:
        """Async wrapper for forecast API call"""
        return await asyncio.to_thread(weather_api.get_forecast, city, days=3)
    
    async def _fetch_air_quality(self, lat: float, lon: float) -> Dict[str, Any]:
        """Async wrapper for air quality API call"""
        return await asyncio.to_thread(weather_api.get_air_quality, lat, lon)
    
    def _aggregate_data(self, city: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate and structure collected data"""
        weather_data = results.get("weather", {})
        forecast_data = results.get("forecast", {})
        air_quality_data = results.get("air_quality", {})
        
        # Calculate environmental score (0-100, higher is better)
        env_score = self._calculate_environmental_score(weather_data, air_quality_data)
        
        aggregated = {
            "city": city,
            "collection_timestamp": eco_logger.traces[-1]["timestamp"] if eco_logger.traces else None,
            "environmental_score": env_score,
            "weather": weather_data,
            "forecast": forecast_data,
            "air_quality": air_quality_data,
            "recommendations": self._generate_recommendations(env_score, air_quality_data),
            "success": all([
                weather_data.get("success", False),
                air_quality_data.get("success", False)
            ])
        }
        
        return aggregated
    
    def _calculate_environmental_score(
        self,
        weather: Dict[str, Any],
        air_quality: Dict[str, Any]
    ) -> float:
        """Calculate overall environmental health score (0-100)"""
        score = 100.0
        
        # AQI penalty (AQI scale 1-5)
        if air_quality.get("success"):
            aqi = air_quality.get("aqi", 3)
            score -= (aqi - 1) * 15
        
        # Temperature extremes penalty
        if weather.get("success"):
            temp = weather.get("temperature_celsius", 20)
            if temp < 0 or temp > 35:
                score -= 10
        
        # High humidity penalty
        if weather.get("success"):
            humidity = weather.get("humidity_percent", 50)
            if humidity > 80:
                score -= 5
        
        # Low wind penalty
        if weather.get("success"):
            wind = weather.get("wind_speed_mps", 3)
            if wind < 1:
                score -= 10
        
        return max(0, min(100, score))
    
    def _generate_recommendations(
        self,
        env_score: float,
        air_quality: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable recommendations based on data"""
        recommendations = []
        
        if env_score < 50:
            recommendations.append("URGENT: Environmental conditions are poor. Consider indoor activities.")
        elif env_score < 70:
            recommendations.append("WARNING: Moderate conditions. Sensitive groups should limit outdoor exposure.")
        else:
            recommendations.append("OK: Good environmental conditions for outdoor activities.")
        
        # AQI-specific recommendations
        if air_quality.get("success"):
            aqi = air_quality.get("aqi", 0)
            if aqi >= 4:
                recommendations.append("MASK: Wear a mask outdoors due to poor air quality.")
                recommendations.append("TREES: Support tree planting initiatives to improve air quality.")
            
            pollutants = air_quality.get("pollutants", {})
            if pollutants.get("pm2_5", 0) > 35:
                recommendations.append("INDUSTRY: PM2.5 levels high. Advocate for industrial emission controls.")
            if pollutants.get("no2", 0) > 200:
                recommendations.append("TRANSPORT: NO2 levels high. Consider public transit or carpooling.")
        
        return recommendations
    
    def collect_user_carbon_data(self, activities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate user's carbon footprint"""
        eco_logger.log_agent_action(
            self.name,
            "CALCULATE_USER_CARBON",
            {"activity_count": len(activities)}
        )
        
        footprint = carbon_calculator.calculate_total_footprint(activities)
        
        # Store in memory for tracking
        memory_bank.store(
            "user_carbon_history",
            str(eco_logger.traces[-1]["timestamp"]),
            footprint
        )
        
        return footprint

# Global instance
data_collector_agent = DataCollectorAgent()