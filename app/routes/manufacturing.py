"""
SEEKER Manufacturing API Routes
AI-assisted product prototyping and rapid iteration
On-demand global manufacturing connections
AI-facilitated mass production scaling
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import asyncio
import logging
import uuid
from pydantic import BaseModel

from app.services.manufacturing_service import ManufacturingService
from app.services.classification_engine import TaskClassificationEngine as ClassificationEngine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/manufacturing", tags=["manufacturing"])

# Initialize services
manufacturing_service = ManufacturingService()
classification_engine = ClassificationEngine()

# Pydantic models for manufacturing requests
class DesignData(BaseModel):
    name: str
    description: Optional[str] = None
    dimensions: Dict[str, float]
    material: str
    complexity: str = "medium"
    quantity: int = 1
    quality: str = "standard"
    finishing: Optional[str] = None
    shipping_address: Optional[Dict[str, str]] = None
    requirements: Optional[Dict[str, Any]] = None

class ManufacturingRequest(BaseModel):
    design_data: DesignData
    manufacturing_type: str  # "3d_printing", "cnc_machining", "injection_molding"
    priority: str = "normal"  # "urgent", "normal", "flexible"
    budget: str = "medium"  # "low", "medium", "high"
    timeline: str = "normal"  # "urgent", "normal", "flexible"

class ManufacturingJob(BaseModel):
    job_id: str
    status: str
    submitted_at: datetime
    estimated_completion: Optional[datetime] = None
    cost_estimate: Optional[float] = None
    manufacturing_partner: Optional[str] = None

class QualityCheckRequest(BaseModel):
    job_id: str
    part_data: Dict[str, Any]

class ManufacturingConnection(BaseModel):
    api_id: str
    name: str
    available: bool
    estimated_cost: Optional[float] = None
    lead_time: Optional[int] = None
    quality_rating: Optional[float] = None
    capabilities: List[str] = []

@router.post("/optimize-design")
async def optimize_manufacturing_design(request: ManufacturingRequest):
    """
    AI-assisted design optimization for manufacturing
    """
    try:
        logger.info(f"Optimizing manufacturing design: {request.design_data.name}")
        
        # Classify the manufacturing request
        classification_result = classification_engine.classify_request(
            f"manufacturing {request.manufacturing_type} {request.design_data.material}"
        )
        
        # Optimize the design for manufacturing
        optimization_result = await manufacturing_service.optimize_design_for_manufacturing(
            request.design_data,
            request.manufacturing_type,
            request.requirements or {}
        )
        
        return {
            "request_id": str(uuid.uuid4()),
            "optimization_result": optimization_result,
            "classification": classification_result,
            "recommendations": optimization_result.get("recommendations", []),
            "estimated_cost_savings": optimization_result.get("cost_savings", 0),
            "improved_lead_time": optimization_result.get("time_savings", 0)
        }
        
    except Exception as e:
        logger.error(f"Error optimizing manufacturing design: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/connect-global-manufacturing")
async def connect_global_manufacturing(request: ManufacturingRequest):
    """
    Connect to global manufacturing network
    """
    try:
        logger.info(f"Connecting to global manufacturing for: {request.design_data.name}")
        
        # Find optimal manufacturing connections
        connections = await manufacturing_service.find_optimal_manufacturing_connections(
            request.design_data,
            request.manufacturing_type,
            request.budget,
            request.timeline
        )
        
        return {
            "request_id": str(uuid.uuid4()),
            "available_connections": connections,
            "recommended_connection": connections[0] if connections else None,
            "total_connections": len(connections)
        }
        
    except Exception as e:
        logger.error(f"Error connecting to global manufacturing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit-manufacturing-job")
async def submit_manufacturing_job(
    request: ManufacturingRequest,
    background_tasks: BackgroundTasks
):
    """
    Submit a manufacturing job to the global network
    """
    try:
        logger.info(f"Submitting manufacturing job: {request.design_data.name}")
        
        # Create manufacturing job
        job = await manufacturing_service.create_manufacturing_job(
            request.design_data,
            request.manufacturing_type,
            request.priority,
            request.budget
        )
        
        # Start background monitoring
        background_tasks.add_task(
            manufacturing_service.monitor_manufacturing_job,
            job["job_id"]
        )
        
        return {
            "job_id": job["job_id"],
            "status": job["status"],
            "estimated_cost": job["estimated_cost"],
            "estimated_completion": job["estimated_completion"],
            "manufacturing_partner": job["manufacturing_partner"],
            "tracking_url": f"/api/v1/manufacturing/job/{job['job_id']}/status"
        }
        
    except Exception as e:
        logger.error(f"Error submitting manufacturing job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/job/{job_id}/status")
async def get_manufacturing_job_status(job_id: str):
    """
    Get the status of a manufacturing job
    """
    try:
        job_status = await manufacturing_service.get_job_status(job_id)
        
        if not job_status:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return job_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/job/{job_id}/quality-check")
async def perform_quality_check(job_id: str, request: QualityCheckRequest):
    """
    Perform quality check on manufactured part
    """
    try:
        logger.info(f"Performing quality check for job: {job_id}")
        
        quality_result = await manufacturing_service.perform_quality_check(
            job_id,
            request.part_data
        )
        
        return {
            "job_id": job_id,
            "quality_result": quality_result,
            "overall_score": quality_result["overall_score"],
            "pass_fail": quality_result["pass_fail"],
            "recommendations": quality_result["recommendations"]
        }
        
    except Exception as e:
        logger.error(f"Error performing quality check: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/available-materials")
async def get_available_materials():
    """
    Get list of available manufacturing materials
    """
    try:
        materials = await manufacturing_service.get_available_materials()
        return {
            "materials": materials,
            "total_count": len(materials)
        }
        
    except Exception as e:
        logger.error(f"Error getting available materials: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/manufacturing-capabilities")
async def get_manufacturing_capabilities():
    """
    Get available manufacturing capabilities
    """
    try:
        capabilities = await manufacturing_service.get_manufacturing_capabilities()
        return {
            "capabilities": capabilities,
            "total_count": len(capabilities)
        }
        
    except Exception as e:
        logger.error(f"Error getting manufacturing capabilities: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-connection")
async def test_manufacturing_connection(request: Dict[str, Any]):
    """
    Test connection to a manufacturing API
    """
    try:
        api_id = request.get("api_id")
        design_data = request.get("design_data")
        
        if not api_id or not design_data:
            raise HTTPException(status_code=400, detail="Missing required parameters")
        
        connection_result = await manufacturing_service.test_manufacturing_connection(
            api_id,
            design_data
        )
        
        return connection_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error testing manufacturing connection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/job-update")
async def update_manufacturing_job(request: Dict[str, Any]):
    """
    Update manufacturing job status (called by manufacturing partners)
    """
    try:
        job_id = request.get("job_id")
        status = request.get("status")
        timestamp = request.get("timestamp")
        
        if not job_id or not status:
            raise HTTPException(status_code=400, detail="Missing required parameters")
        
        await manufacturing_service.update_job_status(job_id, status, timestamp)
        
        return {"status": "updated", "job_id": job_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating manufacturing job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance-metrics")
async def get_manufacturing_performance_metrics():
    """
    Get manufacturing performance metrics
    """
    try:
        metrics = await manufacturing_service.get_performance_metrics()
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/manufacturing-updates")
async def manufacturing_updates_websocket(websocket: WebSocket):
    """
    WebSocket for real-time manufacturing updates
    """
    await websocket.accept()
    
    try:
        while True:
            # Send manufacturing updates
            updates = await manufacturing_service.get_recent_updates()
            await websocket.send_json({
                "type": "manufacturing_updates",
                "data": updates,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            await asyncio.sleep(30)  # Update every 30 seconds
            
    except WebSocketDisconnect:
        logger.info("Manufacturing WebSocket disconnected")
    except Exception as e:
        logger.error(f"Error in manufacturing WebSocket: {e}")
        await websocket.close()

@router.get("/health")
async def manufacturing_health_check():
    """
    Health check for manufacturing services
    """
    try:
        health_status = await manufacturing_service.health_check()
        return {
            "status": "healthy" if health_status else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": health_status
        }
        
    except Exception as e:
        logger.error(f"Manufacturing health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        } 