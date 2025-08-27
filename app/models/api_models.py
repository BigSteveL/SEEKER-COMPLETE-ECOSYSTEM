from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class RequestStatus(str, Enum):
    """Enumeration for request processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class UserRequestModel(BaseModel):
    """
    Model for user request input to the SEEKER orchestration system.
    
    This model represents the initial request from a user, including
    the input text and associated metadata for processing.
    """
    
    input_text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The text input from the user to be processed by the AI agents",
        example="I need help analyzing this code for performance optimization"
    )
    
    user_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique identifier for the user making the request",
        example="user_12345"
    )
    
    device_id: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional device identifier for tracking and context",
        example="device_67890"
    )
    
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional context information for enhanced processing",
        example={
            "session_id": "sess_abc123",
            "user_preferences": {"language": "en", "timezone": "UTC"},
            "previous_requests": ["req_001", "req_002"]
        }
    )
    
    @validator('input_text')
    def validate_input_text(cls, v):
        """Validate that input text is not just whitespace."""
        if not v.strip():
            raise ValueError('Input text cannot be empty or only whitespace')
        return v.strip()
    
    @validator('user_id')
    def validate_user_id(cls, v):
        """Validate user ID format."""
        if not v.isalnum() and '_' not in v:
            raise ValueError('User ID must contain only alphanumeric characters and underscores')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "input_text": "Can you help me optimize this Python function for better performance?",
                "user_id": "user_12345",
                "device_id": "device_67890",
                "context": {
                    "session_id": "sess_abc123",
                    "user_preferences": {"language": "en", "timezone": "UTC"},
                    "previous_requests": ["req_001", "req_002"]
                }
            }
        }

class ProcessingResponseModel(BaseModel):
    """
    Model for the initial processing response from the SEEKER system.
    
    This model is returned immediately after request classification and routing,
    providing the user with processing status and routing information.
    """
    
    request_id: str = Field(
        ...,
        description="Unique identifier for the processing request",
        example="req_abc123def456"
    )
    
    status: RequestStatus = Field(
        ...,
        description="Current status of the request processing",
        example=RequestStatus.PROCESSING
    )
    
    classification_results: Dict[str, Any] = Field(
        ...,
        description="Results from the classification engine including category scores and confidence",
        example={
            "technical": 0.85,
            "strategic": 0.12,
            "sensitive": 0.03,
            "primary_category": "technical",
            "confidence": 0.87
        }
    )
    
    routing_decision: Dict[str, Any] = Field(
        ...,
        description="Routing decision including assigned agents and logic",
        example={
            "assigned_agents": ["technical_ai_agent"],
            "routing_logic": "auto-route",
            "primary_category": "technical",
            "confidence": 0.87,
            "estimated_processing_time": 3.5
        }
    )
    
    estimated_response_time: str = Field(
        ...,
        description="Estimated time for complete response in human-readable format",
        example="3-5 seconds"
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall confidence score for the classification and routing decision",
        example=0.87
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the processing response was generated"
    )
    
    message: str = Field(
        default="Request accepted and being processed",
        description="Human-readable message about the processing status"
    )
    
    @validator('confidence')
    def validate_confidence(cls, v):
        """Validate confidence is within valid range."""
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return round(v, 3)
    
    @validator('estimated_response_time')
    def validate_response_time(cls, v):
        """Validate response time format."""
        if not v or len(v.strip()) == 0:
            raise ValueError('Estimated response time cannot be empty')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "req_abc123def456",
                "status": "processing",
                "classification_results": {
                    "technical": 0.85,
                    "strategic": 0.12,
                    "sensitive": 0.03,
                    "primary_category": "technical",
                    "confidence": 0.87
                },
                "routing_decision": {
                    "assigned_agents": ["technical_ai_agent"],
                    "routing_logic": "auto-route",
                    "primary_category": "technical",
                    "confidence": 0.87,
                    "estimated_processing_time": 3.5
                },
                "estimated_response_time": "3-5 seconds",
                "confidence": 0.87,
                "timestamp": "2024-01-15T10:30:00Z",
                "message": "Request accepted and being processed"
            }
        }

class AgentResponseModel(BaseModel):
    """
    Model for individual AI agent responses.
    
    This model represents the response from a single AI agent,
    including the response content and performance metrics.
    """
    
    response_id: str = Field(
        ...,
        description="Unique identifier for the agent response",
        example="resp_xyz789abc123"
    )
    
    agent_id: str = Field(
        ...,
        description="Identifier of the AI agent that generated this response",
        example="technical_ai_agent"
    )
    
    response_content: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="The actual response content from the AI agent",
        example="Based on your code analysis request, I've identified several optimization opportunities..."
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for this specific agent response",
        example=0.92
    )
    
    processing_time: float = Field(
        ...,
        ge=0.0,
        description="Time taken by this agent to process the request in seconds",
        example=2.34
    )
    
    agent_type: Optional[str] = Field(
        default=None,
        description="Type/category of the AI agent",
        example="technical"
    )
    
    capabilities_used: Optional[List[str]] = Field(
        default=None,
        description="List of capabilities used by the agent for this response",
        example=["code_analysis", "performance_optimization"]
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata about the response",
        example={
            "model_version": "v2.1",
            "tokens_used": 1500,
            "temperature": 0.7
        }
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the agent response was generated"
    )
    
    @validator('confidence')
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
        """Validate response content is not just whitespace."""
        if not v.strip():
            raise ValueError('Response content cannot be empty or only whitespace')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "response_id": "resp_xyz789abc123",
                "agent_id": "technical_ai_agent",
                "response_content": "Based on your code analysis request, I've identified several optimization opportunities. The main bottleneck appears to be in the nested loop structure...",
                "confidence": 0.92,
                "processing_time": 2.34,
                "agent_type": "technical",
                "capabilities_used": ["code_analysis", "performance_optimization"],
                "metadata": {
                    "model_version": "v2.1",
                    "tokens_used": 1500,
                    "temperature": 0.7
                },
                "timestamp": "2024-01-15T10:30:02Z"
            }
        }

class CompleteResponseModel(BaseModel):
    """
    Model for the complete response including all agent responses.
    
    This model represents the final response after all agents have processed
    the request, providing a comprehensive view of all responses.
    """
    
    request_id: str = Field(
        ...,
        description="Unique identifier for the original request",
        example="req_abc123def456"
    )
    
    status: RequestStatus = Field(
        ...,
        description="Final status of the request processing",
        example=RequestStatus.COMPLETED
    )
    
    agent_responses: List[AgentResponseModel] = Field(
        ...,
        description="List of responses from all assigned AI agents"
    )
    
    total_processing_time: float = Field(
        ...,
        ge=0.0,
        description="Total time taken for all agents to process the request",
        example=4.67
    )
    
    average_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Average confidence across all agent responses",
        example=0.89
    )
    
    summary: Optional[str] = Field(
        default=None,
        description="Optional summary of all agent responses",
        example="Technical analysis completed with high confidence. Strategic insights provided for business context."
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the complete response was assembled"
    )
    
    @validator('average_confidence')
    def validate_average_confidence(cls, v):
        """Validate average confidence is within valid range."""
        if not 0.0 <= v <= 1.0:
            raise ValueError('Average confidence must be between 0.0 and 1.0')
        return round(v, 3)
    
    @validator('total_processing_time')
    def validate_total_processing_time(cls, v):
        """Validate total processing time is positive."""
        if v < 0:
            raise ValueError('Total processing time must be non-negative')
        return round(v, 3)
    
    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "req_abc123def456",
                "status": "completed",
                "agent_responses": [
                    {
                        "response_id": "resp_xyz789abc123",
                        "agent_id": "technical_ai_agent",
                        "response_content": "Technical analysis completed...",
                        "confidence": 0.92,
                        "processing_time": 2.34
                    }
                ],
                "total_processing_time": 4.67,
                "average_confidence": 0.89,
                "summary": "Technical analysis completed with high confidence.",
                "timestamp": "2024-01-15T10:30:05Z"
            }
        } 

class ResponseModel(BaseModel):
    """
    Simple response model for general API responses.
    """
    success: bool = Field(
        ...,
        description="Whether the operation was successful"
    )
    
    message: str = Field(
        ...,
        description="Human-readable message about the operation result"
    )
    
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional data payload"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the response was generated"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {"result": "example_data"},
                "timestamp": "2024-01-15T10:30:00Z"
            }
        } 