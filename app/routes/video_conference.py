from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import json
import logging
from datetime import datetime
from collections import defaultdict

from app.models.video_conference import (
    VideoConference, Participant, ConferenceStatus, ParticipantRole,
    TranslationMode, ConferenceMessage, WebRTCOffer, WebRTCAnswer, ICECandidate,
    TranslationRequest, TranslationResponse, ConferenceStats,
    ConferenceCreateRequest, ConferenceJoinRequest, ConferenceUpdateRequest
)
from app.services.video_conference_service import VideoConferenceService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/video-conference", tags=["Video Conference"])

# Initialize video conference service
video_service = VideoConferenceService()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = defaultdict(dict)
    
    async def connect(self, websocket: WebSocket, conference_id: str, participant_id: str):
        await websocket.accept()
        self.active_connections[conference_id][participant_id] = websocket
        logger.info(f"WebSocket connected: participant {participant_id} in conference {conference_id}")
    
    def disconnect(self, conference_id: str, participant_id: str):
        if conference_id in self.active_connections and participant_id in self.active_connections[conference_id]:
            del self.active_connections[conference_id][participant_id]
            logger.info(f"WebSocket disconnected: participant {participant_id} from conference {conference_id}")
    
    async def send_personal_message(self, message: str, conference_id: str, participant_id: str):
        if conference_id in self.active_connections and participant_id in self.active_connections[conference_id]:
            await self.active_connections[conference_id][participant_id].send_text(message)
    
    async def broadcast_to_conference(self, message: str, conference_id: str, exclude_participant: Optional[str] = None):
        if conference_id in self.active_connections:
            for participant_id, connection in self.active_connections[conference_id].items():
                if participant_id != exclude_participant:
                    try:
                        await connection.send_text(message)
                    except Exception as e:
                        logger.error(f"Error broadcasting to {participant_id}: {e}")

manager = ConnectionManager()


@router.post("/conferences/", response_model=VideoConference)
async def create_conference(request: ConferenceCreateRequest, background_tasks: BackgroundTasks):
    """Create a new video conference for SEEKER negotiations"""
    try:
        request_data = request.dict()
        request_data["host_id"] = "system"  # In a real app, this would be the authenticated user
        
        conference = await video_service.create_conference(request_data)
        
        logger.info(f"📹 Created video conference: {conference.id} - {conference.title}")
        
        return conference
        
    except Exception as e:
        logger.error(f"Error creating conference: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conferences/", response_model=List[VideoConference])
async def list_conferences():
    """List all video conferences"""
    try:
        conferences = video_service.get_all_conferences()
        return conferences
        
    except Exception as e:
        logger.error(f"Error listing conferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conferences/active/", response_model=List[VideoConference])
async def list_active_conferences():
    """List active video conferences"""
    try:
        conferences = video_service.get_active_conferences()
        return conferences
        
    except Exception as e:
        logger.error(f"Error listing active conferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conferences/{conference_id}", response_model=VideoConference)
