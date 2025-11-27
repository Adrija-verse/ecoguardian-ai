"""
Action Deployer Agent - EcoGuardian AI
Deploys eco-interventions based on predictions and simulates their impact.
Handles automated deployment actions like tree planting recommendations,
emission reduction strategies, and green infrastructure suggestions.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

# Configure logging
logger = logging.getLogger(__name__)


class ActionDeployerAgent:
    """
    Autonomous agent responsible for deploying eco-interventions.
    Translates predictions into actionable deployment strategies.
    
    AGENT PATTERN: Sequential execution of deployment actions
    Each action is deployed based on AI predictions and environmental data
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Action Deployer Agent.
        
        Args:
            config: Configuration dictionary with deployment parameters
        """
        self.config = config or {}
        self.deployment_history = []
        
        # Map of action types to their deployment methods
        self.action_types = {
            "tree_planting": self._deploy_tree_planting,
            "emission_reduction": self._deploy_emission_reduction,
            "green_infrastructure": self._deploy_green_infrastructure,
            "air_quality_improvement": self._deploy_air_quality_improvement,
            "carbon_offset": self._deploy_carbon_offset
        }
        logger.info("ActionDeployerAgent initialized successfully")
    
    async def deploy_actions(self, predictions: Dict[str, Any], location: str) -> Dict[str, Any]:
        """
        Deploy multiple eco-actions based on predictions.
        
        WORKFLOW:
        1. Extract recommendations from AI predictions
        2. Deploy each action sequentially
        3. Calculate aggregate environmental impact
        4. Store in deployment history for agent evaluation
        
        Args:
            predictions: Dictionary containing pollution predictions and recommendations
            location: Target location for deployment
            
        Returns:
            Dictionary with deployment results and impact metrics
        """
        logger.info(f"Starting action deployment for location: {location}")
        
        deployment_results = {
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "actions_deployed": [],
            "estimated_impact": {},
            "status": "in_progress"
        }
        
        try:
            # Extract action recommendations from AI predictions
            recommended_actions = self._extract_recommendations(predictions)
            
            # Deploy each recommended action (SEQUENTIAL PATTERN)
            for action in recommended_actions:
                action_type = action.get("type")
                action_params = action.get("parameters", {})
                
                if action_type in self.action_types:
                    logger.info(f"Deploying action: {action_type}")
                    result = await self.action_types[action_type](
                        location, 
                        action_params, 
                        predictions
                    )
                    deployment_results["actions_deployed"].append(result)
                else:
                    logger.warning(f"Unknown action type: {action_type}")
            
            # Calculate aggregate impact across all deployed actions
            deployment_results["estimated_impact"] = self._calculate_aggregate_impact(
                deployment_results["actions_deployed"]
            )
            deployment_results["status"] = "completed"
            
            # Store in deployment history (used for AGENT EVALUATION)
            self.deployment_history.append(deployment_results)
            
            logger.info(f"Deployment completed. {len(deployment_results['actions_deployed'])} actions deployed")
            
        except Exception as e:
            logger.error(f"Deployment failed: {str(e)}")
            deployment_results["status"] = "failed"
            deployment_results["error"] = str(e)
        
        return deployment_results
    
    def _extract_recommendations(self, predictions: Dict[str, Any]) -> List[Dict]:
        """
        Extract actionable recommendations from prediction data.
        
        INTELLIGENCE: Maps AI predictions to concrete deployment actions
        Considers current AQI, pollution levels, and intervention priorities
        """
        recommendations = []
        
        # Get current environmental state
        current_aqi = predictions.get("current_aqi", 0)
        interventions = predictions.get("interventions", [])
        
        # STRATEGY 1: Use AI-generated interventions if available
        if interventions:
            for intervention in interventions[:5]:  # Top 5 interventions
                priority = intervention.get("priority_level", "Medium")
                intervention_name = intervention.get("name", "").lower()
                
                # Map AI intervention to action type
                if "tree" in intervention_name or "green space" in intervention_name:
                    recommendations.append({
                        "type": "tree_planting",
                        "parameters": {
                            "tree_count": 1000 if priority == "High" else 500,
                            "species": "native"
                        }
                    })
                elif "traffic" in intervention_name or "emission" in intervention_name:
                    recommendations.append({
                        "type": "emission_reduction",
                        "parameters": {
                            "target_reduction_percent": 30 if priority == "High" else 20
                        }
                    })
                elif "infrastructure" in intervention_name:
                    recommendations.append({
                        "type": "green_infrastructure",
                        "parameters": {"hotspot_count": 3 if priority == "High" else 1}
                    })
                elif "air quality" in intervention_name or "pollution" in intervention_name:
                    recommendations.append({
                        "type": "air_quality_improvement",
                        "parameters": {
                            "urgency": "high" if priority == "High" else "medium",
                            "target_reduction": 30
                        }
                    })
        
        # STRATEGY 2: Fallback rule-based recommendations based on AQI
        if not recommendations and current_aqi > 0:
            if current_aqi >= 4:  # Poor or Very Poor
                recommendations.extend([
                    {
                        "type": "air_quality_improvement",
                        "parameters": {"urgency": "high", "target_reduction": 30}
                    },
                    {
                        "type": "tree_planting",
                        "parameters": {"tree_count": 1000, "species": "native"}
                    },
                    {
                        "type": "emission_reduction",
                        "parameters": {"target_reduction_percent": 25}
                    }
                ])
            elif current_aqi >= 3:  # Moderate
                recommendations.extend([
                    {
                        "type": "tree_planting",
                        "parameters": {"tree_count": 500, "species": "native"}
                    },
                    {
                        "type": "green_infrastructure",
                        "parameters": {"hotspot_count": 2}
                    }
                ])
        
        # Always include carbon monitoring
        recommendations.append({
            "type": "carbon_offset",
            "parameters": {"monitoring_duration": "30_days"}
        })
        
        return recommendations
    
    async def _deploy_tree_planting(self, location: str, params: Dict, predictions: Dict) -> Dict:
        """
        Deploy tree planting intervention.
        
        IMPACT: Trees absorb CO2 and improve air quality
        Each tree absorbs approximately 21kg CO2 per year
        """
        tree_count = params.get("tree_count", 100)
        species = params.get("species", "native")
        
        # Simulate API call to city planning department
        await asyncio.sleep(0.1)
        
        # Calculate environmental impact
        co2_reduction_per_year = tree_count * 21  # kg CO2 per tree per year
        aqi_improvement = tree_count * 0.02  # 0.02% AQI improvement per tree
        
        return {
            "action_type": "tree_planting",
            "status": "deployed",
            "details": {
                "tree_count": tree_count,
                "species": species,
                "planting_zones": self._identify_planting_zones(location, predictions),
                "estimated_cost_usd": tree_count * 50  # $50 per tree
            },
            "impact": {
                "co2_reduction_kg_per_year": co2_reduction_per_year,
                "air_quality_improvement_percent": round(aqi_improvement, 2),
                "oxygen_production_kg_per_year": tree_count * 118  # kg O2 per tree per year
            }
        }
    
    async def _deploy_emission_reduction(self, location: str, params: Dict, predictions: Dict) -> Dict:
        """
        Deploy emission reduction strategies.
        
        STRATEGIES: Traffic optimization, industrial monitoring, public transport
        """
        target_reduction = params.get("target_reduction_percent", 20)
        
        await asyncio.sleep(0.1)
        
        strategies = [
            "Traffic flow optimization with AI-powered signals",
            "Real-time industrial emission monitoring",
            "Public transport incentives and subsidies",
            "Electric vehicle charging infrastructure"
        ]
        
        # Calculate impact based on typical city emissions
        estimated_co2_reduction = target_reduction * 50  # kg per percent reduction
        
        return {
            "action_type": "emission_reduction",
            "status": "deployed",
            "details": {
                "target_reduction_percent": target_reduction,
                "strategies": strategies,
                "implementation_timeline": "6_months",
                "monitoring_frequency": "daily"
            },
            "impact": {
                "co2_reduction_kg_per_year": estimated_co2_reduction,
                "estimated_nox_reduction_percent": target_reduction * 0.8,
                "estimated_pm25_reduction_percent": target_reduction * 0.7
            }
        }
    
    async def _deploy_green_infrastructure(self, location: str, params: Dict, predictions: Dict) -> Dict:
        """
        Deploy green infrastructure projects.
        
        INFRASTRUCTURE: Green roofs, vertical gardens, urban parks, bioswales
        """
        hotspot_count = params.get("hotspot_count", 1)
        
        await asyncio.sleep(0.1)
        
        infrastructure_types = [
            "Green roofs (vegetated roof systems)",
            "Vertical gardens (living walls)",
            "Urban parks and green corridors",
            "Bioswales (vegetated drainage channels)"
        ]
        
        # Calculate impact
        coverage_area = hotspot_count * 5000  # 5000 sqm per hotspot
        temp_reduction = hotspot_count * 1.5  # Celsius
        
        return {
            "action_type": "green_infrastructure",
            "status": "deployed",
            "details": {
                "infrastructure_types": infrastructure_types[:hotspot_count + 1],
                "coverage_area_sqm": coverage_area,
                "target_hotspots": hotspot_count
            },
            "impact": {
                "temperature_reduction_celsius": round(temp_reduction, 2),
                "stormwater_management_improvement_percent": 35,
                "urban_heat_island_mitigation_percent": 25
            }
        }
    
    async def _deploy_air_quality_improvement(self, location: str, params: Dict, predictions: Dict) -> Dict:
        """
        Deploy air quality improvement measures.
        
        URGENCY-BASED: High urgency triggers immediate interventions
        """
        urgency = params.get("urgency", "medium")
        target_reduction = params.get("target_reduction", 20)
        
        await asyncio.sleep(0.1)
        
        measures = {
            "high": [
                "Immediate traffic restrictions in city center",
                "Industrial shutdown protocols for high-emission facilities",
                "Emergency air purifier deployment in public spaces"
            ],
            "medium": [
                "Dynamic traffic management based on pollution levels",
                "Continuous emission monitoring with alerts",
                "Public awareness campaigns and health advisories"
            ],
            "low": [
                "Gradual infrastructure improvements",
                "Long-term urban planning initiatives"
            ]
        }
        
        return {
            "action_type": "air_quality_improvement",
            "status": "deployed",
            "details": {
                "urgency": urgency,
                "measures": measures.get(urgency, measures["medium"]),
                "target_aqi_reduction": target_reduction,
                "deployment_speed": "immediate" if urgency == "high" else "gradual"
            },
            "impact": {
                "expected_aqi_improvement": target_reduction,
                "health_impact_reduction_percent": round(target_reduction * 1.2, 2),
                "hospital_admissions_reduction_percent": round(target_reduction * 0.8, 2)
            }
        }
    
    async def _deploy_carbon_offset(self, location: str, params: Dict, predictions: Dict) -> Dict:
        """
        Deploy carbon offset monitoring and tracking.
        
        MONITORING: Continuous tracking of CO2, CH4, and N2O emissions
        """
        monitoring_duration = params.get("monitoring_duration", "30_days")
        
        await asyncio.sleep(0.1)
        
        return {
            "action_type": "carbon_offset",
            "status": "deployed",
            "details": {
                "monitoring_duration": monitoring_duration,
                "tracking_metrics": ["CO2", "CH4", "N2O"],
                "reporting_frequency": "daily",
                "sensor_network_size": 50
            },
            "impact": {
                "baseline_emissions_kg": predictions.get("current_emissions", 1000),
                "monitoring_accuracy_percent": 95,
                "data_granularity": "15_minute_intervals"
            }
        }
    
    def _identify_planting_zones(self, location: str, predictions: Dict) -> List[str]:
        """
        Identify optimal zones for tree planting based on predictions.
        
        STRATEGY: Prioritize high-pollution hotspots
        """
        zones = []
        
        # Try to get hotspots from predictions
        hotspots = predictions.get("hotspots", [])
        if hotspots:
            for i, hotspot in enumerate(hotspots[:5]):
                zones.append(f"Zone_{i+1}_{location}_hotspot")
        
        # Fallback to general zones
        if not zones:
            zones = [
                f"{location}_CityCenter",
                f"{location}_IndustrialArea",
                f"{location}_ResidentialZone"
            ]
        
        return zones
    
    def _calculate_aggregate_impact(self, deployed_actions: List[Dict]) -> Dict:
        """
        Calculate the aggregate impact of all deployed actions.
        
        AGGREGATION: Sums up environmental benefits across all interventions
        Used for reporting and AGENT EVALUATION
        """
        total_co2_reduction = 0
        total_aqi_improvement = 0
        total_temperature_reduction = 0
        
        for action in deployed_actions:
            impact = action.get("impact", {})
            
            # Accumulate CO2 reductions
            total_co2_reduction += impact.get("co2_reduction_kg_per_year", 0)
            
            # Accumulate AQI improvements
            total_aqi_improvement += impact.get("air_quality_improvement_percent", 0)
            total_aqi_improvement += impact.get("expected_aqi_improvement", 0)
            
            # Accumulate temperature reductions
            total_temperature_reduction += impact.get("temperature_reduction_celsius", 0)
        
        # Calculate overall environmental benefit score
        # Score = (AQI improvement + temp reduction * 10) / 2
        overall_score = (total_aqi_improvement + total_temperature_reduction * 10) / 2 if (total_aqi_improvement + total_temperature_reduction) > 0 else 0
        
        return {
            "total_co2_reduction_kg_per_year": round(total_co2_reduction, 2),
            "total_aqi_improvement_percent": round(total_aqi_improvement, 2),
            "total_temperature_reduction_celsius": round(total_temperature_reduction, 2),
            "overall_environmental_score": round(overall_score, 2),
            "equivalent_trees_planted": round(total_co2_reduction / 21, 0) if total_co2_reduction > 0 else 0
        }
    
    def get_deployment_history(self, limit: int = 10) -> List[Dict]:
        """
        Retrieve recent deployment history.
        
        OBSERVABILITY: Provides transparency into past deployments
        """
        return self.deployment_history[-limit:]
    
    def evaluate_deployment_success(self, deployment_id: Optional[str] = None) -> Dict:
        """
        Evaluate the success of deployments.
        
        AGENT EVALUATION REQUIREMENT: Self-assessment of deployment performance
        Tracks success rate, average actions per deployment, and overall effectiveness
        """
        if not self.deployment_history:
            return {
                "status": "no_deployments",
                "success_rate": 0,
                "message": "No deployments have been executed yet"
            }
        
        # Count successful deployments
        successful_deployments = sum(
            1 for d in self.deployment_history 
            if d.get("status") == "completed"
        )
        
        total_deployments = len(self.deployment_history)
        success_rate = (successful_deployments / total_deployments) * 100
        
        # Calculate average actions per deployment
        total_actions = sum(
            len(d.get("actions_deployed", [])) 
            for d in self.deployment_history
        )
        avg_actions = total_actions / total_deployments if total_deployments > 0 else 0
        
        # Calculate total environmental impact
        total_co2_saved = sum(
            d.get("estimated_impact", {}).get("total_co2_reduction_kg_per_year", 0)
            for d in self.deployment_history
        )
        
        return {
            "total_deployments": total_deployments,
            "successful_deployments": successful_deployments,
            "failed_deployments": total_deployments - successful_deployments,
            "success_rate_percent": round(success_rate, 2),
            "average_actions_per_deployment": round(avg_actions, 2),
            "total_co2_reduction_kg_per_year": round(total_co2_saved, 2),
            "evaluation_status": "excellent" if success_rate >= 95 else "good" if success_rate >= 80 else "needs_improvement",
            "recommendation": "System is performing optimally" if success_rate >= 95 else "Consider reviewing failed deployments"
        }