import logging
from typing import Dict, List, Any
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskClassificationEngine:
    def __init__(self):
        # Define SEEKER-specific keyword categories based on patent
        self.product_search_keywords = [
            "product", "search", "find", "compare", "price", "cost", "buy", "purchase",
            "supplier", "vendor", "manufacturer", "global", "regional", "market",
            "shipping", "delivery", "inventory", "stock", "availability"
        ]
        
        self.price_negotiation_keywords = [
            "negotiate", "bargain", "discount", "deal", "offer", "quote", "pricing",
            "competitive", "market price", "best price", "lowest cost", "bulk",
            "quantity", "volume discount", "contract", "agreement"
        ]
        
        self.verification_keywords = [
            "verify", "authenticate", "validate", "check", "inspect", "quality",
            "certification", "compliance", "regulatory", "standards", "fraud",
            "genuine", "original", "counterfeit", "safety", "testing"
        ]
        
        self.supply_chain_keywords = [
            "supply chain", "logistics", "shipping", "tracking", "delivery",
            "fulfillment", "warehouse", "distribution", "transport", "freight",
            "order status", "inventory", "stock", "lead time", "backorder"
        ]
        
        self.translation_keywords = [
            "translate", "language", "multilingual", "foreign", "international",
            "cross-border", "localization", "interpret", "communication",
            "voice", "speech", "dialect", "culture", "region"
        ]
        
        # Legacy categories for backward compatibility
        self.technical_keywords = [
            "code", "analyze", "calculate", "debug", "technical", 
            "programming", "software", "data", "algorithm"
        ]
        self.strategic_keywords = [
            "plan", "strategy", "business", "market", "growth", 
            "revenue", "investment", "partnership", "competitive"
        ]
        self.sensitive_keywords = [
            "private", "personal", "confidential", "secure", "password", 
            "financial", "medical", "legal"
        ]
        
        # Confidence thresholds
        self.high_confidence_threshold = 0.70
        self.medium_confidence_threshold = 0.60
        
    def classify_request(self, input_text: str) -> Dict[str, Any]:
        """
        Main classification method that processes input text and returns classification results.
        
        Args:
            input_text (str): The input text to classify
            
        Returns:
            Dict containing classification_results, confidence, and routing_decision
        """
        try:
            if not input_text or not input_text.strip():
                logger.warning("Empty or None input text provided")
                return self._get_default_classification()
            
            # Calculate scores for each SEEKER category
            product_search_score = self._calculate_product_search_score(input_text)
            price_negotiation_score = self._calculate_price_negotiation_score(input_text)
            verification_score = self._calculate_verification_score(input_text)
            supply_chain_score = self._calculate_supply_chain_score(input_text)
            translation_score = self._calculate_translation_score(input_text)
            
            # Legacy scores for backward compatibility
            technical_score = self._calculate_technical_score(input_text)
            strategic_score = self._calculate_strategic_score(input_text)
            sensitive_score = self._calculate_sensitive_score(input_text)
            
            scores = {
                "product_search": product_search_score,
                "price_negotiation": price_negotiation_score,
                "verification": verification_score,
                "supply_chain": supply_chain_score,
                "translation": translation_score,
                "technical": technical_score,
                "strategic": strategic_score,
                "sensitive": sensitive_score
            }
            
            # Calculate overall confidence
            confidence = self._calculate_confidence(scores)
            
            # Determine routing based on scores and confidence
            routing_decision = self._determine_routing(scores, confidence)
            
            result = {
                "classification_results": scores,
                "confidence": confidence,
                "routing_decision": routing_decision
            }
            
            logger.info(f"Classification completed: confidence={confidence:.2f}, routing={routing_decision['assigned_agents']}")
            return result
            
        except Exception as e:
            logger.error(f"Error in classify_request: {str(e)}")
            return self._get_default_classification()
    
    def _calculate_technical_score(self, text: str) -> float:
        """Calculate technical relevance score (0-1)."""
        try:
            text_lower = text.lower()
            matches = sum(1 for keyword in self.technical_keywords if keyword in text_lower)
            total_keywords = len(self.technical_keywords)
            return min(matches / total_keywords, 1.0) if total_keywords > 0 else 0.0
        except Exception as e:
            logger.error(f"Error calculating technical score: {str(e)}")
            return 0.0
    
    def _calculate_strategic_score(self, text: str) -> float:
        """Calculate strategic relevance score (0-1)."""
        try:
            text_lower = text.lower()
            matches = sum(1 for keyword in self.strategic_keywords if keyword in text_lower)
            total_keywords = len(self.strategic_keywords)
            return min(matches / total_keywords, 1.0) if total_keywords > 0 else 0.0
        except Exception as e:
            logger.error(f"Error calculating strategic score: {str(e)}")
            return 0.0
    
    def _calculate_product_search_score(self, text: str) -> float:
        """Calculate product search relevance score (0-1)."""
        try:
            text_lower = text.lower()
            matches = sum(1 for keyword in self.product_search_keywords if keyword in text_lower)
            total_keywords = len(self.product_search_keywords)
            return min(matches / total_keywords, 1.0) if total_keywords > 0 else 0.0
        except Exception as e:
            logger.error(f"Error calculating product search score: {str(e)}")
            return 0.0
    
    def _calculate_price_negotiation_score(self, text: str) -> float:
        """Calculate price negotiation relevance score (0-1)."""
        try:
            text_lower = text.lower()
            matches = sum(1 for keyword in self.price_negotiation_keywords if keyword in text_lower)
            total_keywords = len(self.price_negotiation_keywords)
            return min(matches / total_keywords, 1.0) if total_keywords > 0 else 0.0
        except Exception as e:
            logger.error(f"Error calculating price negotiation score: {str(e)}")
            return 0.0
    
    def _calculate_verification_score(self, text: str) -> float:
        """Calculate verification/authentication relevance score (0-1)."""
        try:
            text_lower = text.lower()
            matches = sum(1 for keyword in self.verification_keywords if keyword in text_lower)
            total_keywords = len(self.verification_keywords)
            return min(matches / total_keywords, 1.0) if total_keywords > 0 else 0.0
        except Exception as e:
            logger.error(f"Error calculating verification score: {str(e)}")
            return 0.0
    
    def _calculate_supply_chain_score(self, text: str) -> float:
        """Calculate supply chain monitoring relevance score (0-1)."""
        try:
            text_lower = text.lower()
            matches = sum(1 for keyword in self.supply_chain_keywords if keyword in text_lower)
            total_keywords = len(self.supply_chain_keywords)
            return min(matches / total_keywords, 1.0) if total_keywords > 0 else 0.0
        except Exception as e:
            logger.error(f"Error calculating supply chain score: {str(e)}")
            return 0.0
    
    def _calculate_translation_score(self, text: str) -> float:
        """Calculate translation/multilingual relevance score (0-1)."""
        try:
            text_lower = text.lower()
            matches = sum(1 for keyword in self.translation_keywords if keyword in text_lower)
            total_keywords = len(self.translation_keywords)
            return min(matches / total_keywords, 1.0) if total_keywords > 0 else 0.0
        except Exception as e:
            logger.error(f"Error calculating translation score: {str(e)}")
            return 0.0
    
    def _calculate_sensitive_score(self, text: str) -> float:
        """Calculate sensitive content score (0-1)."""
        try:
            text_lower = text.lower()
            matches = sum(1 for keyword in self.sensitive_keywords if keyword in text_lower)
            total_keywords = len(self.sensitive_keywords)
            return min(matches / total_keywords, 1.0) if total_keywords > 0 else 0.0
        except Exception as e:
            logger.error(f"Error calculating sensitive score: {str(e)}")
            return 0.0
    
    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """Calculate overall confidence based on score distribution."""
        try:
            # Simple confidence calculation based on score variance
            max_score = max(scores.values())
            min_score = min(scores.values())
            variance = max_score - min_score
            
            # Higher variance indicates more confident classification
            confidence = min(max_score + (variance * 0.5), 1.0)
            return round(confidence, 3)
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 0.5
    
    def _determine_routing(self, scores: Dict[str, float], confidence: float) -> Dict[str, Any]:
        """Determine routing decision based on scores and confidence."""
        try:
            # Determine primary category
            primary_category = max(scores.items(), key=lambda x: x[1])[0]
            
            # Determine routing logic based on confidence
            if confidence > self.high_confidence_threshold:
                routing_logic = "auto-route"
                assigned_agents = [f"ai_agent_{primary_category}"]
            elif confidence > self.medium_confidence_threshold:
                routing_logic = "dual-AI processing"
                # Assign primary and secondary agents
                sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                assigned_agents = [f"ai_agent_{sorted_categories[0][0]}", f"ai_agent_{sorted_categories[1][0]}"]
            else:
                routing_logic = "escalate to human"
                assigned_agents = ["human_agent"]
            
            return {
                "assigned_agents": assigned_agents,
                "routing_logic": routing_logic,
                "primary_category": primary_category,
                "confidence_level": self._get_confidence_level(confidence)
            }
            
        except Exception as e:
            logger.error(f"Error determining routing: {str(e)}")
            return {
                "assigned_agents": ["human_agent"],
                "routing_logic": "escalate to human",
                "primary_category": "unknown",
                "confidence_level": "low"
            }
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Convert confidence score to confidence level."""
        if confidence > self.high_confidence_threshold:
            return "high"
        elif confidence > self.medium_confidence_threshold:
            return "medium"
        else:
            return "low"
    
    def _get_default_classification(self) -> Dict[str, Any]:
        """Return default classification when errors occur."""
        return {
            "classification_results": {
                "product_search": 0.0,
                "price_negotiation": 0.0,
                "verification": 0.0,
                "supply_chain": 0.0,
                "translation": 0.0,
                "technical": 0.0,
                "strategic": 0.0,
                "sensitive": 0.0
            },
            "confidence": 0.0,
            "routing_decision": {
                "assigned_agents": ["human_agent"],
                "routing_logic": "escalate to human",
                "primary_category": "unknown",
                "confidence_level": "low"
            }
        } 