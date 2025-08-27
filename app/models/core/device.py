from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class Device(BaseModel):
    device_id: str = Field(..., description="Unique identifier for the device")
    user_id: str = Field(..., description="ID of the user who owns the device")
    device_type: str = Field(..., description="Type of the device (e.g., phone, tablet, laptop)")
    hardware_specs: Dict[str, Any] = Field(default_factory=dict, description="Hardware specifications of the device")
    registration_date: datetime = Field(default_factory=datetime.utcnow, description="Date the device was registered")
    last_active: Optional[datetime] = Field(default=None, description="Last active timestamp of the device") 