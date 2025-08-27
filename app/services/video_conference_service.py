import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Any
from collections import defaultdict
import uuid

from app.models.video_conference import (
    VideoConference, Participant, ConferenceStatus, ParticipantRole,
    TranslationMode, ConferenceMessage, WebRTCOffer, WebRTCAnswer, ICECandidate,
    TranslationRequest, TranslationResponse, ConferenceStats
)
from app.services.classification_engine import TaskClassificationEngine as ClassificationEngine
from app.services.agent_router import AgentRouter

logger = logging.getLogger(__name__)


class VideoConferenceService:
    """Service for managing video conferences with real-time translation"""
    
    def __init__(self):
        self.conferences: Dict[str, VideoConference] = {}
        self.participant_sessions: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.webrtc_connections: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.translation_cache: Dict[str, Dict[str, str]] = defaultdict(dict)
        self.classification_engine = ClassificationEngine()
        self.agent_router = AgentRouter()
        
        # WebSocket connection management
        self.active_connections: Dict[str, Set[str]] = defaultdict(set)
        self.connection_participants: Dict[str, str] = {}
        
        # Real-time translation settings
        self.supported_languages = {
            "en-US": "English",
            "es-ES": "Spanish", 
            "fr-FR": "French",
            "de-DE": "German",
            "it-IT": "Italian",
            "pt-BR": "Portuguese",
            "ru-RU": "Russian",
            "ja-JP": "Japanese",
            "ko-KR": "Korean",
            "zh-CN": "Chinese"
        }
        
        # Background tasks will be started when needed
        # asyncio.create_task(self._cleanup_expired_conferences())
        # asyncio.create_task(self._monitor_connection_quality())

    async def create_conference(self, request_data: Dict[str, Any]) -> VideoConference:
        """Create a new video conference"""
        try:
            conference = VideoConference(
                title=request_data["title"],
                description=request_data.get("description"),
                host_id=request_data["host_id"],
                scheduled_start=request_data["scheduled_start"],
                scheduled_end=request_data.get("scheduled_end"),
                max_participants=request_data.get("max_participants", 10),
                languages=request_data.get("languages", ["en-US"]),
                translation_enabled=request_data.get("translation_enabled", True),
                recording_enabled=request_data.get("recording_enabled", False),
                negotiation_type=request_data.get("negotiation_type"),
                parties_involved=request_data.get("parties_involved", []),
                estimated_duration=request_data.get("estimated_duration")
            )
            
            self.conferences[conference.id] = conference
            logger.info(f"Created conference {conference.id}: {conference.title}")
            
            return conference
            
        except Exception as e:
            logger.error(f"Error creating conference: {e}")
            raise

    async def join_conference(self, conference_id: str, participant_data: Dict[str, Any]) -> Participant:
        """Join a participant to a conference"""
        try:
            if conference_id not in self.conferences:
                raise ValueError(f"Conference {conference_id} not found")
            
            conference = self.conferences[conference_id]
            
            # Check if conference is full
            if len(conference.participants) >= conference.max_participants:
                raise ValueError("Conference is full")
            
            # Check if conference is active or scheduled
            if conference.status not in [ConferenceStatus.SCHEDULED, ConferenceStatus.ACTIVE]:
                raise ValueError(f"Cannot join conference with status: {conference.status}")
            
            # Create participant
            participant = Participant(
                user_id=participant_data["user_id"],
                name=participant_data["name"],
                email=participant_data["email"],
                role=ParticipantRole(participant_data["role"]),
                language=participant_data.get("language", "en-US"),
                timezone=participant_data.get("timezone", "UTC"),
                is_host=participant_data.get("is_host", False),
                joined_at=datetime.utcnow()
            )
            
            # Add to conference
            conference.participants.append(participant)
            conference.updated_at = datetime.utcnow()
            
            # Initialize session data
            self.participant_sessions[conference_id][participant.id] = {
                "joined_at": datetime.utcnow(),
                "last_activity": datetime.utcnow(),
                "connection_quality": 1.0,
                "translation_requests": 0,
                "messages_sent": 0
            }
            
            # Start conference if first participant joins
            if len(conference.participants) == 1 and conference.status == ConferenceStatus.SCHEDULED:
                conference.status = ConferenceStatus.ACTIVE
                conference.actual_start = datetime.utcnow()
            
            logger.info(f"Participant {participant.name} joined conference {conference_id}")
            return participant
            
        except Exception as e:
            logger.error(f"Error joining conference: {e}")
            raise

    async def leave_conference(self, conference_id: str, participant_id: str) -> bool:
        """Remove participant from conference"""
        try:
            if conference_id not in self.conferences:
                return False
            
            conference = self.conferences[conference_id]
            participant = next((p for p in conference.participants if p.id == participant_id), None)
            
            if not participant:
                return False
            
            # Update participant
            participant.left_at = datetime.utcnow()
            participant.is_speaking = False
            
            # Remove from active participants
            conference.participants = [p for p in conference.participants if p.id != participant_id]
            
            # Clean up session data
            if participant_id in self.participant_sessions[conference_id]:
                del self.participant_sessions[conference_id][participant_id]
            
            # End conference if no participants left
            if len(conference.participants) == 0:
                conference.status = ConferenceStatus.ENDED
                conference.actual_end = datetime.utcnow()
            
            conference.updated_at = datetime.utcnow()
            
            logger.info(f"Participant {participant.name} left conference {conference_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error leaving conference: {e}")
            return False

    async def handle_webrtc_offer(self, offer_data: WebRTCOffer) -> bool:
        """Handle WebRTC offer from participant"""
        try:
            conference_id = offer_data.conference_id
            if conference_id not in self.conferences:
                return False
            
            # Store offer for signaling
            if conference_id not in self.webrtc_connections:
                self.webrtc_connections[conference_id] = {}
            
            connection_key = f"{offer_data.from_participant_id}_{offer_data.to_participant_id}"
            self.webrtc_connections[conference_id][connection_key] = {
                "offer": offer_data.offer,
                "timestamp": offer_data.timestamp,
                "status": "pending"
            }
            
            logger.info(f"WebRTC offer stored for {connection_key} in conference {conference_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error handling WebRTC offer: {e}")
            return False

    async def handle_webrtc_answer(self, answer_data: WebRTCAnswer) -> bool:
        """Handle WebRTC answer from participant"""
        try:
            conference_id = answer_data.conference_id
            if conference_id not in self.conferences:
                return False
            
            connection_key = f"{answer_data.from_participant_id}_{answer_data.to_participant_id}"
            
            if conference_id in self.webrtc_connections and connection_key in self.webrtc_connections[conference_id]:
                self.webrtc_connections[conference_id][connection_key]["answer"] = answer_data.answer
                self.webrtc_connections[conference_id][connection_key]["status"] = "connected"
                
                logger.info(f"WebRTC connection established for {connection_key} in conference {conference_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error handling WebRTC answer: {e}")
            return False

    async def handle_ice_candidate(self, candidate_data: ICECandidate) -> bool:
        """Handle ICE candidate for WebRTC connection"""
        try:
            conference_id = candidate_data.conference_id
            if conference_id not in self.conferences:
                return False
            
            connection_key = f"{candidate_data.from_participant_id}_{candidate_data.to_participant_id}"
            
            if conference_id not in self.webrtc_connections:
                self.webrtc_connections[conference_id] = {}
            
            if connection_key not in self.webrtc_connections[conference_id]:
                self.webrtc_connections[conference_id][connection_key] = {}
            
            if "ice_candidates" not in self.webrtc_connections[conference_id][connection_key]:
                self.webrtc_connections[conference_id][connection_key]["ice_candidates"] = []
            
            self.webrtc_connections[conference_id][connection_key]["ice_candidates"].append(
                candidate_data.candidate
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error handling ICE candidate: {e}")
            return False

    async def process_translation_request(self, request: TranslationRequest) -> TranslationResponse:
        """Process real-time translation request"""
        try:
            # Check if translation is cached
            cache_key = f"{request.source_language}_{request.target_language}_{request.original_text}"
            if cache_key in self.translation_cache[request.conference_id]:
                translated_text = self.translation_cache[request.conference_id][cache_key]
                confidence = 0.95  # High confidence for cached translations
            else:
                # Use SEEKER's classification and translation capabilities
                classification_result = self.classification_engine.classify_request(
                    request.original_text
                )
                
                # Generate translation based on SEEKER's translation category
                if classification_result["routing_decision"]["primary_category"] == "translation":
                    translated_text = await self._generate_translation(
                        request.original_text,
                        request.source_language,
                        request.target_language
                    )
                    confidence = 0.85
                else:
                    # Fallback translation
                    translated_text = await self._fallback_translation(
                        request.original_text,
                        request.source_language,
                        request.target_language
                    )
                    confidence = 0.75
                
                # Cache the translation
                self.translation_cache[request.conference_id][cache_key] = translated_text
            
            # Create translation response
            response = TranslationResponse(
                request_id=str(uuid.uuid4()),
                conference_id=request.conference_id,
                participant_id=request.participant_id,
                original_text=request.original_text,
                translated_text=translated_text,
                source_language=request.source_language,
                target_language=request.target_language,
                confidence=confidence
            )
            
            # Update participant session stats
            if request.conference_id in self.participant_sessions:
                if request.participant_id in self.participant_sessions[request.conference_id]:
                    self.participant_sessions[request.conference_id][request.participant_id]["translation_requests"] += 1
            
            logger.info(f"Translation processed for participant {request.participant_id} in conference {request.conference_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing translation request: {e}")
            # Return fallback response
            return TranslationResponse(
                request_id=str(uuid.uuid4()),
                conference_id=request.conference_id,
                participant_id=request.participant_id,
                original_text=request.original_text,
                translated_text=request.original_text,  # Return original as fallback
                source_language=request.source_language,
                target_language=request.target_language,
                confidence=0.0
            )

    async def _generate_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """Generate translation using SEEKER's AI capabilities"""
        try:
            # This would integrate with SEEKER's translation service
            # For now, return a placeholder translation
            translation_map = {
                ("en-US", "es-ES"): {
                    "hello": "hola",
                    "goodbye": "adiós",
                    "thank you": "gracias",
                    "price": "precio",
                    "negotiation": "negociación"
                },
                ("es-ES", "en-US"): {
                    "hola": "hello",
                    "adiós": "goodbye", 
                    "gracias": "thank you",
                    "precio": "price",
                    "negociación": "negotiation"
                }
            }
            
            key = (source_lang, target_lang)
            if key in translation_map:
                return translation_map[key].get(text.lower(), text)
            
            return text  # Return original if no translation available
            
        except Exception as e:
            logger.error(f"Error generating translation: {e}")
            return text

    async def _fallback_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """Fallback translation method"""
        # Simple word replacement for common negotiation terms
        common_terms = {
            "price": "precio" if target_lang == "es-ES" else "prix" if target_lang == "fr-FR" else text,
            "negotiate": "negociar" if target_lang == "es-ES" else "négocier" if target_lang == "fr-FR" else text,
            "contract": "contrato" if target_lang == "es-ES" else "contrat" if target_lang == "fr-FR" else text,
            "payment": "pago" if target_lang == "es-ES" else "paiement" if target_lang == "fr-FR" else text
        }
        
        return common_terms.get(text.lower(), text)

    async def get_conference_stats(self, conference_id: str) -> Optional[ConferenceStats]:
        """Get conference statistics"""
        try:
            if conference_id not in self.conferences:
                return None
            
            conference = self.conferences[conference_id]
            session_data = self.participant_sessions.get(conference_id, {})
            
            # Calculate stats
            total_participants = len(conference.participants)
            active_participants = len([p for p in conference.participants if not p.left_at])
            
            duration_minutes = 0
            if conference.actual_start:
                end_time = conference.actual_end or datetime.utcnow()
                duration_minutes = int((end_time - conference.actual_start).total_seconds() / 60)
            
            messages_sent = sum(session.get("messages_sent", 0) for session in session_data.values())
            translations_processed = sum(session.get("translation_requests", 0) for session in session_data.values())
            
            avg_connection_quality = 1.0
            if session_data:
                qualities = [session.get("connection_quality", 1.0) for session in session_data.values()]
                avg_connection_quality = sum(qualities) / len(qualities)
            
            languages_used = list(set(p.language for p in conference.participants))
            
            return ConferenceStats(
                conference_id=conference_id,
                total_participants=total_participants,
                active_participants=active_participants,
                duration_minutes=duration_minutes,
                messages_sent=messages_sent,
                translations_processed=translations_processed,
                average_connection_quality=avg_connection_quality,
                languages_used=languages_used
            )
            
        except Exception as e:
            logger.error(f"Error getting conference stats: {e}")
            return None

    async def _cleanup_expired_conferences(self):
        """Background task to cleanup expired conferences"""
        while True:
            try:
                current_time = datetime.utcnow()
                expired_conferences = []
                
                for conference_id, conference in self.conferences.items():
                    # Remove conferences that ended more than 24 hours ago
                    if (conference.status == ConferenceStatus.ENDED and 
                        conference.actual_end and 
                        current_time - conference.actual_end > timedelta(hours=24)):
                        expired_conferences.append(conference_id)
                
                for conference_id in expired_conferences:
                    del self.conferences[conference_id]
                    if conference_id in self.participant_sessions:
                        del self.participant_sessions[conference_id]
                    if conference_id in self.webrtc_connections:
                        del self.webrtc_connections[conference_id]
                    if conference_id in self.translation_cache:
                        del self.translation_cache[conference_id]
                    
                    logger.info(f"Cleaned up expired conference {conference_id}")
                
                await asyncio.sleep(3600)  # Run every hour
                
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")
                await asyncio.sleep(3600)

    async def _monitor_connection_quality(self):
        """Background task to monitor connection quality"""
        while True:
            try:
                for conference_id, sessions in self.participant_sessions.items():
                    for participant_id, session in sessions.items():
                        # Simulate connection quality monitoring
                        # In a real implementation, this would check actual WebRTC stats
                        session["connection_quality"] = max(0.5, session.get("connection_quality", 1.0) - 0.01)
                        
                        # Update participant connection quality
                        if conference_id in self.conferences:
                            conference = self.conferences[conference_id]
                            participant = next((p for p in conference.participants if p.id == participant_id), None)
                            if participant:
                                participant.connection_quality = session["connection_quality"]
                
                await asyncio.sleep(30)  # Run every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in connection monitoring: {e}")
                await asyncio.sleep(30)

    def get_conference(self, conference_id: str) -> Optional[VideoConference]:
        """Get conference by ID"""
        return self.conferences.get(conference_id)

    def get_all_conferences(self) -> List[VideoConference]:
        """Get all conferences"""
        return list(self.conferences.values())

    def get_active_conferences(self) -> List[VideoConference]:
        """Get active conferences"""
        return [c for c in self.conferences.values() if c.status == ConferenceStatus.ACTIVE] 