async def get_conference(conference_id: str):
    """Get conference details"""
    try:
        conference = video_service.get_conference(conference_id)
        if not conference:
            raise HTTPException(status_code=404, detail="Conference not found")
        
        return conference
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conference: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conferences/{conference_id}/join", response_model=Participant)
async def join_conference(conference_id: str, request: ConferenceJoinRequest):
    """Join a video conference"""
    try:
        participant_data = request.dict()
        participant_data["conference_id"] = conference_id
        
        participant = await video_service.join_conference(conference_id, participant_data)
        
        logger.info(f"👥 Participant {participant.name} joined conference {conference_id}")
        
        return participant
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error joining conference: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conferences/{conference_id}/leave/{participant_id}")
async def leave_conference(conference_id: str, participant_id: str):
    """Leave a video conference"""
    try:
        success = await video_service.leave_conference(conference_id, participant_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Participant or conference not found")
        
        logger.info(f"👋 Participant {participant_id} left conference {conference_id}")
        
        return {"message": "Successfully left conference"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error leaving conference: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/conferences/{conference_id}", response_model=VideoConference)
async def update_conference(conference_id: str, request: ConferenceUpdateRequest):
    """Update conference settings"""
    try:
        conference = video_service.get_conference(conference_id)
        if not conference:
            raise HTTPException(status_code=404, detail="Conference not found")
        
        # Update conference fields
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(conference, field):
                setattr(conference, field, value)
        
        conference.updated_at = datetime.utcnow()
        
        logger.info(f"📝 Updated conference {conference_id}")
        
        return conference
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating conference: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conferences/{conference_id}/stats", response_model=ConferenceStats)
async def get_conference_stats(conference_id: str):
    """Get conference statistics"""
    try:
        stats = await video_service.get_conference_stats(conference_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Conference not found")
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conference stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conferences/{conference_id}/webrtc/offer")
async def handle_webrtc_offer(conference_id: str, offer: WebRTCOffer):
    """Handle WebRTC offer for peer connection"""
    try:
        success = await video_service.handle_webrtc_offer(offer)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to process WebRTC offer")
        
        # Broadcast offer to target participant
        message = {
            "type": "webrtc_offer",
            "from_participant_id": offer.from_participant_id,
            "offer": offer.offer,
            "timestamp": offer.timestamp.isoformat()
        }
        
        await manager.send_personal_message(
            json.dumps(message),
            conference_id,
            offer.to_participant_id
        )
        
        return {"message": "WebRTC offer processed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling WebRTC offer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conferences/{conference_id}/webrtc/answer")
async def handle_webrtc_answer(conference_id: str, answer: WebRTCAnswer):
    """Handle WebRTC answer for peer connection"""
    try:
        success = await video_service.handle_webrtc_answer(answer)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to process WebRTC answer")
        
        # Broadcast answer to target participant
        message = {
            "type": "webrtc_answer",
            "from_participant_id": answer.from_participant_id,
            "answer": answer.answer,
            "timestamp": answer.timestamp.isoformat()
        }
        
        await manager.send_personal_message(
            json.dumps(message),
            conference_id,
            answer.to_participant_id
        )
        
        return {"message": "WebRTC answer processed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling WebRTC answer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conferences/{conference_id}/webrtc/ice-candidate")
async def handle_ice_candidate(conference_id: str, candidate: ICECandidate):
    """Handle ICE candidate for WebRTC connection"""
    try:
        success = await video_service.handle_ice_candidate(candidate)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to process ICE candidate")
        
        # Broadcast ICE candidate to target participant
        message = {
            "type": "ice_candidate",
            "from_participant_id": candidate.from_participant_id,
            "candidate": candidate.candidate,
            "timestamp": candidate.timestamp.isoformat()
        }
        
        await manager.send_personal_message(
            json.dumps(message),
            conference_id,
            candidate.to_participant_id
        )
        
        return {"message": "ICE candidate processed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling ICE candidate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conferences/{conference_id}/translate", response_model=TranslationResponse)
async def translate_message(conference_id: str, request: TranslationRequest):
    """Process real-time translation request"""
    try:
        response = await video_service.process_translation_request(request)
        
        logger.info(f"🌐 Translation processed for conference {conference_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing translation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws/{conference_id}/{participant_id}")
async def websocket_endpoint(websocket: WebSocket, conference_id: str, participant_id: str):
    """WebSocket endpoint for real-time video conference communication"""
    await manager.connect(websocket, conference_id, participant_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            
            if message_type == "join":
                # Participant joined notification
                join_message = {
                    "type": "participant_joined",
                    "participant_id": participant_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
                await manager.broadcast_to_conference(
                    json.dumps(join_message),
                    conference_id,
                    exclude_participant=participant_id
                )
                
            elif message_type == "chat":
                # Handle chat message
                chat_message = {
                    "type": "chat_message",
                    "participant_id": participant_id,
                    "message": message.get("message", ""),
                    "timestamp": datetime.utcnow().isoformat()
                }
                await manager.broadcast_to_conference(
                    json.dumps(chat_message),
                    conference_id
                )
                
            elif message_type == "translation_request":
                # Handle translation request
                translation_request = TranslationRequest(
                    conference_id=conference_id,
                    participant_id=participant_id,
                    original_text=message.get("text", ""),
                    source_language=message.get("source_language", "en-US"),
                    target_language=message.get("target_language", "en-US"),
                    translation_mode=TranslationMode(message.get("mode", "simultaneous"))
                )
                
                response = await video_service.process_translation_request(translation_request)
                
                # Send translation response back to requesting participant
                translation_message = {
                    "type": "translation_response",
                    "original_text": response.original_text,
                    "translated_text": response.translated_text,
                    "source_language": response.source_language,
                    "target_language": response.target_language,
                    "confidence": response.confidence,
                    "timestamp": response.timestamp.isoformat()
                }
                
                await manager.send_personal_message(
                    json.dumps(translation_message),
                    conference_id,
                    participant_id
                )
                
            elif message_type == "speaking":
                # Handle speaking indicator
                speaking_message = {
                    "type": "speaking_indicator",
                    "participant_id": participant_id,
                    "is_speaking": message.get("is_speaking", False),
                    "timestamp": datetime.utcnow().isoformat()
                }
                await manager.broadcast_to_conference(
                    json.dumps(speaking_message),
                    conference_id,
                    exclude_participant=participant_id
                )
                
            elif message_type == "connection_quality":
                # Handle connection quality update
                quality_message = {
                    "type": "connection_quality",
                    "participant_id": participant_id,
                    "quality": message.get("quality", 1.0),
                    "timestamp": datetime.utcnow().isoformat()
                }
                await manager.broadcast_to_conference(
                    json.dumps(quality_message),
                    conference_id,
                    exclude_participant=participant_id
                )
                
            else:
                # Unknown message type
                logger.warning(f"Unknown message type: {message_type}")
                
    except WebSocketDisconnect:
        manager.disconnect(conference_id, participant_id)
        
        # Notify other participants
        leave_message = {
            "type": "participant_left",
            "participant_id": participant_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        await manager.broadcast_to_conference(
            json.dumps(leave_message),
            conference_id
        )
        
        # Update participant status in service
        await video_service.leave_conference(conference_id, participant_id)
        
        logger.info(f"WebSocket disconnected: participant {participant_id} from conference {conference_id}")
        
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(conference_id, participant_id)


@router.get("/health")
async def video_conference_health():
    """Health check for video conferencing service"""
    try:
        active_conferences = len(video_service.get_active_conferences())
        total_conferences = len(video_service.get_all_conferences())
        
        return {
            "status": "healthy",
            "active_conferences": active_conferences,
            "total_conferences": total_conferences,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Video conference health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unhealthy") 