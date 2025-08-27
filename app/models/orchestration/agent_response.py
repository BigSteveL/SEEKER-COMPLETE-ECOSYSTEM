from pydantic import BaseModel, Field
from typing import Any, List
from datetime import datetime

class Agent_Response(BaseModel):
    response_id: str = Field(..., description="Unique identifier for the agent response")
    request_id: str = Field(..., description="ID of the related task request")
    agent_id: str = Field(..., description="ID of the responding agent")
    response_content: Any = Field(..., description="Content of the agent's response")
    response_confidence: float = Field(..., description="Confidence score of the response")
    processing_time: float = Field(..., description="Time taken to process the request (in seconds)")
    vector_embedding: List[float] = Field(default_factory=list, description="Vector embedding of the response")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of creation") 