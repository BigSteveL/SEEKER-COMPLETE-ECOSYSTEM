"""
SEEKER 3D Printer API Routes
AI-assisted product prototyping and rapid iteration
Real-time print job monitoring and control
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import logging
import uuid
import json

from app.services.printer_service import SEEKER3DPrinterService, PrinterInfo, PrintJob, PrinterState
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/3d-printer", tags=["3d-printer"])

# Initialize 3D printer service
printer_service = SEEKER3DPrinterService()

# Pydantic models
class PrinterConnectionRequest(BaseModel):
    printer_id: str

class PrintJobRequest(BaseModel):
    printer_id: str
    file_path: str
    filename: str

class TemperatureRequest(BaseModel):
    printer_id: str
    extruder_temp: float
    bed_temp: Optional[float] = None

class MoveAxisRequest(BaseModel):
    printer_id: str
    axis: str
    position: float

class PrinterCommandRequest(BaseModel):
    printer_id: str
    command: str

@router.get("/discover")
async def discover_printers():
    """
    Discover available 3D printers on the system
    """
    try:
        logger.info("🔍 Discovering 3D printers...")
        printers = await printer_service.discover_printers()
        
        return {
            "printers": [
                {
                    "id": p.id,
                    "name": p.name,
                    "port": p.port,
                    "model": p.model,
                    "firmware": p.firmware,
                    "capabilities": p.capabilities,
                    "max_temperature": p.max_temperature,
                    "max_bed_temperature": p.max_bed_temperature,
                    "build_volume": p.build_volume
                }
                for p in printers
            ],
            "total_count": len(printers)
        }
        
    except Exception as e:
        logger.error(f"Error discovering printers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printers")
async def get_printers():
    """
    Get list of discovered and connected printers
    """
    try:
        discovered = printer_service.get_discovered_printers()
        connected = printer_service.get_connected_printers()
        
        return {
            "discovered": [
                {
                    "id": p.id,
                    "name": p.name,
                    "port": p.port,
                    "model": p.model,
                    "firmware": p.firmware,
                    "capabilities": p.capabilities
                }
                for p in discovered
            ],
            "connected": connected,
            "total_discovered": len(discovered),
            "total_connected": len(connected)
        }
        
    except Exception as e:
        logger.error(f"Error getting printers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/connect")
async def connect_printer(request: PrinterConnectionRequest):
    """
    Connect to a specific 3D printer
    """
    try:
        logger.info(f"🔌 Connecting to printer: {request.printer_id}")
        success = await printer_service.connect_printer(request.printer_id)
        
        if success:
            return {
                "message": "Printer connected successfully",
                "printer_id": request.printer_id,
                "status": "connected"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to connect to printer")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error connecting to printer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/disconnect")
async def disconnect_printer(request: PrinterConnectionRequest):
    """
    Disconnect from a 3D printer
    """
    try:
        logger.info(f"🔌 Disconnecting from printer: {request.printer_id}")
        success = await printer_service.disconnect_printer(request.printer_id)
        
        if success:
            return {
                "message": "Printer disconnected successfully",
                "printer_id": request.printer_id,
                "status": "disconnected"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to disconnect from printer")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disconnecting from printer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{printer_id}/status")
async def get_printer_status(printer_id: str):
    """
    Get current status of a connected printer
    """
    try:
        state = await printer_service.get_printer_state(printer_id)
        
        if not state:
            raise HTTPException(status_code=404, detail="Printer not found or not connected")
        
        return {
            "printer_id": printer_id,
            "status": state.status.value,
            "temperature": state.temperature,
            "target_temperature": state.target_temperature,
            "position": state.position,
            "fan_speed": state.fan_speed,
            "print_progress": state.print_progress,
            "current_job": {
                "id": state.current_job.id,
                "filename": state.current_job.filename,
                "progress": state.current_job.progress,
                "elapsed_time": state.current_job.elapsed_time,
                "remaining_time": state.current_job.remaining_time,
                "status": state.current_job.status.value
            } if state.current_job else None,
            "last_update": state.last_update.isoformat() if state.last_update else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting printer status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/print")
async def start_print_job(request: PrintJobRequest, background_tasks: BackgroundTasks):
    """
    Start a print job on a connected printer
    """
    try:
        logger.info(f"🖨️ Starting print job: {request.filename} on printer {request.printer_id}")
        
        job_id = await printer_service.send_print_job(
            request.printer_id,
            request.file_path,
            request.filename
        )
        
        if job_id:
            return {
                "message": "Print job started successfully",
                "job_id": job_id,
                "printer_id": request.printer_id,
                "filename": request.filename,
                "status": "printing"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to start print job")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting print job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{printer_id}/pause")
async def pause_print(printer_id: str):
    """
    Pause current print job
    """
    try:
        logger.info(f"⏸️ Pausing print on printer: {printer_id}")
        success = await printer_service.pause_print(printer_id)
        
        if success:
            return {
                "message": "Print paused successfully",
                "printer_id": printer_id,
                "status": "paused"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to pause print")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error pausing print: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{printer_id}/resume")
async def resume_print(printer_id: str):
    """
    Resume paused print job
    """
    try:
        logger.info(f"▶️ Resuming print on printer: {printer_id}")
        success = await printer_service.resume_print(printer_id)
        
        if success:
            return {
                "message": "Print resumed successfully",
                "printer_id": printer_id,
                "status": "printing"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to resume print")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resuming print: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{printer_id}/cancel")
async def cancel_print(printer_id: str):
    """
    Cancel current print job
    """
    try:
        logger.info(f"❌ Canceling print on printer: {printer_id}")
        success = await printer_service.cancel_print(printer_id)
        
        if success:
            return {
                "message": "Print canceled successfully",
                "printer_id": printer_id,
                "status": "idle"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to cancel print")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error canceling print: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/temperature")
async def set_temperature(request: TemperatureRequest):
    """
    Set printer temperatures
    """
    try:
        logger.info(f"🌡️ Setting temperature on printer: {request.printer_id}")
        success = await printer_service.set_temperature(
            request.printer_id,
            request.extruder_temp,
            request.bed_temp
        )
        
        if success:
            return {
                "message": "Temperature set successfully",
                "printer_id": request.printer_id,
                "extruder_temp": request.extruder_temp,
                "bed_temp": request.bed_temp
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to set temperature")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting temperature: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{printer_id}/home")
async def home_axes(printer_id: str):
    """
    Home all printer axes
    """
    try:
        logger.info(f"🏠 Homing axes on printer: {printer_id}")
        success = await printer_service.home_axes(printer_id)
        
        if success:
            return {
                "message": "Axes homed successfully",
                "printer_id": printer_id,
                "status": "homed"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to home axes")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error homing axes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/move")
async def move_axis(request: MoveAxisRequest):
    """
    Move printer axis to position
    """
    try:
        logger.info(f"📍 Moving {request.axis} axis on printer: {request.printer_id}")
        success = await printer_service.move_axis(
            request.printer_id,
            request.axis,
            request.position
        )
        
        if success:
            return {
                "message": "Axis moved successfully",
                "printer_id": request.printer_id,
                "axis": request.axis,
                "position": request.position
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to move axis")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error moving axis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/command")
async def send_command(request: PrinterCommandRequest):
    """
    Send custom command to printer
    """
    try:
        logger.info(f"📤 Sending command to printer: {request.printer_id}")
        
        # Get printer connection
        if request.printer_id not in printer_service.connected_printers:
            raise HTTPException(status_code=404, detail="Printer not connected")
        
        connection = printer_service.connected_printers[request.printer_id]
        response = await connection.send_command(request.command)
        
        return {
            "message": "Command sent successfully",
            "printer_id": request.printer_id,
            "command": request.command,
            "response": response
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs")
async def get_print_jobs():
    """
    Get all print jobs
    """
    try:
        jobs = printer_service.get_print_jobs()
        
        return {
            "jobs": [
                {
                    "id": job.id,
                    "filename": job.filename,
                    "progress": job.progress,
                    "status": job.status.value,
                    "started_at": job.started_at.isoformat(),
                    "elapsed_time": job.elapsed_time,
                    "remaining_time": job.remaining_time
                }
                for job in jobs.values()
            ],
            "total_count": len(jobs)
        }
        
    except Exception as e:
        logger.error(f"Error getting print jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/{printer_id}")
async def printer_websocket(websocket: WebSocket, printer_id: str):
    """
    WebSocket endpoint for real-time printer status updates
    """
    await websocket.accept()
    
    try:
        # Add status callback
        async def status_callback(printer_id: str, state: PrinterState):
            try:
                await websocket.send_json({
                    "type": "status_update",
                    "printer_id": printer_id,
                    "status": state.status.value,
                    "temperature": state.temperature,
                    "position": state.position,
                    "print_progress": state.print_progress,
                    "current_job": {
                        "id": state.current_job.id,
                        "filename": state.current_job.filename,
                        "progress": state.current_job.progress,
                        "status": state.current_job.status.value
                    } if state.current_job else None,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Error sending WebSocket update: {e}")
        
        printer_service.add_status_callback(status_callback)
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                elif message.get("type") == "command":
                    # Handle custom commands
                    command = message.get("command")
                    if command:
                        response = await printer_service.connected_printers[printer_id].send_command(command)
                        await websocket.send_json({
                            "type": "command_response",
                            "command": command,
                            "response": response
                        })
                        
            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnected for printer: {printer_id}")
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
                
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        await websocket.close()

@router.get("/health")
async def printer_health_check():
    """
    Health check for 3D printer service
    """
    try:
        discovered_count = len(printer_service.get_discovered_printers())
        connected_count = len(printer_service.get_connected_printers())
        
        return {
            "status": "healthy",
            "service": "3d_printer",
            "discovered_printers": discovered_count,
            "connected_printers": connected_count,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Printer health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "3d_printer",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        } 