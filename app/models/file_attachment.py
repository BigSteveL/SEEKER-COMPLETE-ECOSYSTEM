from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class FileType(str, Enum):
    """Supported file types for attachments"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    SPREADSHEET = "spreadsheet"
    PRESENTATION = "presentation"
    ARCHIVE = "archive"
    CODE = "code"
    OTHER = "other"

class FileAttachment(BaseModel):
    """Model for file attachments in the SEEKER system"""
    
    attachment_id: str = Field(..., description="Unique identifier for the file attachment")
    filename: str = Field(..., description="Original filename of the uploaded file")
    file_type: FileType = Field(..., description="Type/category of the file")
    mime_type: str = Field(..., description="MIME type of the file")
    file_size: int = Field(..., description="Size of the file in bytes")
    file_path: Optional[str] = Field(default=None, description="Path where the file is stored")
    file_url: Optional[str] = Field(default=None, description="URL to access the file")
    file_hash: Optional[str] = Field(default=None, description="SHA-256 hash of the file content")
    
    # Metadata
    uploaded_by: str = Field(..., description="User ID who uploaded the file")
    uploaded_at: datetime = Field(default_factory=datetime.now, description="When the file was uploaded")
    description: Optional[str] = Field(default=None, description="Optional description of the file")
    tags: list[str] = Field(default_factory=list, description="Tags for categorizing the file")
    
    # Processing status
    is_processed: bool = Field(default=False, description="Whether the file has been processed")
    processing_status: str = Field(default="pending", description="Current processing status")
    processing_metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional processing metadata")
    
    # Security and access control
    is_public: bool = Field(default=False, description="Whether the file is publicly accessible")
    access_permissions: list[str] = Field(default_factory=list, description="List of user IDs with access")
    encryption_key: Optional[str] = Field(default=None, description="Encryption key if file is encrypted")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class FileUploadRequest(BaseModel):
    """Request model for file uploads"""
    
    filename: str = Field(..., description="Original filename")
    file_type: FileType = Field(..., description="Type of file being uploaded")
    description: Optional[str] = Field(default=None, description="Optional description")
    tags: list[str] = Field(default_factory=list, description="Tags for categorization")
    is_public: bool = Field(default=False, description="Whether file should be public")
    access_permissions: list[str] = Field(default_factory=list, description="Users with access")

class FileProcessingResult(BaseModel):
    """Result of file processing operations"""
    
    attachment_id: str = Field(..., description="ID of the processed attachment")
    processing_successful: bool = Field(..., description="Whether processing was successful")
    processing_time: float = Field(..., description="Time taken to process in seconds")
    extracted_text: Optional[str] = Field(default=None, description="Text extracted from the file")
    extracted_metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata extracted from file")
    error_message: Optional[str] = Field(default=None, description="Error message if processing failed")
    processed_at: datetime = Field(default_factory=datetime.now, description="When processing completed")

class FileAttachmentResponse(BaseModel):
    """Response model for file attachment operations"""
    
    attachment: FileAttachment = Field(..., description="The file attachment details")
    download_url: Optional[str] = Field(default=None, description="URL to download the file")
    preview_url: Optional[str] = Field(default=None, description="URL to preview the file")
    processing_result: Optional[FileProcessingResult] = Field(default=None, description="Processing results if available") 