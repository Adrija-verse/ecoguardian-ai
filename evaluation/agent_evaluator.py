"""
Advanced Agent Evaluation System
Demonstrates sophisticated agent self-assessment
"""

import json
from typing import Dict, List, Any
from datetime import datetime

class AgentEvaluator:
    """Evaluates agent performance with multiple metrics"""
    
    def __init__(self):
        self.evaluation_history = []
        self.benchmarks = {
            "prediction_accuracy": 0.85,  # 85% target
            "response_time": 5.0,  # 5 seconds max
            "deployment_success": 0.95,  # 95% success rate
            "data_completeness": 0.90  # 90% complete data
        }
    
    def evaluate_prediction_quality(
        self, 
        predictions: Dict[str, Any], 
        ground_truth: Dict[str, Any] = None
    ) -> Dict[str, float]:
        """Evaluate prediction quality with detailed metrics"""
        
        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "metrics": {}
        }
        
        # 1. Completeness Score
        required_fields = ["interventions", "average_confidence", "city"]
        completeness = sum(
            1 for field in required_fields 
            if field in predictions and predictions[field]
        ) / len(required_fields)
        evaluation["metrics"]["completeness"] = round(completeness * 100, 2)
        
        # 2. Confidence Score
        avg_confidence = predictions.get("average_confidence", 0)
        confidence_score = min(avg_confidence / 80, 1.0) * 100  # 80% is ideal
        evaluation["metrics"]["confidence_quality"] = round(confidence_score, 2)
        
        # 3. Intervention Relevance
        interventions = predictions.get("interventions", [])
        high_priority = sum(
            1 for i in interventions 
            if i.get("priority_level") == "High"
        )
        relevance = (high_priority / len(interventions) * 100) if interventions else 0
        evaluation["metrics"]["intervention_relevance"] = round(relevance, 2)
        
        # 4. Overall Quality Score
        overall = (
            completeness * 0.3 +
            (avg_confidence / 100) * 0.4 +
            (relevance / 100) * 0.3
        ) * 100
        evaluation["metrics"]["overall_quality"] = round(overall, 2)
        
        # 5. Pass/Fail
        evaluation["status"] = "PASS" if overall >= 70 else "FAIL"
        evaluation["grade"] = self._get_grade(overall)
        
        self.evaluation_history.append(evaluation)
        return evaluation
    
    def evaluate_agent_collaboration(
        self,
        a2a_messages: List[Dict]
    ) -> Dict[str, Any]:
        """Evaluate inter-agent collaboration quality"""
        
        if not a2a_messages:
            return {
                "message_count": 0,
                "collaboration_score": 0,
                "status": "FAIL - No A2A communication"
            }
        
        # Analyze message flow
        senders = set(msg["sender"] for msg in a2a_messages)
        receivers = set(msg["receiver"] for msg in a2a_messages)
        
        # Calculate collaboration metrics
        agent_participation = len(senders.union(receivers))
        message_density = len(a2a_messages) / max(agent_participation, 1)
        
        collaboration_score = min(
            (agent_participation / 4) * 0.5 +  # Ideal: 4+ agents
            min(message_density / 2, 1.0) * 0.5  # Ideal: 2+ messages per agent
        , 1.0) * 100
        
        return {
            "message_count": len(a2a_messages),
            "unique_agents": agent_participation,
            "message_density": round(message_density, 2),
            "collaboration_score": round(collaboration_score, 2),
            "status": "PASS" if collaboration_score >= 70 else "NEEDS_IMPROVEMENT"
        }
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 95: return "A+"
        if score >= 90: return "A"
        if score >= 85: return "B+"
        if score >= 80: return "B"
        if score >= 75: return "C+"
        if score >= 70: return "C"
        return "F"
    
    def generate_evaluation_report(self) -> Dict[str, Any]:
        """Generate comprehensive evaluation report"""
        if not self.evaluation_history:
            return {"status": "No evaluations performed"}
        
        # Calculate aggregates
        all_scores = [
            e["metrics"]["overall_quality"] 
            for e in self.evaluation_history
        ]
        
        return {
            "total_evaluations": len(self.evaluation_history),
            "average_score": round(sum(all_scores) / len(all_scores), 2),
            "highest_score": round(max(all_scores), 2),
            "lowest_score": round(min(all_scores), 2),
            "pass_rate": round(
                sum(1 for e in self.evaluation_history if e["status"] == "PASS") 
                / len(self.evaluation_history) * 100, 2
            ),
            "benchmark_comparison": self._compare_to_benchmarks(),
            "recent_evaluations": self.evaluation_history[-5:]
        }
    
    def _compare_to_benchmarks(self) -> Dict[str, str]:
        """Compare performance against benchmarks"""
        if not self.evaluation_history:
            return {}
        
        avg_quality = sum(
            e["metrics"]["overall_quality"] 
            for e in self.evaluation_history
        ) / len(self.evaluation_history)
        
        return {
            "vs_target_85": "EXCEEDS" if avg_quality >= 85 else "BELOW",
            "performance_level": self._get_grade(avg_quality),
            "improvement_needed": max(0, 85 - avg_quality)
        }

# Global instance
agent_evaluator = AgentEvaluator()