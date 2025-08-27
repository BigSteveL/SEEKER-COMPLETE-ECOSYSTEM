from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class User(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    personal_profile: Dict[str, Any] = Field(default_factory=dict, description="Personal profile information")
    device_registrations: List[Dict[str, Any]] = Field(default_factory=list, description="List of device registrations")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of creation")
    updated_at: Optional[datetime] = Field(default=None, description="Timestamp of last update") 