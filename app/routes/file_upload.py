from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.file_attachment import FileAttachment, FileType
import uuid
import os
from datetime import datetime

router = APIRouter()

# In-memory storage for demo
uploaded_files = {}

@router.post("/upload/", response_model=FileAttachment)
async def upload_file(file: UploadFile = File(...), user_id: str = "default_user"):
    file_id = str(uuid.uuid4())
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    file_path = f"uploads/{file_id}_{file.filename}"
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Create file record
    file_attachment = FileAttachment(
        attachment_id=file_id,
        filename=file.filename or "unknown_file",
        file_type=FileType.OTHER,  # Default to OTHER, could be enhanced with MIME type mapping
        mime_type=file.content_type or "application/octet-stream",
        file_size=len(content),
        uploaded_by=user_id,
        file_path=file_path
    )
    
    uploaded_files[file_id] = file_attachment
    return file_attachment

@router.get("/files/{file_id}")
async def get_file_info(file_id: str):
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")
    return uploaded_files[file_id] 