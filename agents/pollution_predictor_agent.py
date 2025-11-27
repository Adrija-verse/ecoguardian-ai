"""
EcoGuardian AI - Pollution Predictor Agent (Powered by Gemini)
Sequential agent that analyzes data and predicts optimal interventions
"""

import google.generativeai as genai
from typing import Dict, Any, List
import json
from config.settings import Settings
from memory.session_manager import memory_bank
from observability.logger import eco_logger

class PollutionPredictorAgent:
    """
    Sequential Agent: Analyzes environmental data and predicts interventions
    Powered by Google Gemini for natural language understanding
    Demonstrates LLM-powered agent with evaluation capabilities
    """
    
    def __init__(self):
        self.name = "PollutionPredictorAgent"
        self.version = "1.0"
        
        # Configure Gemini
        genai.configure(api_key=Settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Settings.GEMINI_MODEL)
        
        # Evaluation metrics
        self.predictions_made = 0
        self.prediction_accuracy = []
        
        eco_logger.log_agent_action(
            self.name,
            "INITIALIZED",
            {"model": Settings.GEMINI_MODEL, "version": self.version}
        )
    
    # FIXED: Removed the decorator - using manual logging instead
    def predict_interventions(
        self,
        city_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Predict optimal environmental interventions using AI
        
        Args:
            city_data: Current environmental data from DataCollectorAgent
            historical_data: Optional past data for trend analysis
        
        Returns:
            Predicted interventions with confidence scores
        """
        eco_logger.log_agent_action(
            self.name,
            "START_PREDICTION",
            {"city": city_data.get("city"), "env_score": city_data.get("environmental_score")}
        )
        
        # Retrieve historical context from memory
        if not historical_data:
            historical_data = self._get_historical_context(city_data.get("city"))
        
        # Generate AI prompt
        prompt = self._create_prediction_prompt(city_data, historical_data)
        
        # Get Gemini prediction
        try:
            response = self.model.generate_content(prompt)
            prediction_text = response.text
            
            # Parse structured predictions
            predictions = self._parse_gemini_response(prediction_text, city_data)
            
            # Self-evaluate prediction quality
            evaluation = self._evaluate_prediction(predictions, city_data)
            predictions["evaluation"] = evaluation
            
            self.predictions_made += 1
            
            eco_logger.log_agent_action(
                self.name,
                "PREDICTION_COMPLETE",
                {
                    "interventions_count": len(predictions.get("interventions", [])),
                    "confidence_avg": predictions.get("average_confidence", 0)
                }
            )
            
            # Store prediction in memory
            memory_bank.store(
                "predictions",
                f"{city_data.get('city')}_{self.predictions_made}",
                predictions
            )
            
            return predictions
            
        except Exception as e:
            eco_logger.log_error(self.name, e, {"city": city_data.get("city")})
            return self._fallback_prediction(city_data)
    
    def _create_prediction_prompt(
        self,
        city_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]]
    ) -> str:
        """
        Create structured prompt for Gemini
        Includes context, data, and expected output format
        """
        prompt = f"""You are an expert environmental scientist analyzing pollution data for {city_data.get('city')}.

CURRENT ENVIRONMENTAL DATA:
- Environmental Score: {city_data.get('environmental_score', 'N/A')}/100
- Air Quality Index (AQI): {city_data.get('air_quality', {}).get('aqi', 'N/A')} ({city_data.get('air_quality', {}).get('aqi_label', 'N/A')})
- Temperature: {city_data.get('weather', {}).get('temperature_celsius', 'N/A')}°C
- Humidity: {city_data.get('weather', {}).get('humidity_percent', 'N/A')}%
- Wind Speed: {city_data.get('weather', {}).get('wind_speed_mps', 'N/A')} m/s

KEY POLLUTANTS (μg/m³):
- PM2.5: {city_data.get('air_quality', {}).get('pollutants', {}).get('pm2_5', 'N/A')}
- PM10: {city_data.get('air_quality', {}).get('pollutants', {}).get('pm10', 'N/A')}
- NO2: {city_data.get('air_quality', {}).get('pollutants', {}).get('no2', 'N/A')}
- SO2: {city_data.get('air_quality', {}).get('pollutants', {}).get('so2', 'N/A')}
- O3: {city_data.get('air_quality', {}).get('pollutants', {}).get('o3', 'N/A')}

HISTORICAL TREND:
{self._format_historical_data(historical_data)}

TASK: Predict the top 5 most effective environmental interventions to improve air quality and reduce pollution.

For each intervention, provide:
1. **Intervention Name** (e.g., "Increase Urban Green Spaces")
2. **Description** (2-3 sentences explaining the intervention)
3. **Expected Impact** (percentage reduction in key pollutant or AQI improvement)
4. **Implementation Timeline** (short-term: <6 months, medium-term: 6-18 months, long-term: >18 months)
5. **Priority Level** (High/Medium/Low based on current conditions)
6. **Confidence Score** (0-100, your confidence in this prediction)

Format your response as a JSON array of interventions. Be specific and data-driven."""

        return prompt
    
    def _format_historical_data(self, historical_data: List[Dict[str, Any]]) -> str:
        """Format historical data for prompt"""
        if not historical_data or len(historical_data) == 0:
            return "No historical data available (first analysis)."
        
        formatted = []
        for i, data in enumerate(historical_data[-3:]):  # Last 3 records
            formatted.append(f"Record {i+1}: AQI={data.get('aqi', 'N/A')}, Score={data.get('env_score', 'N/A')}")
        
        return "\n".join(formatted)
    
    def _parse_gemini_response(self, response_text: str, city_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Gemini's response into structured predictions
        Handles both JSON and natural language responses
        """
        try:
            # Try to extract JSON from response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "[" in response_text and "]" in response_text:
                start = response_text.index("[")
                end = response_text.rindex("]") + 1
                json_str = response_text[start:end]
            else:
                json_str = response_text
            
            interventions = json.loads(json_str)
            
            # Calculate average confidence
            confidences = [i.get("confidence_score", 50) for i in interventions if isinstance(i, dict)]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 50
            
            return {
                "success": True,
                "city": city_data.get("city"),
                "current_aqi": city_data.get("air_quality", {}).get("aqi"),
                "interventions": interventions,
                "average_confidence": round(avg_confidence, 1),
                "prediction_id": self.predictions_made + 1,
                "model_used": Settings.GEMINI_MODEL
            }
            
        except Exception as e:
            eco_logger.log_error(
                self.name,
                e,
                {"parsing_error": "Failed to parse Gemini response", "response_length": len(response_text)}
            )
            return self._fallback_prediction(city_data)
    
    def _evaluate_prediction(self, predictions: Dict[str, Any], city_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agent self-evaluation: Assess prediction quality
        Demonstrates agent evaluation capability
        """
        evaluation = {
            "quality_score": 0.0,
            "completeness": False,
            "data_coverage": False,
            "actionability": False,
            "issues": []
        }
        
        interventions = predictions.get("interventions", [])
        
        # Check completeness (should have 5 interventions)
        if len(interventions) >= 5:
            evaluation["completeness"] = True
            evaluation["quality_score"] += 25
        else:
            evaluation["issues"].append(f"Only {len(interventions)} interventions provided (expected 5)")
        
        # Check data coverage (interventions should address key pollutants)
        required_fields = ["name", "description", "expected_impact", "priority_level"]
        complete_interventions = sum(
            1 for i in interventions
            if all(field in i for field in required_fields)
        )
        
        if complete_interventions == len(interventions):
            evaluation["data_coverage"] = True
            evaluation["quality_score"] += 25
        else:
            evaluation["issues"].append(f"Some interventions missing required fields")
        
        # Check actionability (confidence scores should be reasonable)
        if predictions.get("average_confidence", 0) >= 60:
            evaluation["actionability"] = True
            evaluation["quality_score"] += 25
        else:
            evaluation["issues"].append("Low confidence scores indicate uncertain predictions")
        
        # Relevance to current conditions
        current_aqi = city_data.get("air_quality", {}).get("aqi", 0)
        if current_aqi >= 4:  # Poor air quality
            high_priority = sum(1 for i in interventions if i.get("priority_level") == "High")
            if high_priority >= 3:
                evaluation["quality_score"] += 25
            else:
                evaluation["issues"].append("Insufficient high-priority interventions for poor AQI")
        else:
            evaluation["quality_score"] += 25
        
        # Record evaluation metric
        self.prediction_accuracy.append(evaluation["quality_score"])
        eco_logger.record_metric("prediction_accuracy", evaluation["quality_score"])
        
        return evaluation
    
    def _fallback_prediction(self, city_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback predictions when Gemini fails
        Rule-based system as backup
        """
        aqi = city_data.get("air_quality", {}).get("aqi", 3)
        
        interventions = [
            {
                "name": "Increase Urban Green Spaces",
                "description": "Plant trees and create parks to absorb CO2 and filter air pollutants.",
                "expected_impact": "10-15% reduction in PM2.5 over 12 months",
                "implementation_timeline": "medium-term",
                "priority_level": "High" if aqi >= 4 else "Medium",
                "confidence_score": 75
            },
            {
                "name": "Promote Public Transportation",
                "description": "Expand public transit to reduce vehicle emissions.",
                "expected_impact": "8-12% reduction in NO2",
                "implementation_timeline": "long-term",
                "priority_level": "High",
                "confidence_score": 70
            },
            {
                "name": "Industrial Emission Controls",
                "description": "Implement stricter regulations on industrial emissions.",
                "expected_impact": "15-20% reduction in SO2 and particulates",
                "implementation_timeline": "medium-term",
                "priority_level": "High" if aqi >= 3 else "Medium",
                "confidence_score": 65
            },
            {
                "name": "Electric Vehicle Incentives",
                "description": "Provide subsidies and infrastructure for electric vehicles to reduce tailpipe emissions.",
                "expected_impact": "12-18% reduction in NO2 and CO",
                "implementation_timeline": "long-term",
                "priority_level": "Medium",
                "confidence_score": 68
            },
            {
                "name": "Air Quality Monitoring Network",
                "description": "Deploy comprehensive sensor network for real-time pollution tracking and early warning.",
                "expected_impact": "Enable 25% faster response to pollution events",
                "implementation_timeline": "short-term",
                "priority_level": "High",
                "confidence_score": 80
            }
        ]
        
        return {
            "success": True,
            "fallback": True,
            "city": city_data.get("city"),
            "current_aqi": aqi,
            "interventions": interventions,
            "average_confidence": 71.6,
            "model_used": "Rule-based fallback"
        }
    
    def _get_historical_context(self, city: str) -> List[Dict[str, Any]]:
        """Retrieve historical data from memory bank"""
        historical = memory_bank.search(
            "city_profiles",
            filter_fn=lambda data: data.get("city") == city
        )
        return historical[:5]  # Last 5 records
    
    def get_evaluation_metrics(self) -> Dict[str, Any]:
        """
        Get agent's self-evaluation metrics
        Demonstrates agent evaluation reporting
        """
        if not self.prediction_accuracy:
            return {
                "predictions_made": 0,
                "average_quality_score": 0,
                "status": "No predictions made yet"
            }
        
        return {
            "predictions_made": self.predictions_made,
            "average_quality_score": round(sum(self.prediction_accuracy) / len(self.prediction_accuracy), 2),
            "min_quality": min(self.prediction_accuracy),
            "max_quality": max(self.prediction_accuracy),
            "recent_scores": self.prediction_accuracy[-5:]
        }

# Global instance
pollution_predictor_agent = PollutionPredictorAgent()