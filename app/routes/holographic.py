"""
SEEKER Holographic Projector API Routes
Real-time 3D holographic displays for business presentations
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Dict, Optional
import logging
import json
import asyncio

from app.services.holographic_service import (
    holographic_service, 
    HolographicProjectionRequest,
    ProjectionType,
    HolographicDeviceType
)
from app.models.api_models import ResponseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/holographic", tags=["Holographic Projection"])

# WebSocket connections for real-time holographic streaming
holographic_connections: Dict[str, WebSocket] = {}

@router.on_event("startup")
async def startup_event():
    """Initialize holographic service on startup"""
    try:
        await holographic_service.initialize()
        logger.info("✅ Holographic service initialized on startup")
    except Exception as e:
        logger.error(f"❌ Failed to initialize holographic service: {e}")

@router.get("/devices", response_model=ResponseModel)
async def get_holographic_devices():
    """Get all available holographic devices"""
    try:
        devices = await holographic_service.get_all_devices()
        return ResponseModel(
            success=True,
            message="Holographic devices retrieved successfully",
            data={"devices": devices}
        )
    except Exception as e:
        logger.error(f"❌ Failed to get holographic devices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/devices/{device_id}", response_model=ResponseModel)
async def get_device_status(device_id: str):
    """Get status of a specific holographic device"""
    try:
        device_status = await holographic_service.get_device_status(device_id)
        if not device_status:
            raise HTTPException(status_code=404, detail="Device not found")
        
        return ResponseModel(
            success=True,
            message="Device status retrieved successfully",
            data={"device": device_status}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get device status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/projections", response_model=ResponseModel)
async def create_holographic_projection(request: HolographicProjectionRequest):
    """Create a new holographic projection"""
    try:
        projection_id = await holographic_service.create_holographic_projection(request)
        
        return ResponseModel(
            success=True,
            message="Holographic projection created successfully",
            data={
                "projection_id": projection_id,
                "device_id": request.device_id,
                "projection_type": request.projection_type.value
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Failed to create holographic projection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projections", response_model=ResponseModel)
async def get_active_projections():
    """Get all active holographic projections"""
    try:
        projections = await holographic_service.get_active_projections()
        
        return ResponseModel(
            success=True,
            message="Active projections retrieved successfully",
            data={"projections": projections}
        )
    except Exception as e:
        logger.error(f"❌ Failed to get active projections: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/projections/{projection_id}", response_model=ResponseModel)
async def update_projection(projection_id: str, updates: Dict):
    """Update an existing holographic projection"""
    try:
        success = await holographic_service.update_projection(projection_id, updates)
        
        if not success:
            raise HTTPException(status_code=404, detail="Projection not found")
        
        return ResponseModel(
            success=True,
            message="Projection updated successfully",
            data={"projection_id": projection_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to update projection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/projections/{projection_id}", response_model=ResponseModel)
async def remove_projection(projection_id: str):
    """Remove a holographic projection"""
    try:
        success = await holographic_service.remove_projection(projection_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Projection not found")
        
        return ResponseModel(
            success=True,
            message="Projection removed successfully",
            data={"projection_id": projection_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to remove projection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/projections/{projection_id}/streaming", response_model=ResponseModel)
async def start_real_time_streaming(projection_id: str, stream_config: Dict):
    """Start real-time streaming for a holographic projection"""
    try:
        success = await holographic_service.start_real_time_streaming(projection_id, stream_config)
        
        if not success:
            raise HTTPException(status_code=404, detail="Projection not found")
        
        return ResponseModel(
            success=True,
            message="Real-time streaming started successfully",
            data={
                "projection_id": projection_id,
                "stream_config": stream_config
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to start real-time streaming: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/projections/{projection_id}/collaborative", response_model=ResponseModel)
async def enable_collaborative_mode(projection_id: str, participants: List[str]):
    """Enable collaborative mode for multi-party holographic interaction"""
    try:
        success = await holographic_service.enable_collaborative_mode(projection_id, participants)
        
        if not success:
            raise HTTPException(status_code=404, detail="Projection not found")
        
        return ResponseModel(
            success=True,
            message="Collaborative mode enabled successfully",
            data={
                "projection_id": projection_id,
                "participants": participants,
                "interaction_mode": "multi_user"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to enable collaborative mode: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/{projection_id}")
async def holographic_websocket(websocket: WebSocket, projection_id: str):
    """WebSocket endpoint for real-time holographic interaction"""
    await websocket.accept()
    holographic_connections[projection_id] = websocket
    
    try:
        logger.info(f"🔮 WebSocket connected for holographic projection: {projection_id}")
        
        while True:
            # Receive real-time interaction data
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process holographic interaction
            await process_holographic_interaction(projection_id, message)
            
            # Send updated projection data back
            response = {
                "type": "projection_update",
                "projection_id": projection_id,
                "timestamp": asyncio.get_event_loop().time(),
                "data": message
            }
            
            await websocket.send_text(json.dumps(response))
            
    except WebSocketDisconnect:
        logger.info(f"🔮 WebSocket disconnected for projection: {projection_id}")
    except Exception as e:
        logger.error(f"❌ WebSocket error for projection {projection_id}: {e}")
    finally:
        if projection_id in holographic_connections:
            del holographic_connections[projection_id]

async def process_holographic_interaction(projection_id: str, interaction_data: Dict):
    """Process real-time holographic interaction data"""
    try:
        interaction_type = interaction_data.get("type")
        
        if interaction_type == "position_update":
            # Update projection position
            position = interaction_data.get("position", (0.0, 0.0, 0.0))
            await holographic_service.update_projection(projection_id, {"position": position})
            
        elif interaction_type == "rotation_update":
            # Update projection rotation
            rotation = interaction_data.get("rotation", (0.0, 0.0, 0.0))
            await holographic_service.update_projection(projection_id, {"rotation": rotation})
            
        elif interaction_type == "scale_update":
            # Update projection scale
            scale = interaction_data.get("scale", 1.0)
            await holographic_service.update_projection(projection_id, {"scale": scale})
            
        elif interaction_type == "animation_trigger":
            # Trigger holographic animation
            animation_data = interaction_data.get("animation_data", {})
            await holographic_service.update_projection(projection_id, {"animation_data": animation_data})
            
        logger.info(f"🔮 Processed holographic interaction: {interaction_type} for projection {projection_id}")
        
    except Exception as e:
        logger.error(f"❌ Failed to process holographic interaction: {e}")

@router.post("/business-presentation", response_model=ResponseModel)
async def create_business_presentation(presentation_data: Dict):
    """Create a business presentation with holographic elements"""
    try:
        # Extract presentation components
        title = presentation_data.get("title", "Business Presentation")
        slides = presentation_data.get("slides", [])
        holographic_elements = presentation_data.get("holographic_elements", [])
        
        # Create holographic projections for each element
        projection_ids = []
        for element in holographic_elements:
            request = HolographicProjectionRequest(
                device_id=element.get("device_id", "holo_proj_001"),
                projection_type=ProjectionType(element.get("type", "static_3d")),
                model_url=element.get("model_url"),
                position=element.get("position", (0.0, 0.0, 0.0)),
                rotation=element.get("rotation", (0.0, 0.0, 0.0)),
                scale=element.get("scale", 1.0),
                is_interactive=element.get("is_interactive", False)
            )
            
            projection_id = await holographic_service.create_holographic_projection(request)
            projection_ids.append(projection_id)
        
        return ResponseModel(
            success=True,
            message="Business presentation created successfully",
            data={
                "presentation_title": title,
                "slide_count": len(slides),
                "holographic_elements": len(holographic_elements),
                "projection_ids": projection_ids
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to create business presentation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business-scenarios", response_model=ResponseModel)
async def get_business_scenarios():
    """Get predefined business scenarios for holographic presentations"""
    scenarios = [
        {
            "id": "engineering_design",
            "name": "Engineering Design Review",
            "description": "3D holographic display of engineering blueprints and prototypes",
            "devices": ["holo_proj_001", "holo_display_001"],
            "use_cases": ["Product design review", "Prototype visualization", "Technical presentations"]
        },
        {
            "id": "architecture_presentation",
            "name": "Architectural Design Presentation",
            "description": "Holographic building models and architectural walkthroughs",
            "devices": ["holo_display_001", "holo_table_001"],
            "use_cases": ["Building design review", "Virtual walkthroughs", "Client presentations"]
        },
        {
            "id": "manufacturing_planning",
            "name": "Manufacturing Process Planning",
            "description": "Interactive holographic manufacturing workflows and equipment",
            "devices": ["holo_table_001", "holo_proj_001"],
            "use_cases": ["Process optimization", "Equipment layout", "Training simulations"]
        },
        {
            "id": "collaborative_design",
            "name": "Multi-Party Collaborative Design",
            "description": "Real-time collaborative holographic design sessions",
            "devices": ["holo_table_001", "holo_display_001"],
            "use_cases": ["Team collaboration", "Remote design sessions", "Interactive prototyping"]
        }
    ]
    
    return ResponseModel(
        success=True,
        message="Business scenarios retrieved successfully",
        data={"scenarios": scenarios}
    )

@router.post("/scenarios/{scenario_id}/activate", response_model=ResponseModel)
async def activate_business_scenario(scenario_id: str, scenario_config: Dict):
    """Activate a specific business scenario with holographic elements"""
    try:
        # Get scenario configuration
        scenarios_response = await get_business_scenarios()
        scenarios = scenarios_response.data["scenarios"]
        
        scenario = next((s for s in scenarios if s["id"] == scenario_id), None)
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
        
        # Activate scenario with holographic elements
        elements = scenario_config.get("elements", [])
        projection_ids = []
        
        for element in elements:
            request = HolographicProjectionRequest(
                device_id=element.get("device_id", scenario["devices"][0]),
                projection_type=ProjectionType(element.get("type", "interactive_3d")),
                model_url=element.get("model_url"),
                position=element.get("position", (0.0, 0.0, 0.0)),
                rotation=element.get("rotation", (0.0, 0.0, 0.0)),
                scale=element.get("scale", 1.0),
                is_interactive=element.get("is_interactive", True)
            )
            
            projection_id = await holographic_service.create_holographic_projection(request)
            projection_ids.append(projection_id)
        
        return ResponseModel(
            success=True,
            message=f"Business scenario '{scenario['name']}' activated successfully",
            data={
                "scenario_id": scenario_id,
                "scenario_name": scenario["name"],
                "projection_ids": projection_ids,
                "devices_used": scenario["devices"]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to activate business scenario: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 