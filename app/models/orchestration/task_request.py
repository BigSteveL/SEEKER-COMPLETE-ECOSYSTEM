from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class Task_Request(BaseModel):
    request_id: str = Field(..., description="Unique identifier for the request")
    user_id: str = Field(..., description="ID of the user making the request") 
    input_text: str = Field(..., description="Text input from the user")
    input_audio: Optional[bytes] = Field(default=None, description="Audio input from the user")
    classification_results: Optional[Dict[str, float]] = Field(default=None, description="Classification results")
    routing_decision: Optional[Dict[str, Any]] = Field(default=None, description="Routing decision made by the system")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when request was created") 