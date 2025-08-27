from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

# Enums
class RequestStatus(str, Enum):
    """Enumeration for request processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentType(str, Enum):
    """Enumeration for AI agent types."""
    TECHNICAL = "technical"
    STRATEGIC = "strategic"
    SENSITIVE = "sensitive"
    HUMAN = "human"

# Core Models
class User(BaseModel):
    """
    Core user model for the SEEKER system.
    
    Represents a user in the system with their profile and device registrations.
    """
    user_id: str = Field(
        ..., 
        min_length=1,
        max_length=100,
        description="Unique identifier for the user"
    )
    personal_profile: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Personal profile information"
    )
    device_registrations: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="List of device registrations"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, 
        description="Timestamp of creation"
    )
    updated_at: Optional[datetime] = Field(
        default=None, 
        description="Timestamp of last update"
    )
    
    @validator('user_id')
    def validate_user_id(cls, v):
        """Validate user ID format."""
        if not v.isalnum() and '_' not in v:
            raise ValueError('User ID must contain only alphanumeric characters and underscores')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_12345",
                "personal_profile": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "preferences": {"language": "en", "timezone": "UTC"}
                },
                "device_registrations": [
                    {"device_id": "device_67890", "type": "laptop"}
                ]
            }
        }

class Task_Request(BaseModel):
    """
    Core task request model for the SEEKER orchestration system.
    
    Represents a user's request that needs to be processed by AI agents.
    """
    request_id: str = Field(
        ..., 
        description="Unique identifier for the task request"
    )
    user_id: str = Field(
        ..., 
        description="ID of the user making the request"
    )
    input_text: Optional[str] = Field(
        default=None, 
        max_length=10000,
        description="Text input for the task request"
    )
    input_audio: Optional[bytes] = Field(
        default=None, 
        description="Audio input for the task request (as bytes)"
    )
    classification_results: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Results from classification models"
    )
    routing_decision: Optional[str] = Field(
        default=None, 
        description="Routing decision for the request"
    )
    status: RequestStatus = Field(
        default=RequestStatus.PENDING,
        description="Current status of the request"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, 
        description="Timestamp of creation"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of last update"
    )
    
    @validator('input_text')
    def validate_input_text(cls, v):
        """Validate that input text is not just whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError('Input text cannot be empty or only whitespace')
        return v.strip() if v else v
    
    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "req_abc123def456",
                "user_id": "user_12345",
                "input_text": "Can you help me optimize this Python function for better performance?",
                "classification_results": {
                    "technical": 0.85,
                    "strategic": 0.12,
                    "sensitive": 0.03
                },
                "routing_decision": "auto-route",
                "status": "processing"
            }
        }

class Agent_Response(BaseModel):
    """
    Core agent response model for the SEEKER orchestration system.
    
    Represents a response from an AI agent to a task request.
    """
    response_id: str = Field(
        ..., 
        description="Unique identifier for the agent response"
    )
    request_id: str = Field(
        ..., 
        description="ID of the related task request"
    )
    agent_id: str = Field(
        ..., 
        description="ID of the responding agent"
    )
    agent_type: AgentType = Field(
        ..., 
        description="Type of the AI agent"
    )
    response_content: str = Field(
        ..., 
        min_length=1,
        max_length=50000,
        description="Content of the agent's response"
    )
    response_confidence: float = Field(
        ..., 
        ge=0.0,
        le=1.0,
        description="Confidence score of the response"
    )
    processing_time: float = Field(
        ..., 
        ge=0.0,
        description="Time taken to process the request (in seconds)"
    )
    vector_embedding: List[float] = Field(
        default_factory=list, 
        description="Vector embedding of the response"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata about the response"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, 
        description="Timestamp of creation"
    )
    
    @validator('response_confidence')
    def validate_confidence(cls, v):
        """Validate confidence is within valid range."""
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return round(v, 3)
    
    @validator('processing_time')
    def validate_processing_time(cls, v):
        """Validate processing time is positive."""
        if v < 0:
            raise ValueError('Processing time must be non-negative')
        return round(v, 3)
    
    @validator('response_content')
    def validate_response_content(cls, v):
        """Validate that response content is not just whitespace."""
        if not v.strip():
            raise ValueError('Response content cannot be empty or only whitespace')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "response_id": "resp_xyz789abc123",
                "request_id": "req_abc123def456",
                "agent_id": "technical_ai_agent",
                "agent_type": "technical",
                "response_content": "Based on your code analysis request, I've identified several optimization opportunities...",
                "response_confidence": 0.92,
                "processing_time": 2.34,
                "metadata": {
                    "model_version": "v2.1",
                    "tokens_used": 1500
                }
            }
        }

class Device(BaseModel):
    """
    Core device model for the SEEKER system.
    
    Represents a device registered by a user in the system.
    """
    device_id: str = Field(
        ..., 
        description="Unique identifier for the device"
    )
    user_id: str = Field(
        ..., 
        description="ID of the user who owns the device"
    )
    device_type: str = Field(
        ..., 
        description="Type of the device (e.g., phone, tablet, laptop)"
    )
    hardware_specs: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Hardware specifications of the device"
    )
    registration_date: datetime = Field(
        default_factory=datetime.utcnow, 
        description="Date the device was registered"
    )
    last_active: Optional[datetime] = Field(
        default=None, 
        description="Last active timestamp of the device"
    )
    
    @validator('device_id')
    def validate_device_id(cls, v):
        """Validate device ID format."""
        if not v.isalnum() and '_' not in v:
            raise ValueError('Device ID must contain only alphanumeric characters and underscores')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "device_67890",
                "user_id": "user_12345",
                "device_type": "laptop",
                "hardware_specs": {
                    "os": "Windows 11",
                    "cpu": "Intel i7",
                    "ram": "16GB"
                }
            }
        } 