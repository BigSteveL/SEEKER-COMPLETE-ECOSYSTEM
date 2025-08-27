import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import statistics
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentRouter:
    def __init__(self):
        # SEEKER-specific agent definitions based on patent
        self.agents = {
            "product_search_agent": {
                "capabilities": ["global_search", "price_comparison", "supplier_analysis", "market_research"],
                "performance_metrics": {"success_rate": 0.0, "avg_response_time": 0.0, "total_requests": 0},
                "availability": True
            },
            "price_negotiation_agent": {
                "capabilities": ["price_optimization", "supplier_negotiation", "demand_forecasting", "competitive_analysis"],
                "performance_metrics": {"success_rate": 0.0, "avg_response_time": 0.0, "total_requests": 0},
                "availability": True
            },
            "verification_agent": {
                "capabilities": ["product_verification", "fraud_detection", "compliance_checking", "quality_assurance"],
                "performance_metrics": {"success_rate": 0.0, "avg_response_time": 0.0, "total_requests": 0},
                "availability": True
            },
            "supply_chain_agent": {
                "capabilities": ["logistics_monitoring", "inventory_tracking", "delivery_optimization", "real_time_insights"],
                "performance_metrics": {"success_rate": 0.0, "avg_response_time": 0.0, "total_requests": 0},
                "availability": True
            },
            "translation_agent": {
                "capabilities": ["multilingual_translation", "voice_processing", "cross_border_communication", "cultural_adaptation"],
                "performance_metrics": {"success_rate": 0.0, "avg_response_time": 0.0, "total_requests": 0},
                "availability": True
            },
            # Legacy agents for backward compatibility
            "technical_ai_agent": {
                "capabilities": ["code_analysis", "debugging", "algorithm_optimization"],
                "performance_metrics": {"success_rate": 0.0, "avg_response_time": 0.0, "total_requests": 0},
                "availability": True
            },
            "strategic_ai_agent": {
                "capabilities": ["business_analysis", "market_research", "strategy_planning"],
                "performance_metrics": {"success_rate": 0.0, "avg_response_time": 0.0, "total_requests": 0},
                "availability": True
            },
            "local_ai_system": {
                "capabilities": ["secure_processing", "privacy_compliance", "local_analysis"],
                "performance_metrics": {"success_rate": 0.0, "avg_response_time": 0.0, "total_requests": 0},
                "availability": True
            },
            "human_operator": {
                "capabilities": ["complex_analysis", "decision_making", "escalation_handling"],
                "performance_metrics": {"success_rate": 0.0, "avg_response_time": 0.0, "total_requests": 0},
                "availability": True
            }
        }
        
        # Performance tracking
        self.routing_history = []
        self.performance_data = defaultdict(list)
        
        # SAIR loop integration
        self.sair_loop_data = []
        
        # Confidence thresholds
        self.high_confidence_threshold = 0.70
        self.medium_confidence_threshold = 0.60
        
    async def determine_routing(self, classification_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine optimal routing based on classification results.
        
        Args:
            classification_results: Dict containing scores, confidence, and routing_decision
            
        Returns:
            Dict containing routing decision with assigned agents and logic
        """
        try:
            scores = classification_results.get("classification_results", {})
            confidence = classification_results.get("confidence", 0.0)
            primary_category = classification_results.get("routing_decision", {}).get("primary_category", "unknown")
            
            # Assign agents based on category and confidence
            assigned_agents = await self._assign_agents(primary_category, confidence)
            
            # Determine routing logic
            routing_logic = self._get_routing_logic(confidence, len(assigned_agents))
            
            # Create routing decision
            routing_decision = await self._create_routing_decision(assigned_agents, routing_logic)
            
            # Track routing decision for performance analysis
            await self._track_routing_decision(classification_results, routing_decision)
            
            # Update SAIR loop data
            await self._update_sair_loop_data(classification_results, routing_decision)
            
            logger.info(f"Routing determined: {assigned_agents} with logic: {routing_logic}")
            return routing_decision
            
        except Exception as e:
            logger.error(f"Error in determine_routing: {str(e)}")
            return await self._get_fallback_routing()
    
    async def _assign_agents(self, category: str, confidence: float) -> List[str]:
        """
        Assign SEEKER-specific agents based on category and confidence level.
        
        Args:
            category: Primary classification category
            confidence: Confidence score (0-1)
            
        Returns:
            List of assigned agent IDs
        """
        try:
            # Handle sensitive content first (highest priority)
            if category == "sensitive" and confidence > 0:
                return ["local_ai_system"]
            
            # SEEKER-specific routing based on patent categories
            if confidence > self.high_confidence_threshold:
                if category == "product_search":
                    return ["product_search_agent"]
                elif category == "price_negotiation":
                    return ["price_negotiation_agent"]
                elif category == "verification":
                    return ["verification_agent"]
                elif category == "supply_chain":
                    return ["supply_chain_agent"]
                elif category == "translation":
                    return ["translation_agent"]
                # Legacy categories
                elif category == "technical":
                    return ["technical_ai_agent"]
                elif category == "strategic":
                    return ["strategic_ai_agent"]
                else:
                    return ["human_operator"]
            
            # Medium confidence - dual processing
            elif confidence > self.medium_confidence_threshold:
                if category in ["product_search", "price_negotiation", "verification", "supply_chain", "translation"]:
                    # Assign primary agent and backup human operator
                    primary_agent = f"{category.replace('_', '')}_agent"
                    return [primary_agent, "human_operator"]
                elif category in ["technical", "strategic"]:
                    return ["technical_ai_agent", "strategic_ai_agent"]
                else:
                    return ["human_operator"]
            
            # Low confidence - human escalation
            else:
                return ["human_operator"]
                
        except Exception as e:
            logger.error(f"Error in _assign_agents: {str(e)}")
            return ["human_operator"]
    
    async def _create_routing_decision(self, agents: List[str], logic: str) -> Dict[str, Any]:
        """
        Create comprehensive routing decision with metadata.
        
        Args:
            agents: List of assigned agent IDs
            logic: Routing logic description
            
        Returns:
            Dict containing routing decision details
        """
        try:
            # Get agent details
            agent_details = []
            for agent_id in agents:
                if agent_id in self.agents:
                    agent_details.append({
                        "agent_id": agent_id,
                        "capabilities": self.agents[agent_id]["capabilities"],
                        "performance_metrics": self.agents[agent_id]["performance_metrics"],
                        "availability": self.agents[agent_id]["availability"]
                    })
            
            routing_decision = {
                "assigned_agents": agents,
                "agent_details": agent_details,
                "routing_logic": logic,
                "timestamp": datetime.utcnow(),
                "estimated_processing_time": await self._estimate_processing_time(agents),
                "load_balancing": await self._check_load_balancing(agents)
            }
            
            return routing_decision
            
        except Exception as e:
            logger.error(f"Error in _create_routing_decision: {str(e)}")
            return {
                "assigned_agents": ["human_operator"],
                "routing_logic": "fallback",
                "timestamp": datetime.utcnow()
            }
    
    def _get_routing_logic(self, confidence: float, agent_count: int) -> str:
        """Determine routing logic based on confidence and agent count."""
        if confidence > self.high_confidence_threshold:
            return "auto-route"
        elif confidence > self.medium_confidence_threshold:
            return "dual-AI processing"
        else:
            return "human escalation"
    
    async def _estimate_processing_time(self, agents: List[str]) -> float:
        """Estimate processing time based on agent performance metrics."""
        try:
            total_time = 0.0
            for agent_id in agents:
                if agent_id in self.agents:
                    avg_time = self.agents[agent_id]["performance_metrics"]["avg_response_time"]
                    total_time += avg_time
            
            return total_time / len(agents) if agents else 0.0
            
        except Exception as e:
            logger.error(f"Error estimating processing time: {str(e)}")
            return 0.0
    
    async def _check_load_balancing(self, agents: List[str]) -> Dict[str, Any]:
        """Check load balancing across assigned agents."""
        try:
            load_info = {}
            for agent_id in agents:
                if agent_id in self.agents:
                    total_requests = self.agents[agent_id]["performance_metrics"]["total_requests"]
                    load_info[agent_id] = {
                        "total_requests": total_requests,
                        "availability": self.agents[agent_id]["availability"]
                    }
            
            return load_info
            
        except Exception as e:
            logger.error(f"Error checking load balancing: {str(e)}")
            return {}
    
    async def _track_routing_decision(self, classification_results: Dict[str, Any], routing_decision: Dict[str, Any]):
        """Track routing decision for performance analysis."""
        try:
            tracking_data = {
                "timestamp": datetime.utcnow(),
                "classification": classification_results,
                "routing": routing_decision,
                "performance_metrics": {}
            }
            
            self.routing_history.append(tracking_data)
            
            # Keep only last 1000 entries for memory management
            if len(self.routing_history) > 1000:
                self.routing_history = self.routing_history[-1000:]
                
        except Exception as e:
            logger.error(f"Error tracking routing decision: {str(e)}")
    
    async def _update_sair_loop_data(self, classification_results: Dict[str, Any], routing_decision: Dict[str, Any]):
        """Update SAIR loop data for learning and optimization."""
        try:
            sair_data = {
                "loop_id": f"sair_{datetime.utcnow().timestamp()}",
                "request_id": None,  # Will be set when request is processed
                "success_metrics": {
                    "confidence": classification_results.get("confidence", 0.0),
                    "agent_count": len(routing_decision.get("assigned_agents", [])),
                    "routing_logic": routing_decision.get("routing_logic", "")
                },
                "learning_updates": {
                    "category_distribution": classification_results.get("classification_results", {}),
                    "routing_pattern": routing_decision.get("assigned_agents", [])
                },
                "routing_adjustments": {
                    "load_balancing": routing_decision.get("load_balancing", {}),
                    "estimated_time": routing_decision.get("estimated_processing_time", 0.0)
                },
                "timestamp": datetime.utcnow()
            }
            
            self.sair_loop_data.append(sair_data)
            
            # Trigger learning updates
            await self._update_agent_performance()
            
        except Exception as e:
            logger.error(f"Error updating SAIR loop data: {str(e)}")
    
    async def _update_agent_performance(self):
        """Update agent performance metrics based on recent routing history."""
        try:
            # Analyze recent routing history for performance updates
            recent_history = self.routing_history[-100:] if self.routing_history else []
            
            for agent_id in self.agents:
                agent_routes = [h for h in recent_history if agent_id in h.get("routing", {}).get("assigned_agents", [])]
                
                if agent_routes:
                    # Calculate success rate (simplified - in real implementation, this would come from actual results)
                    success_rate = 0.85  # Placeholder
                    
                    # Calculate average response time (simplified)
                    avg_response_time = 2.5  # Placeholder
                    
                    # Update agent metrics
                    self.agents[agent_id]["performance_metrics"].update({
                        "success_rate": success_rate,
                        "avg_response_time": avg_response_time,
                        "total_requests": len(agent_routes)
                    })
                    
        except Exception as e:
            logger.error(f"Error updating agent performance: {str(e)}")
    
    async def _get_fallback_routing(self) -> Dict[str, Any]:
        """Get fallback routing when errors occur."""
        return {
            "assigned_agents": ["human_operator"],
            "routing_logic": "fallback",
            "timestamp": datetime.utcnow(),
            "error": "Fallback routing due to error"
        }
    
    async def get_performance_analytics(self) -> Dict[str, Any]:
        """Get performance analytics for monitoring and optimization."""
        try:
            analytics = {
                "total_routes": len(self.routing_history),
                "agent_performance": {},
                "routing_distribution": defaultdict(int),
                "confidence_distribution": defaultdict(int)
            }
            
            # Agent performance
            for agent_id, agent_data in self.agents.items():
                analytics["agent_performance"][agent_id] = agent_data["performance_metrics"]
            
            # Routing distribution
            for route in self.routing_history:
                logic = route.get("routing", {}).get("routing_logic", "unknown")
                analytics["routing_distribution"][logic] += 1
                
                confidence = route.get("classification", {}).get("confidence", 0.0)
                if confidence > self.high_confidence_threshold:
                    analytics["confidence_distribution"]["high"] += 1
                elif confidence > self.medium_confidence_threshold:
                    analytics["confidence_distribution"]["medium"] += 1
                else:
                    analytics["confidence_distribution"]["low"] += 1
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting performance analytics: {str(e)}")
            return {}
    
    async def optimize_routing(self):
        """Optimize routing based on performance data and SAIR loop insights."""
        try:
            # Analyze performance patterns
            analytics = await self.get_performance_analytics()
            
            # Adjust agent availability based on performance
            for agent_id, performance in analytics.get("agent_performance", {}).items():
                if performance.get("success_rate", 0.0) < 0.7:
                    self.agents[agent_id]["availability"] = False
                    logger.warning(f"Agent {agent_id} marked as unavailable due to low success rate")
            
            # Update routing thresholds based on performance
            # This is a simplified optimization - in production, you'd use more sophisticated ML
            logger.info("Routing optimization completed")
            
        except Exception as e:
            logger.error(f"Error optimizing routing: {str(e)}") 