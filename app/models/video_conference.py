from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class ParticipantRole(str, Enum):
    """Participant roles in video conference"""
    NEGOTIATOR = "negotiator"
    BUYER = "buyer"
    SELLER = "seller"
    MEDIATOR = "mediator"
    OBSERVER = "observer"
    TRANSLATOR = "translator"


class ConferenceStatus(str, Enum):
    """Video conference status"""
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"
    CANCELLED = "cancelled"


class TranslationMode(str, Enum):
    """Real-time translation modes"""
    SIMULTANEOUS = "simultaneous"  # Real-time voice translation
    SUBTITLE = "subtitle"          # Text subtitles
    HYBRID = "hybrid"              # Both voice and text
    OFF = "off"                    # No translation


class Participant(BaseModel):
    """Video conference participant model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    email: str
    role: ParticipantRole
    language: str = "en-US"
    timezone: str = "UTC"
    is_host: bool = False
    is_muted: bool = False
    is_video_enabled: bool = True
    is_speaking: bool = False
    connection_quality: float = 1.0
    joined_at: Optional[datetime] = None
    left_at: Optional[datetime] = None
    webrtc_peer_id: Optional[str] = None
    translation_enabled: bool = True
    translation_mode: TranslationMode = TranslationMode.SIMULTANEOUS


class VideoConference(BaseModel):
    """Video conference room model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    host_id: str
    status: ConferenceStatus = ConferenceStatus.SCHEDULED
    scheduled_start: datetime
    scheduled_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    max_participants: int = 10
    participants: List[Participant] = []
    languages: List[str] = ["en-US"]
    translation_enabled: bool = True
    recording_enabled: bool = False
    chat_enabled: bool = True
    screen_sharing_enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # SEEKER-specific fields
    negotiation_type: Optional[str] = None  # "price_negotiation", "contract_review", etc.
    parties_involved: List[str] = []  # Company names or party identifiers
    estimated_duration: Optional[int] = None  # minutes
    ai_facilitator_enabled: bool = True
    auto_translation_languages: List[str] = ["en-US", "es-ES", "fr-FR", "de-DE", "zh-CN"]


class ConferenceMessage(BaseModel):
    """Chat message in video conference"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conference_id: str
    sender_id: str
    sender_name: str
    message: str
    original_language: str
    translated_message: Optional[str] = None
    target_language: Optional[str] = None
    message_type: str = "text"  # "text", "system", "translation"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WebRTCOffer(BaseModel):
    """WebRTC offer/answer signaling"""
    conference_id: str
    from_participant_id: str
    to_participant_id: str
    offer: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WebRTCAnswer(BaseModel):
    """WebRTC answer signaling"""
    conference_id: str
    from_participant_id: str
    to_participant_id: str
    answer: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ICECandidate(BaseModel):
    """WebRTC ICE candidate"""
    conference_id: str
    from_participant_id: str
    to_participant_id: str
    candidate: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TranslationRequest(BaseModel):
    """Real-time translation request"""
    conference_id: str
    participant_id: str
    original_text: str
    source_language: str
    target_language: str
    translation_mode: TranslationMode
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TranslationResponse(BaseModel):
    """Real-time translation response"""
    request_id: str
    conference_id: str
    participant_id: str
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConferenceCreateRequest(BaseModel):
    """Request to create a new video conference"""
    title: str
    description: Optional[str] = None
    scheduled_start: datetime
    scheduled_end: Optional[datetime] = None
    max_participants: int = 10
    languages: List[str] = ["en-US"]
    translation_enabled: bool = True
    recording_enabled: bool = False
    negotiation_type: Optional[str] = None
    parties_involved: List[str] = []
    estimated_duration: Optional[int] = None


class ConferenceJoinRequest(BaseModel):
    """Request to join a video conference"""
    conference_id: str
    user_id: str
    name: str
    email: str
    role: ParticipantRole
    language: str = "en-US"
    timezone: str = "UTC"


class ConferenceUpdateRequest(BaseModel):
    """Request to update conference settings"""
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    max_participants: Optional[int] = None
    languages: Optional[List[str]] = None
    translation_enabled: Optional[bool] = None
    recording_enabled: Optional[bool] = None
    status: Optional[ConferenceStatus] = None


class ConferenceStats(BaseModel):
    """Conference statistics"""
    conference_id: str
    total_participants: int
    active_participants: int
    duration_minutes: int
    messages_sent: int
    translations_processed: int
    recording_duration: Optional[int] = None
    average_connection_quality: float
    languages_used: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow) 