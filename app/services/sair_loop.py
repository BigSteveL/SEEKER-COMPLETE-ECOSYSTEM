import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import statistics
from collections import defaultdict
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SAIRLoop:
    def __init__(self, db_connection=None):
        self.db = db_connection
        self.learning_data = defaultdict(list)
        self.performance_history = []
        
        # Learning parameters
        self.confidence_thresholds = {
            "high": 0.70,
            "medium": 0.60,
            "low": 0.50
        }
        
        # Keyword weights for classification
        self.keyword_weights = {
            "technical": {
                "code": 1.0, "analyze": 0.9, "calculate": 0.8, "debug": 0.9,
                "technical": 1.0, "programming": 1.0, "software": 0.8, "data": 0.7, "algorithm": 0.9
            },
            "strategic": {
                "plan": 0.8, "strategy": 1.0, "business": 0.9, "market": 0.8,
                "growth": 0.9, "revenue": 0.8, "investment": 0.9, "partnership": 0.8, "competitive": 0.7
            },
            "sensitive": {
                "private": 1.0, "personal": 0.9, "confidential": 1.0, "secure": 0.9,
                "password": 1.0, "financial": 0.9, "medical": 1.0, "legal": 0.9
            }
        }
        
        # Agent performance tracking
        self.agent_performance = defaultdict(lambda: {
            "success_rate": 0.0,
            "avg_response_time": 0.0,
            "total_requests": 0,
            "user_satisfaction": 0.0,
            "accuracy_score": 0.0
        })
        
        # Learning rate and decay
        self.learning_rate = 0.1
        self.decay_factor = 0.95
        
    async def process_feedback(self, request_id: str, user_satisfaction: float, accuracy_score: float) -> Dict[str, Any]:
        """
        Process user feedback and accuracy scores to initiate SAIR loop.
        
        Args:
            request_id: Unique identifier for the request
            user_satisfaction: User satisfaction score (0-1)
            accuracy_score: Accuracy score (0-1)
            
        Returns:
            Dict containing processing results and next actions
        """
        try:
            # Store feedback data
            feedback_data = {
                "request_id": request_id,
                "user_satisfaction": user_satisfaction,
                "accuracy_score": accuracy_score,
                "timestamp": datetime.utcnow(),
                "combined_score": (user_satisfaction + accuracy_score) / 2
            }
            
            # Store in database if available
            if self.db:
                await self.db["feedback_data"].insert_one(feedback_data)
            
            # Add to local tracking
            self.performance_history.append(feedback_data)
            
            # Search for patterns
            patterns = await self.search_patterns(request_id)
            
            # Act on insights
            action_results = await self.act_on_insights(patterns)
            
            # Interpret results
            insights = await self.interpret_results(action_results)
            
            # Refine algorithms
            refinement_results = await self.refine_algorithms(insights)
            
            # Update routing weights
            weight_updates = await self.update_routing_weights(self.agent_performance)
            
            result = {
                "feedback_processed": True,
                "patterns_found": len(patterns.get("patterns", [])),
                "actions_taken": len(action_results.get("actions", [])),
                "insights_generated": len(insights.get("insights", [])),
                "refinements_applied": len(refinement_results.get("refinements", [])),
                "weight_updates": weight_updates,
                "timestamp": datetime.utcnow()
            }
            
            logger.info(f"SAIR loop completed for request {request_id}: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in process_feedback: {str(e)}")
            return {"error": str(e), "feedback_processed": False}
    
    async def search_patterns(self, request_id: str) -> Dict[str, Any]:
        """
        Search for patterns in recent performance data and routing decisions.
        
        Args:
            request_id: Request ID to search patterns for
            
        Returns:
            Dict containing found patterns and their significance
        """
        try:
            patterns = {
                "performance_trends": [],
                "routing_patterns": [],
                "user_satisfaction_correlations": [],
                "accuracy_patterns": []
            }
            
            # Get recent performance data
            recent_data = self.performance_history[-100:] if self.performance_history else []
            
            if recent_data:
                # Analyze performance trends
                satisfaction_scores = [d["user_satisfaction"] for d in recent_data]
                accuracy_scores = [d["accuracy_score"] for d in recent_data]
                
                if len(satisfaction_scores) > 1:
                    patterns["performance_trends"] = {
                        "avg_satisfaction": statistics.mean(satisfaction_scores),
                        "avg_accuracy": statistics.mean(accuracy_scores),
                        "satisfaction_trend": "improving" if satisfaction_scores[-1] > satisfaction_scores[0] else "declining",
                        "accuracy_trend": "improving" if accuracy_scores[-1] > accuracy_scores[0] else "declining"
                    }
                
                # Find correlation patterns
                if len(recent_data) > 10:
                    high_satisfaction_data = [d for d in recent_data if d["user_satisfaction"] > 0.8]
                    if high_satisfaction_data:
                        patterns["user_satisfaction_correlations"] = {
                            "high_satisfaction_count": len(high_satisfaction_data),
                            "avg_accuracy_high_satisfaction": statistics.mean([d["accuracy_score"] for d in high_satisfaction_data])
                        }
            
            # Search database for routing patterns if available
            if self.db:
                routing_data = await self.db["task_requests"].find({"request_id": request_id}).to_list(1)
                if routing_data:
                    patterns["routing_patterns"] = routing_data[0].get("routing_decision", {})
            
            logger.info(f"Patterns found: {len(patterns)} categories")
            return {"patterns": patterns, "timestamp": datetime.utcnow()}
            
        except Exception as e:
            logger.error(f"Error in search_patterns: {str(e)}")
            return {"patterns": {}, "error": str(e)}
    
    async def act_on_insights(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Act on insights from pattern analysis to improve performance.
        
        Args:
            patterns: Patterns found from search phase
            
        Returns:
            Dict containing actions taken and their expected impact
        """
        try:
            actions = []
            
            # Analyze performance trends and take actions
            performance_trends = patterns.get("patterns", {}).get("performance_trends", {})
            
            if performance_trends:
                # Adjust confidence thresholds based on performance
                if performance_trends.get("satisfaction_trend") == "declining":
                    actions.append({
                        "action": "adjust_confidence_thresholds",
                        "details": "Lowering thresholds due to declining satisfaction",
                        "impact": "expected_improvement"
                    })
                    await self._adjust_confidence_thresholds(direction="lower")
                
                if performance_trends.get("accuracy_trend") == "declining":
                    actions.append({
                        "action": "update_keyword_weights",
                        "details": "Updating keyword weights due to declining accuracy",
                        "impact": "expected_improvement"
                    })
                    await self._update_keyword_weights()
            
            # Analyze user satisfaction correlations
            satisfaction_correlations = patterns.get("patterns", {}).get("user_satisfaction_correlations", {})
            if satisfaction_correlations:
                high_satisfaction_count = satisfaction_correlations.get("high_satisfaction_count", 0)
                if high_satisfaction_count > 20:  # Threshold for significant pattern
                    actions.append({
                        "action": "optimize_routing_for_satisfaction",
                        "details": f"High satisfaction pattern detected ({high_satisfaction_count} cases)",
                        "impact": "maintain_high_satisfaction"
                    })
            
            # Store actions in database
            if self.db and actions:
                for action in actions:
                    action["timestamp"] = datetime.utcnow()
                    await self.db["sair_actions"].insert_one(action)
            
            logger.info(f"Actions taken: {len(actions)}")
            return {"actions": actions, "timestamp": datetime.utcnow()}
            
        except Exception as e:
            logger.error(f"Error in act_on_insights: {str(e)}")
            return {"actions": [], "error": str(e)}
    
    async def interpret_results(self, action_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpret the results of actions taken to generate insights.
        
        Args:
            action_results: Results from the act phase
            
        Returns:
            Dict containing insights and recommendations
        """
        try:
            insights = []
            actions = action_results.get("actions", [])
            
            # Analyze action effectiveness
            for action in actions:
                action_type = action.get("action", "")
                impact = action.get("impact", "")
                
                if action_type == "adjust_confidence_thresholds":
                    insights.append({
                        "type": "threshold_adjustment",
                        "insight": "Confidence thresholds adjusted to improve routing accuracy",
                        "recommendation": "Monitor performance for next 24 hours",
                        "priority": "high"
                    })
                
                elif action_type == "update_keyword_weights":
                    insights.append({
                        "type": "keyword_optimization",
                        "insight": "Keyword weights updated to improve classification",
                        "recommendation": "Test with new classification requests",
                        "priority": "medium"
                    })
                
                elif action_type == "optimize_routing_for_satisfaction":
                    insights.append({
                        "type": "routing_optimization",
                        "insight": "Routing optimized based on high satisfaction patterns",
                        "recommendation": "Continue monitoring satisfaction trends",
                        "priority": "high"
                    })
            
            # Generate performance insights
            recent_performance = self.performance_history[-20:] if self.performance_history else []
            if recent_performance:
                avg_satisfaction = statistics.mean([p["user_satisfaction"] for p in recent_performance])
                avg_accuracy = statistics.mean([p["accuracy_score"] for p in recent_performance])
                
                insights.append({
                    "type": "performance_summary",
                    "insight": f"Recent performance: {avg_satisfaction:.2f} satisfaction, {avg_accuracy:.2f} accuracy",
                    "recommendation": "Continue current optimization if performance is good",
                    "priority": "medium"
                })
            
            # Store insights in database
            if self.db and insights:
                for insight in insights:
                    insight["timestamp"] = datetime.utcnow()
                    await self.db["sair_insights"].insert_one(insight)
            
            logger.info(f"Insights generated: {len(insights)}")
            return {"insights": insights, "timestamp": datetime.utcnow()}
            
        except Exception as e:
            logger.error(f"Error in interpret_results: {str(e)}")
            return {"insights": [], "error": str(e)}
    
    async def refine_algorithms(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Refine algorithms based on insights from interpretation phase.
        
        Args:
            insights: Insights from the interpret phase
            
        Returns:
            Dict containing refinements applied and their parameters
        """
        try:
            refinements = []
            insights_list = insights.get("insights", [])
            
            for insight in insights_list:
                insight_type = insight.get("type", "")
                
                if insight_type == "threshold_adjustment":
                    # Refine confidence thresholds
                    refinement = await self._refine_confidence_thresholds()
                    refinements.append(refinement)
                
                elif insight_type == "keyword_optimization":
                    # Refine keyword weights
                    refinement = await self._refine_keyword_weights()
                    refinements.append(refinement)
                
                elif insight_type == "routing_optimization":
                    # Refine routing algorithms
                    refinement = await self._refine_routing_algorithms()
                    refinements.append(refinement)
            
            # Apply learning rate decay
            self.learning_rate *= self.decay_factor
            
            # Store refinements in database
            if self.db and refinements:
                for refinement in refinements:
                    refinement["timestamp"] = datetime.utcnow()
                    refinement["learning_rate"] = self.learning_rate
                    await self.db["sair_refinements"].insert_one(refinement)
            
            logger.info(f"Refinements applied: {len(refinements)}")
            return {"refinements": refinements, "learning_rate": self.learning_rate, "timestamp": datetime.utcnow()}
            
        except Exception as e:
            logger.error(f"Error in refine_algorithms: {str(e)}")
            return {"refinements": [], "error": str(e)}
    
    async def update_routing_weights(self, agent_performance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update routing weights based on agent performance data.
        
        Args:
            agent_performance: Performance data for all agents
            
        Returns:
            Dict containing updated weights and performance metrics
        """
        try:
            weight_updates = {}
            
            # Update agent performance tracking
            for agent_id, performance in agent_performance.items():
                if agent_id in self.agent_performance:
                    # Update with exponential moving average
                    current = self.agent_performance[agent_id]
                    alpha = self.learning_rate
                    
                    self.agent_performance[agent_id].update({
                        "success_rate": alpha * performance.get("success_rate", 0.0) + (1 - alpha) * current["success_rate"],
                        "avg_response_time": alpha * performance.get("avg_response_time", 0.0) + (1 - alpha) * current["avg_response_time"],
                        "total_requests": current["total_requests"] + performance.get("total_requests", 0),
                        "user_satisfaction": alpha * performance.get("user_satisfaction", 0.0) + (1 - alpha) * current["user_satisfaction"],
                        "accuracy_score": alpha * performance.get("accuracy_score", 0.0) + (1 - alpha) * current["accuracy_score"]
                    })
                    
                    weight_updates[agent_id] = {
                        "success_rate": self.agent_performance[agent_id]["success_rate"],
                        "weight_adjustment": self._calculate_weight_adjustment(agent_id)
                    }
            
            # Store weight updates in database
            if self.db and weight_updates:
                weight_data = {
                    "weight_updates": weight_updates,
                    "timestamp": datetime.utcnow(),
                    "learning_rate": self.learning_rate
                }
                await self.db["routing_weights"].insert_one(weight_data)
            
            logger.info(f"Routing weights updated for {len(weight_updates)} agents")
            return {"weight_updates": weight_updates, "timestamp": datetime.utcnow()}
            
        except Exception as e:
            logger.error(f"Error in update_routing_weights: {str(e)}")
            return {"weight_updates": {}, "error": str(e)}
    
    async def _adjust_confidence_thresholds(self, direction: str = "lower"):
        """Adjust confidence thresholds based on performance."""
        adjustment_factor = 0.05 if direction == "lower" else -0.05
        
        for threshold_type in self.confidence_thresholds:
            self.confidence_thresholds[threshold_type] = max(0.1, min(0.9, 
                self.confidence_thresholds[threshold_type] + adjustment_factor))
    
    async def _update_keyword_weights(self):
        """Update keyword weights based on performance feedback."""
        # Simple weight adjustment - in production, use more sophisticated ML
        for category, keywords in self.keyword_weights.items():
            for keyword, weight in keywords.items():
                # Adjust weight based on recent performance
                adjustment = (statistics.mean([p["accuracy_score"] for p in self.performance_history[-10:]]) - 0.5) * 0.1
                self.keyword_weights[category][keyword] = max(0.1, min(2.0, weight + adjustment))
    
    async def _refine_confidence_thresholds(self) -> Dict[str, Any]:
        """Refine confidence thresholds based on insights."""
        return {
            "type": "confidence_threshold_refinement",
            "old_thresholds": dict(self.confidence_thresholds),
            "new_thresholds": dict(self.confidence_thresholds),
            "adjustment_factor": self.learning_rate
        }
    
    async def _refine_keyword_weights(self) -> Dict[str, Any]:
        """Refine keyword weights based on insights."""
        return {
            "type": "keyword_weight_refinement",
            "adjustments": "Weights updated based on performance feedback",
            "learning_rate": self.learning_rate
        }
    
    async def _refine_routing_algorithms(self) -> Dict[str, Any]:
        """Refine routing algorithms based on insights."""
        return {
            "type": "routing_algorithm_refinement",
            "adjustments": "Routing logic optimized based on satisfaction patterns",
            "learning_rate": self.learning_rate
        }
    
    def _calculate_weight_adjustment(self, agent_id: str) -> float:
        """Calculate weight adjustment for an agent based on performance."""
        performance = self.agent_performance[agent_id]
        success_rate = performance["success_rate"]
        user_satisfaction = performance["user_satisfaction"]
        
        # Weight adjustment based on success rate and user satisfaction
        weight_adjustment = (success_rate + user_satisfaction) / 2 - 0.5
        return weight_adjustment * self.learning_rate
    
    async def get_learning_summary(self) -> Dict[str, Any]:
        """Get a summary of learning progress and current state."""
        try:
            summary = {
                "total_feedback_processed": len(self.performance_history),
                "current_learning_rate": self.learning_rate,
                "confidence_thresholds": dict(self.confidence_thresholds),
                "agent_performance": dict(self.agent_performance),
                "recent_performance": {
                    "avg_satisfaction": 0.0,
                    "avg_accuracy": 0.0
                }
            }
            
            if self.performance_history:
                recent_data = self.performance_history[-20:]
                summary["recent_performance"] = {
                    "avg_satisfaction": statistics.mean([p["user_satisfaction"] for p in recent_data]),
                    "avg_accuracy": statistics.mean([p["accuracy_score"] for p in recent_data])
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting learning summary: {str(e)}")
            return {"error": str(e)} 