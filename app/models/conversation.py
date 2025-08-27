from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ConversationMessage(BaseModel):
    message_id: str = Field(..., description="Unique identifier for the message")
    user_input: str = Field(..., description="User's input message")
    system_response: str = Field(..., description="System's response to the user")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the message was created")

class ConversationSession(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the conversation session")
    user_id: str = Field(..., description="ID of the user in the conversation")
    messages: List[ConversationMessage] = Field(default_factory=list, description="List of messages in the conversation")
    created_at: datetime = Field(default_factory=datetime.now, description="When the conversation was created")
    last_activity: datetime = Field(default_factory=datetime.now, description="Last activity timestamp")
    status: str = Field(default="active", description="Status of the conversation (active, closed, etc.)") 