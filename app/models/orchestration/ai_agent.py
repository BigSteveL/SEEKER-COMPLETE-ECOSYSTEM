from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class AI_Agent(BaseModel):
    agent_id: str = Field(..., description="Unique identifier for the AI agent")
    agent_type: str = Field(..., description="Type/category of the AI agent")
    capabilities: List[str] = Field(default_factory=list, description="List of capabilities of the agent")
    performance_metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics for the agent")
    routing_weights: Dict[str, float] = Field(default_factory=dict, description="Routing weights for orchestration")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of creation") 