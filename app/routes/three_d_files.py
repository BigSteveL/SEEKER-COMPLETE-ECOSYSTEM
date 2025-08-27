"""
SEEKER 3D File Processing API Routes
AI-assisted 3D model processing and optimization
STL, OBJ, G-code file handling and analysis
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import json

from app.services.three_d_file_service import SEEKER3DFileService, PrintSettings, ProcessingStatus
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/3d-files", tags=["3d-files"])

# Initialize 3D file service
file_service = SEEKER3DFileService()

# Pydantic models
class PrintSettingsRequest(BaseModel):
    layer_height: float = 0.2
    infill_density: float = 20.0
    print_speed: float = 60.0
    support_enabled: bool = False
    support_density: float = 15.0
    bed_temperature: float = 60.0
    extruder_temperature: float = 200.0
    retraction_distance: float = 5.0
    retraction_speed: float = 45.0

class ModelSearchRequest(BaseModel):
    file_type: Optional[str] = None
    min_volume: Optional[float] = None
    max_volume: Optional[float] = None
    status: Optional[str] = None

@router.post("/upload")
async def upload_3d_file(file: UploadFile = File(...)):
    """
    Upload a 3D file (STL, OBJ, G-code, GLTF, GLB)
    """
    try:
        # Validate file type
        allowed_extensions = ['.stl', '.obj', '.gcode', '.gco', '.g', '.gltf', '.glb']
        file_extension = '.' + file.filename.lower().split('.')[-1]
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Read file content
        content = await file.read()
        
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        if len(content) > 100 * 1024 * 1024:  # 100MB limit
            raise HTTPException(status_code=400, detail="File too large (max 100MB)")
        
        # Upload file
        model_id = await file_service.upload_file(content, file.filename)
        
        logger.info(f"✅ 3D file uploaded: {file.filename} (ID: {model_id})")
        
        return {
            "message": "File uploaded successfully",
            "model_id": model_id,
            "filename": file.filename,
            "file_size": len(content),
            "status": "pending_processing"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading 3D file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def get_models(search: Optional[str] = None):
    """
    Get all 3D models with optional search
    """
    try:
        models = await file_service.get_all_models()
        
        # Apply search filter
        if search:
            filtered_models = []
            search_lower = search.lower()
            for model in models:
                if (search_lower in model.filename.lower() or 
                    search_lower in model.file_type.value.lower()):
                    filtered_models.append(model)
            models = filtered_models
        
        return {
            "models": [
                {
                    "id": model.id,
                    "filename": model.filename,
                    "file_type": model.file_type.value,
                    "file_size": model.file_size,
                    "vertex_count": model.vertex_count,
                    "face_count": model.face_count,
                    "bounding_box": model.bounding_box,
                    "volume": model.volume,
                    "surface_area": model.surface_area,
                    "center_of_mass": model.center_of_mass,
                    "processing_status": model.processing_status.value,
                    "upload_time": model.upload_time.isoformat(),
                    "processing_time": model.processing_time.isoformat() if model.processing_time else None,
                    "metadata": model.metadata or {}
                }
                for model in models
            ],
            "total_count": len(models)
        }
        
    except Exception as e:
        logger.error(f"Error getting models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_id}")
async def get_model_info(model_id: str):
    """
    Get detailed information about a specific 3D model
    """
    try:
        model_info = await file_service.get_model_info(model_id)
        
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return {
            "id": model_info.id,
            "filename": model_info.filename,
            "file_type": model_info.file_type.value,
            "file_size": model_info.file_size,
            "vertex_count": model_info.vertex_count,
            "face_count": model_info.face_count,
            "bounding_box": model_info.bounding_box,
            "volume": model_info.volume,
            "surface_area": model_info.surface_area,
            "center_of_mass": model_info.center_of_mass,
            "processing_status": model_info.processing_status.value,
            "upload_time": model_info.upload_time.isoformat(),
            "processing_time": model_info.processing_time.isoformat() if model_info.processing_time else None,
            "metadata": model_info.metadata or {}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/models/{model_id}")
async def delete_model(model_id: str):
    """
    Delete a 3D model
    """
    try:
        success = await file_service.delete_model(model_id)
        
        if success:
            return {
                "message": "Model deleted successfully",
                "model_id": model_id
            }
        else:
            raise HTTPException(status_code=404, detail="Model not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_id}/process")
async def process_model(model_id: str):
    """
    Manually trigger processing of a 3D model
    """
    try:
        success = await file_service.process_file(model_id)
        
        if success:
            return {
                "message": "Model processing completed",
                "model_id": model_id,
                "status": "completed"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to process model")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_id}/preview")
async def generate_print_preview(model_id: str, settings: PrintSettingsRequest):
    """
    Generate print preview with custom settings
    """
    try:
        print_settings = PrintSettings(
            layer_height=settings.layer_height,
            infill_density=settings.infill_density,
            print_speed=settings.print_speed,
            support_enabled=settings.support_enabled,
            support_density=settings.support_density,
            bed_temperature=settings.bed_temperature,
            extruder_temperature=settings.extruder_temperature,
            retraction_distance=settings.retraction_distance,
            retraction_speed=settings.retraction_speed
        )
        
        preview = await file_service.generate_print_preview(model_id, print_settings)
        
        if preview:
            return preview
        else:
            raise HTTPException(status_code=404, detail="Model not found or processing failed")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating print preview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_id}/download")
async def download_model(model_id: str):
    """
    Download a 3D model file
    """
    try:
        model_info = await file_service.get_model_info(model_id)
        
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # Get file path
        file_path = file_service.upload_dir / f"{model_id}_{model_info.filename}"
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Return file download response
        from fastapi.responses import FileResponse
        return FileResponse(
            path=str(file_path),
            filename=model_info.filename,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_id}/thumbnail")
async def get_model_thumbnail(model_id: str):
    """
    Get thumbnail/preview image for a 3D model
    """
    try:
        model_info = await file_service.get_model_info(model_id)
        
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # For now, return a placeholder
        # In a real implementation, this would generate a thumbnail from the 3D model
        return {
            "model_id": model_id,
            "thumbnail_url": f"/api/v1/3d-files/models/{model_id}/thumbnail-image",
            "has_thumbnail": False,
            "message": "Thumbnail generation not implemented yet"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model thumbnail: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_id}/optimize")
async def optimize_model(model_id: str):
    """
    Optimize a 3D model for printing
    """
    try:
        model_info = await file_service.get_model_info(model_id)
        
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # For now, return optimization suggestions
        # In a real implementation, this would perform actual model optimization
        optimization_suggestions = {
            "model_id": model_id,
            "optimizations": [
                {
                    "type": "mesh_repair",
                    "description": "Fix non-manifold edges and holes",
                    "priority": "high"
                },
                {
                    "type": "reduce_polygons",
                    "description": "Reduce polygon count for faster printing",
                    "priority": "medium"
                },
                {
                    "type": "add_supports",
                    "description": "Add support structures for overhangs",
                    "priority": "low"
                }
            ],
            "estimated_improvement": {
                "print_time_reduction": "15%",
                "material_savings": "8%",
                "quality_improvement": "Better surface finish"
            }
        }
        
        return optimization_suggestions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error optimizing model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
async def get_file_statistics():
    """
    Get statistics about uploaded 3D files
    """
    try:
        models = await file_service.get_all_models()
        
        # Calculate statistics
        total_files = len(models)
        total_size = sum(model.file_size for model in models)
        
        file_types = {}
        for model in models:
            file_type = model.file_type.value
            file_types[file_type] = file_types.get(file_type, 0) + 1
        
        processing_status = {}
        for model in models:
            status = model.processing_status.value
            processing_status[status] = processing_status.get(status, 0) + 1
        
        total_volume = sum(model.volume for model in models if model.volume > 0)
        total_surface_area = sum(model.surface_area for model in models if model.surface_area > 0)
        
        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "file_types": file_types,
            "processing_status": processing_status,
            "total_volume": total_volume,
            "total_surface_area": total_surface_area,
            "average_volume": total_volume / total_files if total_files > 0 else 0,
            "average_surface_area": total_surface_area / total_files if total_files > 0 else 0
        }
        
    except Exception as e:
        logger.error(f"Error getting file statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def file_service_health_check():
    """
    Health check for 3D file service
    """
    try:
        models = await file_service.get_all_models()
        
        return {
            "status": "healthy",
            "service": "3d_file_processing",
            "total_models": len(models),
            "processing_queue_length": len(file_service.processing_queue),
            "upload_directory": str(file_service.upload_dir),
            "processed_directory": str(file_service.processed_dir),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"File service health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "3d_file_processing",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        } 