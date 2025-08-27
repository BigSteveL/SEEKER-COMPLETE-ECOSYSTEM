from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.conversation import ConversationSession, ConversationMessage
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter()

# In-memory storage for demo (replace with database)
conversations = {}

class AddMessageRequest(BaseModel):
    user_input: str
    system_response: str

@router.post("/conversations/", response_model=ConversationSession)
async def create_conversation(user_id: str):
    session_id = str(uuid.uuid4())
    conversation = ConversationSession(
        session_id=session_id,
        user_id=user_id
    )
    conversations[session_id] = conversation
    return conversation

@router.get("/conversations/{session_id}", response_model=ConversationSession)
async def get_conversation(session_id: str):
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversations[session_id]

@router.post("/conversations/{session_id}/messages/")
async def add_message(session_id: str, message_request: AddMessageRequest):
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    message = ConversationMessage(
        message_id=str(uuid.uuid4()),
        user_input=message_request.user_input,
        system_response=message_request.system_response
    )
    
    conversations[session_id].messages.append(message)
    conversations[session_id].last_activity = datetime.now()
    
    return {"status": "Message added successfully"} 