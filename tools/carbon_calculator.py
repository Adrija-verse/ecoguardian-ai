"""
EcoGuardian AI - Carbon Calculator Tool (Custom MCP Tool)
Calculates carbon emissions and offsets for various activities
"""

from typing import Dict, Any
from observability.logger import eco_logger

class CarbonCalculator:
    """
    Custom MCP Tool: Calculates carbon footprint for urban activities
    This demonstrates building a custom tool that agents can invoke
    """
    
    # Emission factors (kg CO2 per unit)
    EMISSION_FACTORS = {
        # Transportation (per km)
        "car": 0.171,
        "bus": 0.089,
        "train": 0.041,
        "plane": 0.255,
        "bike": 0.0,
        "walk": 0.0,
        
        # Energy (per kWh)
        "electricity": 0.475,
        "natural_gas": 0.184,
        
        # Food (per kg)
        "beef": 27.0,
        "chicken": 6.9,
        "fish": 6.1,
        "vegetables": 2.0,
        "dairy": 1.9,
        
        # Waste (per kg)
        "landfill": 0.5,
        "recycling": 0.1,
        "compost": 0.05
    }
    
    # Offset factors
    OFFSET_FACTORS = {
        "tree_planting": 22.0,  # kg CO2 absorbed per tree per year
        "solar_panel": 1000.0,  # kg CO2 avoided per year per kW installed
        "renewable_energy": 0.475  # kg CO2 per kWh avoided
    }
    
    def __init__(self):
        self.name = "CarbonCalculator"
        eco_logger.log_agent_action(
            self.name,
            "INITIALIZED",
            {"emission_categories": len(self.EMISSION_FACTORS)}
        )
    
    def calculate_emissions(
        self,
        activity_type: str,
        category: str,
        amount: float,
        unit: str = "default"
    ) -> Dict[str, Any]:
        """
        Calculate carbon emissions for a specific activity
        
        Args:
            activity_type: Type of activity (transport, energy, food, waste)
            category: Specific category (e.g., 'car', 'electricity')
            amount: Quantity (e.g., km traveled, kWh used)
            unit: Unit of measurement
        
        Returns:
            Dictionary with emissions data
        """
        try:
            # Get emission factor
            category_lower = category.lower()
            if category_lower not in self.EMISSION_FACTORS:
                eco_logger.log_error(
                    self.name,
                    ValueError(f"Unknown category: {category}"),
                    {"activity_type": activity_type}
                )
                return self._error_response(f"Unknown category: {category}")
            
            factor = self.EMISSION_FACTORS[category_lower]
            emissions = amount * factor
            
            # Calculate equivalents for context
            equivalents = self._calculate_equivalents(emissions)
            
            result = {
                "success": True,
                "activity_type": activity_type,
                "category": category,
                "amount": amount,
                "unit": unit if unit != "default" else self._get_default_unit(category_lower),
                "emissions_kg_co2": round(emissions, 2),
                "equivalents": equivalents,
                "offset_recommendations": self._recommend_offsets(emissions)
            }
            
            eco_logger.log_tool_usage(
                self.name,
                input_data={"category": category, "amount": amount},
                output_data={"emissions": emissions}
            )
            
            return result
            
        except Exception as e:
            eco_logger.log_error(self.name, e, {"category": category, "amount": amount})
            return self._error_response(str(e))
    
    def calculate_total_footprint(self, activities: list) -> Dict[str, Any]:
        """
        Calculate total carbon footprint from multiple activities
        
        Args:
            activities: List of dicts with {activity_type, category, amount}
        
        Returns:
            Aggregated emissions data
        """
        total_emissions = 0.0
        breakdown = {}
        
        for activity in activities:
            result = self.calculate_emissions(
                activity.get("activity_type", "general"),
                activity["category"],
                activity["amount"]
            )
            
            if result["success"]:
                emissions = result["emissions_kg_co2"]
                total_emissions += emissions
                
                activity_type = result["activity_type"]
                if activity_type not in breakdown:
                    breakdown[activity_type] = 0.0
                breakdown[activity_type] += emissions
        
        return {
            "success": True,
            "total_emissions_kg_co2": round(total_emissions, 2),
            "breakdown_by_type": {k: round(v, 2) for k, v in breakdown.items()},
            "equivalents": self._calculate_equivalents(total_emissions),
            "offset_recommendations": self._recommend_offsets(total_emissions)
        }
    
    def calculate_offset_impact(self, offset_type: str, quantity: float) -> Dict[str, Any]:
        """
        Calculate CO2 reduction from offset actions
        
        Args:
            offset_type: Type of offset (e.g., 'tree_planting')
            quantity: Number of units (e.g., number of trees)
        
        Returns:
            Offset impact data
        """
        if offset_type not in self.OFFSET_FACTORS:
            return self._error_response(f"Unknown offset type: {offset_type}")
        
        factor = self.OFFSET_FACTORS[offset_type]
        co2_reduced = quantity * factor
        
        return {
            "success": True,
            "offset_type": offset_type,
            "quantity": quantity,
            "co2_reduced_kg": round(co2_reduced, 2),
            "co2_reduced_tons": round(co2_reduced / 1000, 2),
            "equivalents": self._calculate_equivalents(co2_reduced, is_offset=True)
        }
    
    def _calculate_equivalents(self, co2_kg: float, is_offset: bool = False) -> Dict[str, float]:
        """Calculate relatable equivalents for CO2 amount"""
        prefix = "equivalent_to" if not is_offset else "offsets"
        
        return {
            f"{prefix}_tree_years": round(co2_kg / 22, 1),  # Trees needed for 1 year
            f"{prefix}_car_km": round(co2_kg / 0.171, 0),  # Km driven
            f"{prefix}_flights_short": round(co2_kg / 90, 1)  # Short flights (350km)
        }
    
    def _recommend_offsets(self, emissions_kg: float) -> Dict[str, Any]:
        """Recommend offset actions based on emissions"""
        return {
            "trees_to_plant": round(emissions_kg / 22),
            "solar_kw_needed": round(emissions_kg / 1000, 2),
            "renewable_kwh_needed": round(emissions_kg / 0.475, 0)
        }
    
    def _get_default_unit(self, category: str) -> str:
        """Get default unit for category"""
        if category in ["car", "bus", "train", "plane", "bike", "walk"]:
            return "km"
        elif category in ["electricity", "natural_gas"]:
            return "kWh"
        elif category in ["beef", "chicken", "fish", "vegetables", "dairy"]:
            return "kg"
        elif category in ["landfill", "recycling", "compost"]:
            return "kg"
        return "units"
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """Standard error response"""
        return {
            "success": False,
            "error": message,
            "emissions_kg_co2": 0.0
        }
    
    def get_available_categories(self) -> Dict[str, list]:
        """List all available emission categories"""
        categories = {
            "transportation": [],
            "energy": [],
            "food": [],
            "waste": []
        }
        
        for category in self.EMISSION_FACTORS.keys():
            if category in ["car", "bus", "train", "plane", "bike", "walk"]:
                categories["transportation"].append(category)
            elif category in ["electricity", "natural_gas"]:
                categories["energy"].append(category)
            elif category in ["beef", "chicken", "fish", "vegetables", "dairy"]:
                categories["food"].append(category)
            elif category in ["landfill", "recycling", "compost"]:
                categories["waste"].append(category)
        
        return categories

# Global instance
carbon_calculator = CarbonCalculator()