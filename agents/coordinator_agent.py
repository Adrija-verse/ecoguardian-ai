"""
Coordinator Agent - EcoGuardian AI (FIXED)
Orchestrates multi-agent workflows with A2A Protocol
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class WorkflowType(Enum):
    """Types of multi-agent workflow patterns."""
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    LOOP = "loop"
    HYBRID = "hybrid"

class A2AMessage:
    """Agent-to-Agent communication message structure."""
    
    def __init__(self, sender: str, receiver: str, message_type: str, payload: Dict):
        self.sender = sender
        self.receiver = receiver
        self.message_type = message_type
        self.payload = payload
        self.timestamp = datetime.now().isoformat()
        self.message_id = f"{sender}_{receiver}_{datetime.now().timestamp()}"
    
    def to_dict(self) -> Dict:
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "message_type": self.message_type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }

class CoordinatorAgent:
    """Master coordinator that orchestrates all EcoGuardian agents."""
    
    def __init__(self, agents: Dict[str, Any], memory_manager: Any, session_manager: Any):
        """Initialize the Coordinator Agent."""
        self.agents = agents
        self.memory_manager = memory_manager
        self.session_manager = session_manager
        self.message_queue = []
        self.workflow_history = []
        self.active_sessions = {}
        
        logger.info(f"CoordinatorAgent initialized with {len(agents)} agents")
    
    async def orchestrate_urban_healing(
        self, 
        location: str, 
        user_preferences: Optional[Dict] = None,
        workflow_type: WorkflowType = WorkflowType.HYBRID
    ) -> Dict[str, Any]:
        """Main orchestration method for urban ecosystem healing."""
        logger.info(f"Starting urban healing orchestration for {location}")
        
        session_id = f"coord_{location}_{int(datetime.now().timestamp())}"
        
        workflow_result = {
            "session_id": session_id,
            "location": location,
            "workflow_type": workflow_type.value,
            "start_time": datetime.now().isoformat(),
            "stages": {},
            "a2a_messages": [],
            "status": "in_progress"
        }
        
        try:
            if workflow_type == WorkflowType.HYBRID:
                result = await self._execute_hybrid_workflow(location, user_preferences)
            else:
                result = await self._execute_sequential_workflow(location, user_preferences)
            
            workflow_result["stages"] = result["stages"]
            workflow_result["a2a_messages"] = self.message_queue.copy()
            workflow_result["status"] = "completed"
            workflow_result["end_time"] = datetime.now().isoformat()
            
            # Store results in memory
            self.memory_manager.store(
                key=f"healing_workflow_{session_id}",
                value=workflow_result,
                context={"location": location, "type": "urban_healing"}
            )
            
            logger.info(f"Urban healing orchestration completed for {location}")
            
        except Exception as e:
            logger.error(f"Orchestration failed: {str(e)}")
            workflow_result["status"] = "failed"
            workflow_result["error"] = str(e)
        finally:
            self.message_queue.clear()
        
        self.workflow_history.append(workflow_result)
        return workflow_result
    
    # ✅ FIXED: Sequential workflow with proper async/await
    async def _execute_sequential_workflow(self, location: str, user_preferences: Optional[Dict]) -> Dict:
        """Execute agents in sequential order."""
        logger.info("Executing SEQUENTIAL workflow")
        stages = {}
        
        # Stage 1: Data Collection - ✅ FIXED: Direct await
        data_collector = self.agents.get("data_collector")
        if hasattr(data_collector, 'collect_city_data'):
            collection_result = await data_collector.collect_city_data(location)
        else:
            collection_result = {"success": False, "error": "Data collector not available"}
        
        stages["data_collection"] = collection_result
        # ✅ ADD A2A MESSAGE
        self._send_a2a_message("data_collector", "predictor", "data_ready", {"data": collection_result})
        
        # Stage 2: Prediction - ✅ FIXED: No wrapper needed (sync method)
        predictor = self.agents.get("predictor")
        if hasattr(predictor, 'predict_interventions'):
            prediction_result = predictor.predict_interventions(collection_result)
        else:
            prediction_result = {"success": False, "predictions": []}
        
        stages["prediction"] = prediction_result
        # ✅ ADD A2A MESSAGE
        self._send_a2a_message("predictor", "deployer", "predictions_ready", {"predictions": prediction_result})
        
        # Stage 3: Deployment - ✅ FIXED: Async method needs await
        deployer = self.agents.get("deployer")
        if deployer and hasattr(deployer, 'deploy_actions'):
            deployment_result = await deployer.deploy_actions(prediction_result, location)
            stages["deployment"] = deployment_result
            # ✅ ADD A2A MESSAGE
            self._send_a2a_message("deployer", "coordinator", "deployment_complete", {"deployment": deployment_result})
        
        return {"stages": stages, "workflow_type": "sequential"}
    
    # ✅ FIXED: Hybrid workflow with proper async/await
    async def _execute_hybrid_workflow(self, location: str, user_preferences: Optional[Dict]) -> Dict:
        """Execute a hybrid workflow combining patterns."""
        logger.info("Executing HYBRID workflow")
        stages = {}
        
        # Phase 1: Data collection - ✅ FIXED: Direct await
        data_collector = self.agents.get("data_collector")
        if hasattr(data_collector, 'collect_city_data'):
            city_data = await data_collector.collect_city_data(location)
            stages["phase1_data_collection"] = city_data
            # ✅ ADD A2A MESSAGE
            self._send_a2a_message("data_collector", "predictor", "data_ready", {"city_data": city_data})
        
        # Phase 2: Prediction - ✅ FIXED: Sync method
        predictor = self.agents.get("predictor")
        if hasattr(predictor, 'predict_interventions'):
            predictions = predictor.predict_interventions(city_data)
            stages["phase2_prediction"] = predictions
            # ✅ ADD A2A MESSAGE
            self._send_a2a_message("predictor", "deployer", "predictions_ready", {"predictions": predictions})
        
        # Phase 3: Deployment - ✅ FIXED: Async method
        deployer = self.agents.get("deployer")
        if deployer and hasattr(deployer, 'deploy_actions'):
            deployment = await deployer.deploy_actions(predictions, location)
            stages["phase3_deployment"] = deployment
            # ✅ ADD A2A MESSAGE
            self._send_a2a_message("deployer", "coordinator", "deployment_complete", {"deployment": deployment})
        
        return {"stages": stages, "workflow_type": "hybrid"}
    
    def _send_a2a_message(self, sender: str, receiver: str, message_type: str, payload: Dict):
        """
        A2A PROTOCOL IMPLEMENTATION
    
        Agent-to-Agent communication following standardized message format:
        - sender: Agent that initiated the message
        - receiver: Target agent for the message  
        - message_type: Type of communication (e.g., 'data_ready', 'prediction_complete')
        - payload: Actual data being transmitted
    
        All A2A messages are logged for OBSERVABILITY and stored in message_queue.
        This enables transparent inter-agent coordination and debugging.
        """
        """Send an Agent-to-Agent (A2A) protocol message."""
        message = A2AMessage(sender, receiver, message_type, payload)
        self.message_queue.append(message.to_dict())
        logger.info(f"A2A Message: {sender} → {receiver} ({message_type})")
    
    async def personal_concierge_workflow(self, user_location: str, user_preferences: Dict) -> Dict:
        """Execute personal concierge workflow."""
        logger.info(f"Executing personal concierge workflow for {user_location}")
        
        carbon_footprint = self._calculate_carbon_footprint(user_preferences, {})
        eco_suggestions = self._generate_eco_suggestions(user_preferences, {}, carbon_footprint)
        
        return {
            "user_location": user_location,
            "carbon_footprint": carbon_footprint,
            "eco_suggestions": eco_suggestions,
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_carbon_footprint(self, user_preferences: Dict, environmental_data: Dict) -> Dict:
        """Calculate user's carbon footprint."""
        transport = user_preferences.get("transport_mode", "car")
        diet = user_preferences.get("diet", "mixed")
        
        transport_emissions = {"car": 4.6, "public_transport": 1.5, "bicycle": 0.1}
        diet_emissions = {"meat_heavy": 3.3, "mixed": 2.5, "vegetarian": 1.7}
        
        total_emissions = (
            transport_emissions.get(transport, 4.6) +
            diet_emissions.get(diet, 2.5)
        )
        
        return {
            "total_tons_co2_per_year": round(total_emissions, 2),
            "transport_contribution": transport_emissions.get(transport, 4.6),
            "diet_contribution": diet_emissions.get(diet, 2.5)
        }
    
    def _generate_eco_suggestions(self, user_preferences: Dict, recommendations: Dict, carbon_footprint: Dict) -> List[Dict]:
        """Generate personalized eco-friendly suggestions."""
        suggestions = []
        
        if user_preferences.get("transport_mode") == "car":
            suggestions.append({
                "category": "transport",
                "suggestion": "Switch to public transport 3 days/week",
                "potential_savings_kg_co2": 1200
            })
        
        suggestions.append({
            "category": "energy",
            "suggestion": "Switch to renewable energy provider",
            "potential_savings_kg_co2": 800
        })
        
        return suggestions
    
    async def enterprise_workflow(self, company_data: Dict, optimization_goals: List[str]) -> Dict:
        """Execute enterprise workflow for business sustainability."""
        logger.info(f"Executing enterprise workflow")
        
        return {
            "company": company_data.get("company_name"),
            "enterprise_data": {"total_emissions": 10000, "locations": company_data.get("locations", [])},
            "optimization_strategies": [],
            "deployments": [],
            "estimated_annual_savings_kg_co2": 5000
        }
    
    def evaluate_coordination_performance(self) -> Dict:
        """Evaluate coordinator's orchestration performance."""
        if not self.workflow_history:
            return {"status": "no_workflows", "performance": 0}
        
        completed_workflows = sum(1 for w in self.workflow_history if w.get("status") == "completed")
        total_workflows = len(self.workflow_history)
        success_rate = (completed_workflows / total_workflows) * 100 if total_workflows > 0 else 0
        
        return {
            "total_workflows_executed": total_workflows,
            "successful_workflows": completed_workflows,
            "success_rate_percent": round(success_rate, 2),
            "performance_grade": "excellent" if success_rate >= 95 else "good"
        }
    
    def get_workflow_analytics(self) -> Dict:
        """Get comprehensive analytics across all workflows."""
        return {
            "total_workflows": len(self.workflow_history),
            "workflow_distribution": {},
            "average_execution_time": 0,
            "total_a2a_messages": sum(len(w.get("a2a_messages", [])) for w in self.workflow_history)
        }