"""
EcoGuardian AI - Weather & Pollution API Tool (OpenAPI Integration)
Fetches real-time environmental data from OpenWeatherMap
"""

import requests
from typing import Dict, Any, Optional
from config.settings import Settings
from observability.logger import eco_logger

class WeatherAPITool:
    """
    OpenAPI Tool: Integrates with OpenWeatherMap API
    Fetches air quality and weather data for pollution analysis
    """
    
    def __init__(self):
        self.name = "WeatherAPITool"
        self.api_key = Settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        eco_logger.log_agent_action(
            self.name,
            "INITIALIZED",
            {"api_configured": bool(self.api_key)}
        )
    
    def get_air_quality(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetch current air quality data for coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            Air quality data with AQI and pollutant levels
        """
        try:
            url = f"{self.base_url}/air_pollution"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key
            }
            
            eco_logger.logger.debug(f"🌍 Fetching air quality for ({lat}, {lon})")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse API response
            air_quality = self._parse_air_quality(data)
            
            eco_logger.log_tool_usage(
                self.name,
                input_data={"lat": lat, "lon": lon, "endpoint": "air_pollution"},
                output_data={"aqi": air_quality.get("aqi")}
            )
            eco_logger.record_metric("api_calls", 1)
            
            return air_quality
            
        except requests.exceptions.RequestException as e:
            eco_logger.log_error(self.name, e, {"lat": lat, "lon": lon})
            return self._error_response(f"API request failed: {str(e)}")
        except Exception as e:
            eco_logger.log_error(self.name, e, {"lat": lat, "lon": lon})
            return self._error_response(str(e))
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Fetch current weather data for a city
        
        Args:
            city: City name
        
        Returns:
            Weather data including temperature, humidity, etc.
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"  # Celsius
            }
            
            eco_logger.logger.debug(f"☀️ Fetching weather for {city}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse weather data
            weather = self._parse_weather(data)
            
            eco_logger.log_tool_usage(
                self.name,
                input_data={"city": city, "endpoint": "weather"},
                output_data={"temp": weather.get("temperature_celsius")}
            )
            eco_logger.record_metric("api_calls", 1)
            
            return weather
            
        except requests.exceptions.RequestException as e:
            eco_logger.log_error(self.name, e, {"city": city})
            return self._error_response(f"API request failed: {str(e)}")
        except Exception as e:
            eco_logger.log_error(self.name, e, {"city": city})
            return self._error_response(str(e))
    
    def get_forecast(self, city: str, days: int = 3) -> Dict[str, Any]:
        """
        Get weather forecast for coming days
        
        Args:
            city: City name
            days: Number of days (max 5 for free tier)
        
        Returns:
            Forecast data
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "cnt": days * 8  # 3-hour intervals
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            forecast = self._parse_forecast(data, days)
            
            eco_logger.log_tool_usage(
                self.name,
                input_data={"city": city, "days": days},
                output_data={"forecast_points": len(forecast.get("forecasts", []))}
            )
            
            return forecast
            
        except Exception as e:
            eco_logger.log_error(self.name, e, {"city": city})
            return self._error_response(str(e))
    
    def _parse_air_quality(self, data: Dict) -> Dict[str, Any]:
        """Parse air quality API response"""
        if "list" not in data or len(data["list"]) == 0:
            return self._error_response("No air quality data available")
        
        aqi_data = data["list"][0]
        main = aqi_data.get("main", {})
        components = aqi_data.get("components", {})
        
        # AQI scale: 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor
        aqi = main.get("aqi", 0)
        aqi_labels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        
        return {
            "success": True,
            "aqi": aqi,
            "aqi_label": aqi_labels.get(aqi, "Unknown"),
            "pollutants": {
                "co": components.get("co", 0),  # Carbon monoxide
                "no": components.get("no", 0),  # Nitrogen monoxide
                "no2": components.get("no2", 0),  # Nitrogen dioxide
                "o3": components.get("o3", 0),  # Ozone
                "so2": components.get("so2", 0),  # Sulphur dioxide
                "pm2_5": components.get("pm2_5", 0),  # Fine particles
                "pm10": components.get("pm10", 0),  # Coarse particles
                "nh3": components.get("nh3", 0)  # Ammonia
            },
            "health_implications": self._get_health_implications(aqi),
            "timestamp": aqi_data.get("dt")
        }
    
    def _parse_weather(self, data: Dict) -> Dict[str, Any]:
        """Parse weather API response"""
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        wind = data.get("wind", {})
        
        return {
            "success": True,
            "city": data.get("name", "Unknown"),
            "country": data.get("sys", {}).get("country", ""),
            "coordinates": {
                "lat": data.get("coord", {}).get("lat"),
                "lon": data.get("coord", {}).get("lon")
            },
            "temperature_celsius": main.get("temp"),
            "feels_like_celsius": main.get("feels_like"),
            "humidity_percent": main.get("humidity"),
            "pressure_hpa": main.get("pressure"),
            "description": weather.get("description", ""),
            "wind_speed_mps": wind.get("speed"),
            "wind_direction_deg": wind.get("deg"),
            "cloudiness_percent": data.get("clouds", {}).get("all"),
            "visibility_meters": data.get("visibility"),
            "timestamp": data.get("dt")
        }
    
    def _parse_forecast(self, data: Dict, days: int) -> Dict[str, Any]:
        """Parse forecast API response"""
        forecasts = []
        
        for item in data.get("list", []):
            forecasts.append({
                "timestamp": item.get("dt"),
                "datetime": item.get("dt_txt"),
                "temperature_celsius": item.get("main", {}).get("temp"),
                "description": item.get("weather", [{}])[0].get("description", ""),
                "humidity_percent": item.get("main", {}).get("humidity"),
                "rain_probability": item.get("pop", 0) * 100  # Probability of precipitation
            })
        
        return {
            "success": True,
            "city": data.get("city", {}).get("name"),
            "days_requested": days,
            "forecasts": forecasts
        }
    
    def _get_health_implications(self, aqi: int) -> str:
        """Get health implications based on AQI"""
        implications = {
            1: "Air quality is satisfactory, and air pollution poses little or no risk.",
            2: "Air quality is acceptable. However, there may be a risk for some people who are unusually sensitive to air pollution.",
            3: "Members of sensitive groups may experience health effects. The general public is less likely to be affected.",
            4: "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.",
            5: "Health alert: The risk of health effects is increased for everyone."
        }
        return implications.get(aqi, "Unknown health implications")
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """Standard error response"""
        return {
            "success": False,
            "error": message
        }


# ✅ CRITICAL: Create global instance
weather_api = WeatherAPITool()