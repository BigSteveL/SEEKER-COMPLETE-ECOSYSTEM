"""
Database connection and utilities for SEEKER Global Analytics System
"""

from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)

# Global MongoDB client
_mongo_client = None

def get_mongo_client() -> AsyncIOMotorClient:
    """Get MongoDB client instance"""
    global _mongo_client
    
    if _mongo_client is None:
        try:
            _mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
            logger.info("✅ MongoDB client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize MongoDB client: {e}")
            raise
    
    return _mongo_client

def close_mongo_client():
    """Close MongoDB client connection"""
    global _mongo_client
    
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        logger.info("✅ MongoDB client connection closed") 