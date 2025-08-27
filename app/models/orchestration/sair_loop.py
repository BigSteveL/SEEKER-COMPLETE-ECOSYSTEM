from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime

class SAIR_Loop_Data(BaseModel):
    loop_id: str = Field(..., description="Unique identifier for the SAIR loop instance")
    request_id: str = Field(..., description="ID of the related task request")
    success_metrics: Dict[str, Any] = Field(default_factory=dict, description="Metrics indicating loop success")
    learning_updates: Dict[str, Any] = Field(default_factory=dict, description="Learning updates from the loop")
    routing_adjustments: Dict[str, Any] = Field(default_factory=dict, description="Adjustments to routing based on loop outcomes")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the loop data entry") 