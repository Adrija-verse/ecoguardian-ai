"""
EcoGuardian AI - Configuration Settings
Manages all environment variables and system configurations
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Central configuration for EcoGuardian AI system"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY", "")
    GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
    
    # Gemini Model Configuration - UPDATED TO LATEST MODELS
    GEMINI_MODEL = "models/gemini-2.5-flash"  # Latest stable model
    TEMPERATURE = 0.7
    MAX_OUTPUT_TOKENS = 2048
    
    # Agent Configuration
    MAX_ITERATIONS = 5
    AGENT_TIMEOUT = 300  # seconds
    
    # Memory Configuration
    MEMORY_WINDOW = 10  # Last N messages to remember
    CONTEXT_COMPRESSION_THRESHOLD = 5000  # Compress when context exceeds this
    
    # Observability
    LOG_LEVEL = "INFO"
    ENABLE_TRACING = True
    ENABLE_METRICS = True
    
    # Data Sources
    POLLUTION_DATA_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
    WEATHER_DATA_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    # Project Paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOGS_DIR = BASE_DIR / "logs"
    DATA_DIR = BASE_DIR / "data"
    
    # Simulation Parameters
    EMISSION_REDUCTION_TARGET = 0.20  # 20% reduction goal
    TREE_CO2_ABSORPTION_RATE = 22  # kg CO2 per tree per year
    
    @classmethod
    def validate(cls):
        """Validate that required API keys are set"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in .env file!")
        if not cls.OPENWEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY not found in .env file!")
        
        # Create directories if they don't exist
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.DATA_DIR.mkdir(exist_ok=True)
        
        return True

# Validate settings on import
try:
    Settings.validate()
    print("✅ Configuration loaded successfully!")
except ValueError as e:
    print(f"⚠️ Configuration Error: {e}")
    print("Please set up your .env file with required API keys.")