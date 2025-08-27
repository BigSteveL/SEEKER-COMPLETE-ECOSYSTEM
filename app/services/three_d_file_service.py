"""
SEEKER 3D File Processing Service
AI-assisted 3D model processing and optimization
STL, OBJ, G-code file handling and analysis
"""

import os
import logging
import json
import uuid
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import asyncio
import aiofiles
import numpy as np
from pathlib import Path
import struct

logger = logging.getLogger(__name__)

class FileType(Enum):
    """Supported 3D file types"""
    STL = "stl"
    OBJ = "obj"
    GCODE = "gcode"
    GLTF = "gltf"
    GLB = "glb"

class ProcessingStatus(Enum):
    """File processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class ModelInfo:
    """3D model information"""
    id: str
    filename: str
    file_type: FileType
    file_size: int
    vertex_count: int
    face_count: int
    bounding_box: Dict[str, float]
    volume: float
    surface_area: float
    center_of_mass: Dict[str, float]
    processing_status: ProcessingStatus
    upload_time: datetime
    processing_time: Optional[datetime] = None
    metadata: Dict[str, Any] = None

@dataclass
class PrintSettings:
    """3D print settings"""
    layer_height: float = 0.2
    infill_density: float = 20.0
    print_speed: float = 60.0
    support_enabled: bool = False
    support_density: float = 15.0
    bed_temperature: float = 60.0
    extruder_temperature: float = 200.0
    retraction_distance: float = 5.0
    retraction_speed: float = 45.0

class SEEKER3DFileService:
    """3D file processing service for SEEKER AI system"""
    
    def __init__(self):
        self.upload_dir = Path("uploads/3d_models")
        self.processed_dir = Path("processed/3d_models")
        self.temp_dir = Path("temp/3d_models")
        
        # Create directories
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # File storage
        self.models: Dict[str, ModelInfo] = {}
        self.processing_queue: List[str] = []
        
        # Commented out to avoid event loop errors at import time
        # asyncio.create_task(self._process_queue())
        
        logger.info("🚀 SEEKER 3D File Service initialized")

    async def upload_file(self, file_content: bytes, filename: str) -> str:
        """
        Upload and process a 3D file
        """
        try:
            # Generate unique ID
            model_id = str(uuid.uuid4())
            
            # Determine file type
            file_type = self._get_file_type(filename)
            if not file_type:
                raise ValueError(f"Unsupported file type: {filename}")
            
            # Save file
            file_path = self.upload_dir / f"{model_id}_{filename}"
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_content)
            
            # Create model info
            model_info = ModelInfo(
                id=model_id,
                filename=filename,
                file_type=file_type,
                file_size=len(file_content),
                vertex_count=0,
                face_count=0,
                bounding_box={"x": 0, "y": 0, "z": 0},
                volume=0.0,
                surface_area=0.0,
                center_of_mass={"x": 0, "y": 0, "z": 0},
                processing_status=ProcessingStatus.PENDING,
                upload_time=datetime.now(),
                metadata={}
            )
            
            self.models[model_id] = model_info
            self.processing_queue.append(model_id)
            
            logger.info(f"✅ File uploaded: {filename} (ID: {model_id})")
            return model_id
            
        except Exception as e:
            logger.error(f"Error uploading file {filename}: {e}")
            raise

    async def process_file(self, model_id: str) -> bool:
        """
        Process a 3D file to extract information
        """
        try:
            if model_id not in self.models:
                return False
            
            model_info = self.models[model_id]
            model_info.processing_status = ProcessingStatus.PROCESSING
            
            file_path = self.upload_dir / f"{model_id}_{model_info.filename}"
            
            if not file_path.exists():
                model_info.processing_status = ProcessingStatus.FAILED
                return False
            
            # Process based on file type
            if model_info.file_type == FileType.STL:
                success = await self._process_stl_file(model_id, file_path)
            elif model_info.file_type == FileType.OBJ:
                success = await self._process_obj_file(model_id, file_path)
            elif model_info.file_type == FileType.GCODE:
                success = await self._process_gcode_file(model_id, file_path)
            else:
                success = False
            
            if success:
                model_info.processing_status = ProcessingStatus.COMPLETED
                model_info.processing_time = datetime.now()
                logger.info(f"✅ File processed successfully: {model_info.filename}")
            else:
                model_info.processing_status = ProcessingStatus.FAILED
                logger.error(f"❌ File processing failed: {model_info.filename}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing file {model_id}: {e}")
            if model_id in self.models:
                self.models[model_id].processing_status = ProcessingStatus.FAILED
            return False

    async def _process_stl_file(self, model_id: str, file_path: Path) -> bool:
        """Process STL file to extract geometry information"""
        try:
            # Read STL file
            vertices, faces = await self._read_stl_file(file_path)
            
            if not vertices or not faces:
                return False
            
            # Calculate model properties
            model_info = self.models[model_id]
            model_info.vertex_count = len(vertices)
            model_info.face_count = len(faces)
            
            # Calculate bounding box
            vertices_array = np.array(vertices)
            min_coords = np.min(vertices_array, axis=0)
            max_coords = np.max(vertices_array, axis=0)
            
            model_info.bounding_box = {
                "x": float(max_coords[0] - min_coords[0]),
                "y": float(max_coords[1] - min_coords[1]),
                "z": float(max_coords[2] - min_coords[2])
            }
            
            # Calculate center of mass
            model_info.center_of_mass = {
                "x": float(np.mean(vertices_array[:, 0])),
                "y": float(np.mean(vertices_array[:, 1])),
                "z": float(np.mean(vertices_array[:, 2]))
            }
            
            # Calculate volume and surface area (simplified)
            model_info.volume = self._calculate_volume(vertices, faces)
            model_info.surface_area = self._calculate_surface_area(vertices, faces)
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing STL file {model_id}: {e}")
            return False

    async def _process_obj_file(self, model_id: str, file_path: Path) -> bool:
        """Process OBJ file to extract geometry information"""
        try:
            # Read OBJ file
            vertices, faces = await self._read_obj_file(file_path)
            
            if not vertices or not faces:
                return False
            
            # Calculate model properties (similar to STL)
            model_info = self.models[model_id]
            model_info.vertex_count = len(vertices)
            model_info.face_count = len(faces)
            
            # Calculate bounding box
            vertices_array = np.array(vertices)
            min_coords = np.min(vertices_array, axis=0)
            max_coords = np.max(vertices_array, axis=0)
            
            model_info.bounding_box = {
                "x": float(max_coords[0] - min_coords[0]),
                "y": float(max_coords[1] - min_coords[1]),
                "z": float(max_coords[2] - min_coords[2])
            }
            
            # Calculate center of mass
            model_info.center_of_mass = {
                "x": float(np.mean(vertices_array[:, 0])),
                "y": float(np.mean(vertices_array[:, 1])),
                "z": float(np.mean(vertices_array[:, 2]))
            }
            
            # Calculate volume and surface area
            model_info.volume = self._calculate_volume(vertices, faces)
            model_info.surface_area = self._calculate_surface_area(vertices, faces)
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing OBJ file {model_id}: {e}")
            return False

    async def _process_gcode_file(self, model_id: str, file_path: Path) -> bool:
        """Process G-code file to extract print information"""
        try:
            # Read G-code file
            gcode_info = await self._analyze_gcode_file(file_path)
            
            model_info = self.models[model_id]
            model_info.metadata = gcode_info
            
            # Extract basic information
            model_info.vertex_count = gcode_info.get("total_layers", 0)
            model_info.face_count = gcode_info.get("total_moves", 0)
            
            # Estimate bounding box from G-code
            if "min_coords" in gcode_info and "max_coords" in gcode_info:
                min_coords = gcode_info["min_coords"]
                max_coords = gcode_info["max_coords"]
                
                model_info.bounding_box = {
                    "x": max_coords[0] - min_coords[0],
                    "y": max_coords[1] - min_coords[1],
                    "z": max_coords[2] - min_coords[2]
                }
                
                model_info.center_of_mass = {
                    "x": (max_coords[0] + min_coords[0]) / 2,
                    "y": (max_coords[1] + min_coords[1]) / 2,
                    "z": (max_coords[2] + min_coords[2]) / 2
                }
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing G-code file {model_id}: {e}")
            return False

    async def _read_stl_file(self, file_path: Path) -> Tuple[List, List]:
        """Read STL file and extract vertices and faces"""
        try:
            vertices = []
            faces = []
            
            async with aiofiles.open(file_path, 'rb') as f:
                content = await f.read()
            
            # Check if binary STL
            if content.startswith(b'solid'):
                # ASCII STL
                lines = content.decode('utf-8').split('\n')
                current_face = []
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('vertex'):
                        parts = line.split()
                        vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                        vertices.append(vertex)
                        current_face.append(len(vertices) - 1)
                    elif line.startswith('endfacet'):
                        if len(current_face) == 3:
                            faces.append(current_face)
                        current_face = []
            else:
                # Binary STL - simplified parsing
                # Skip header (80 bytes) and triangle count (4 bytes)
                offset = 84
                
                while offset < len(content):
                    # Each triangle is 50 bytes
                    if offset + 50 > len(content):
                        break
                    
                    # Extract vertices (12 bytes each, 3 vertices per triangle)
                    for i in range(3):
                        vertex = []
                        for j in range(3):
                            value = struct.unpack('<f', content[offset + 12 + i*12 + j*4:offset + 12 + i*12 + (j+1)*4])[0]
                            vertex.append(value)
                        vertices.append(vertex)
                    
                    # Create face
                    face_start = len(vertices) - 3
                    faces.append([face_start, face_start + 1, face_start + 2])
                    
                    offset += 50
            
            return vertices, faces
            
        except Exception as e:
            logger.error(f"Error reading STL file: {e}")
            return [], []

    async def _read_obj_file(self, file_path: Path) -> Tuple[List, List]:
        """Read OBJ file and extract vertices and faces"""
        try:
            vertices = []
            faces = []
            
            async with aiofiles.open(file_path, 'r') as f:
                lines = await f.readlines()
            
            for line in lines:
                line = line.strip()
                if line.startswith('v '):
                    # Vertex
                    parts = line.split()
                    vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                    vertices.append(vertex)
                elif line.startswith('f '):
                    # Face
                    parts = line.split()
                    face = []
                    for i in range(1, len(parts)):
                        # Handle vertex/texture/normal indices
                        vertex_index = int(parts[i].split('/')[0]) - 1
                        face.append(vertex_index)
                    faces.append(face)
            
            return vertices, faces
            
        except Exception as e:
            logger.error(f"Error reading OBJ file: {e}")
            return [], []

    async def _analyze_gcode_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze G-code file to extract print information"""
        try:
            info = {
                "total_layers": 0,
                "total_moves": 0,
                "print_time": 0,
                "filament_used": 0,
                "min_coords": [0, 0, 0],
                "max_coords": [0, 0, 0],
                "settings": {}
            }
            
            async with aiofiles.open(file_path, 'r') as f:
                lines = await f.readlines()
            
            min_coords = [float('inf'), float('inf'), float('inf')]
            max_coords = [float('-inf'), float('-inf'), float('-inf')]
            
            for line in lines:
                line = line.strip().upper()
                
                # Count moves
                if line.startswith('G1') or line.startswith('G0'):
                    info["total_moves"] += 1
                    
                    # Extract coordinates
                    coords = [0, 0, 0]
                    if 'X' in line:
                        coords[0] = float(line.split('X')[1].split()[0])
                    if 'Y' in line:
                        coords[1] = float(line.split('Y')[1].split()[0])
                    if 'Z' in line:
                        coords[2] = float(line.split('Z')[1].split()[0])
                    
                    # Update bounding box
                    for i in range(3):
                        min_coords[i] = min(min_coords[i], coords[i])
                        max_coords[i] = max(max_coords[i], coords[i])
                
                # Count layers
                elif line.startswith(';LAYER:'):
                    info["total_layers"] += 1
                
                # Extract settings
                elif line.startswith(';SETTING_'):
                    setting_line = line[9:]  # Remove ';SETTING_'
                    if ' ' in setting_line:
                        key, value = setting_line.split(' ', 1)
                        info["settings"][key] = value
            
            info["min_coords"] = min_coords
            info["max_coords"] = max_coords
            
            return info
            
        except Exception as e:
            logger.error(f"Error analyzing G-code file: {e}")
            return {}

    def _calculate_volume(self, vertices: List, faces: List) -> float:
        """Calculate volume of 3D model"""
        try:
            volume = 0.0
            for face in faces:
                if len(face) >= 3:
                    v1 = np.array(vertices[face[0]])
                    v2 = np.array(vertices[face[1]])
                    v3 = np.array(vertices[face[2]])
                    
                    # Calculate signed volume of tetrahedron
                    volume += np.dot(v1, np.cross(v2, v3)) / 6.0
            
            return abs(volume)
        except Exception as e:
            logger.error(f"Error calculating volume: {e}")
            return 0.0

    def _calculate_surface_area(self, vertices: List, faces: List) -> float:
        """Calculate surface area of 3D model"""
        try:
            area = 0.0
            for face in faces:
                if len(face) >= 3:
                    v1 = np.array(vertices[face[0]])
                    v2 = np.array(vertices[face[1]])
                    v3 = np.array(vertices[face[2]])
                    
                    # Calculate area of triangle
                    edge1 = v2 - v1
                    edge2 = v3 - v1
                    triangle_area = np.linalg.norm(np.cross(edge1, edge2)) / 2.0
                    area += triangle_area
            
            return area
        except Exception as e:
            logger.error(f"Error calculating surface area: {e}")
            return 0.0

    def _get_file_type(self, filename: str) -> Optional[FileType]:
        """Determine file type from filename"""
        ext = filename.lower().split('.')[-1]
        
        if ext == 'stl':
            return FileType.STL
        elif ext == 'obj':
            return FileType.OBJ
        elif ext in ['gcode', 'gco', 'g']:
            return FileType.GCODE
        elif ext == 'gltf':
            return FileType.GLTF
        elif ext == 'glb':
            return FileType.GLB
        else:
            return None

    async def get_model_info(self, model_id: str) -> Optional[ModelInfo]:
        """Get model information"""
        return self.models.get(model_id)

    async def get_all_models(self) -> List[ModelInfo]:
        """Get all models"""
        return list(self.models.values())

    async def delete_model(self, model_id: str) -> bool:
        """Delete a model"""
        try:
            if model_id in self.models:
                model_info = self.models[model_id]
                
                # Delete files
                file_path = self.upload_dir / f"{model_id}_{model_info.filename}"
                if file_path.exists():
                    file_path.unlink()
                
                # Remove from storage
                del self.models[model_id]
                
                logger.info(f"✅ Model deleted: {model_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting model {model_id}: {e}")
            return False

    async def generate_print_preview(self, model_id: str, settings: PrintSettings) -> Dict[str, Any]:
        """Generate print preview with settings"""
        try:
            if model_id not in self.models:
                return {}
            
            model_info = self.models[model_id]
            
            # Calculate print time estimate
            layer_count = int(model_info.bounding_box["z"] / settings.layer_height)
            print_time = layer_count * (model_info.bounding_box["x"] * model_info.bounding_box["y"] / settings.print_speed)
            
            # Calculate material usage
            volume_cm3 = model_info.volume / 1000  # Convert to cm³
            material_weight = volume_cm3 * 1.24  # PLA density ~1.24 g/cm³
            
            preview = {
                "model_id": model_id,
                "print_time_hours": print_time / 3600,
                "material_weight_g": material_weight,
                "layer_count": layer_count,
                "settings": {
                    "layer_height": settings.layer_height,
                    "infill_density": settings.infill_density,
                    "print_speed": settings.print_speed,
                    "support_enabled": settings.support_enabled,
                    "bed_temperature": settings.bed_temperature,
                    "extruder_temperature": settings.extruder_temperature
                },
                "model_info": {
                    "filename": model_info.filename,
                    "bounding_box": model_info.bounding_box,
                    "volume": model_info.volume,
                    "surface_area": model_info.surface_area
                }
            }
            
            return preview
            
        except Exception as e:
            logger.error(f"Error generating print preview: {e}")
            return {}

    async def _process_queue(self):
        """Background task to process queued files"""
        while True:
            try:
                if self.processing_queue:
                    model_id = self.processing_queue.pop(0)
                    await self.process_file(model_id)
                
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error in processing queue: {e}")
                await asyncio.sleep(5) 