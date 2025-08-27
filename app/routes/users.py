"""
SEEKER Users API Routes
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
async def create_user():
    """Create user endpoint"""
    return {"message": "Create user endpoint"} 