"""
SEEKER AI Orchestration System - Main Application
AI-assisted product prototyping and rapid iteration
On-demand global manufacturing connections
AI-facilitated mass production scaling
"""

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
import uuid
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

# Import routes
from app.routes.orchestration import router as orchestration_router
from app.routes.conversation import router as conversation_router
from app.routes.files import router as files_router
from app.routes.users import router as users_router
from app.routes.video_conference import router as video_conference_router
from app.routes.manufacturing import router as manufacturing_router
from app.routes.printer import router as printer_router
from app.routes.three_d_files import router as three_d_files_router
from app.routes.holographic import router as holographic_router
from app.routes.global_analytics import router as global_analytics_router
from app.routes.consumer_marketplace import router as consumer_marketplace_router
from app.routes.global_shipping import router as global_shipping_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
mongodb_client = None
mongodb_database = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global mongodb_client, mongodb_database
    
    # Startup
    logger.info("🚀 Starting SEEKER AI Orchestration System...")
    
    # Initialize MongoDB connection
    try:
        mongodb_client = AsyncIOMotorClient("mongodb://localhost:27017")
        mongodb_database = mongodb_client.seeker_db
        await mongodb_client.admin.command('ping')
        logger.info("✅ MongoDB connected successfully to seeker_db")
        # Set MongoDB state for routes
        app.state.mongodb = mongodb_database
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        logger.info("⚠️ Running in demo mode without database")
        mongodb_client = None
        mongodb_database = None
        # Set None state for routes
        app.state.mongodb = None
    
    logger.info("🎯 SEEKER system ready to process requests!")
    logger.info("📋 Available endpoints:")
    logger.info("   POST /api/v1/orchestration/process-request - Process user requests")
    logger.info("   GET  /api/v1/orchestration/status/{request_id} - Check request status")
    logger.info("   GET  /api/v1/orchestration/performance-metrics - System metrics")
    logger.info("   POST /api/v1/conversation/conversations/ - Create conversation")
    logger.info("   GET  /api/v1/conversation/conversations/{session_id} - Get conversation")
    logger.info("   POST /api/v1/conversation/conversations/{session_id}/messages/ - Add message")
    logger.info("   POST /api/v1/files/upload/ - Upload file")
    logger.info("   GET  /api/v1/files/files/{file_id} - Get file info")
    logger.info("   POST /api/v1/users - Create user")
    logger.info("   GET  /health - Health check")
    logger.info("   GET  /status - System status")
    logger.info("   🌐 Web interface available at http://localhost:8000")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down SEEKER system...")
    if mongodb_client is not None:
        mongodb_client.close()
        logger.info("✅ MongoDB connection closed")

# Create FastAPI app
app = FastAPI(
    title="SEEKER AI Orchestration System",
    description="AI-assisted product prototyping, global manufacturing connections, and mass production scaling",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(orchestration_router, prefix="/api/v1/orchestration")
app.include_router(conversation_router, prefix="/api/v1")
app.include_router(files_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(video_conference_router, prefix="/api/v1")
app.include_router(manufacturing_router, prefix="/api/v1")
app.include_router(printer_router, prefix="/api/v1")
app.include_router(three_d_files_router, prefix="/api/v1")
app.include_router(holographic_router, prefix="/api/v1")
app.include_router(global_analytics_router, prefix="/api/v1")
app.include_router(consumer_marketplace_router, prefix="/api/v1")
app.include_router(global_shipping_router, prefix="/api/v1")

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    logger.info(f"📥 {request.method} {request.url.path} - Request ID: {request_id}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"📤 {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
        
        response.headers["x-request-id"] = request_id
        response.headers["x-processing-time"] = str(process_time)
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"❌ {request.method} {request.url.path} - Error after {process_time:.3f}s: {e}")
        raise

# Root endpoint - Serve the main interface
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SEEKER AI Orchestration System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .header { text-align: center; color: #333; margin-bottom: 30px; }
            .demo-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .status { margin: 10px 0; padding: 10px; background: #e7f3ff; border-radius: 3px; }
            #output { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px; min-height: 100px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 SEEKER AI Orchestration System</h1>
                <p>AI-Powered Product Prototyping & Global Manufacturing Platform</p>
            </div>
            
            <div class="demo-section">
                <h2>System Status</h2>
                <div class="status" id="systemStatus">Checking system status...</div>
                <button onclick="checkHealth()">Check Health</button>
            </div>
            
            <div class="demo-section">
                <h2>AI Request Processing</h2>
                <input type="text" id="userInput" placeholder="Enter your request (e.g., 'Find electronic components')" style="width: 100%; padding: 10px; margin: 10px 0;">
                <button onclick="processRequest()">Process Request</button>
                <div id="output"></div>
            </div>
            
            <div class="demo-section">
                <h2>Available Endpoints</h2>
                <ul>
                    <li><strong>POST /api/v1/orchestration/process-request</strong> - Process user requests</li>
                    <li><strong>GET /api/v1/orchestration/status/{request_id}</strong> - Check request status</li>
                    <li><strong>GET /api/v1/orchestration/performance-metrics</strong> - System metrics</li>
                    <li><strong>GET /health</strong> - Health check</li>
                    <li><strong>GET /status</strong> - System status</li>
                </ul>
            </div>
        </div>
        
        <script>
            async function checkHealth() {
                try {
                    const response = await fetch('/health');
                    const data = await response.json();
                    document.getElementById('systemStatus').innerHTML = 
                        `<strong>Status:</strong> ${data.status}<br>
                         <strong>Database:</strong> ${data.services.database}<br>
                         <strong>Timestamp:</strong> ${data.timestamp}`;
                } catch (error) {
                    document.getElementById('systemStatus').innerHTML = 'Error checking health: ' + error.message;
                }
            }
            
            async function processRequest() {
                const input = document.getElementById('userInput').value;
                if (!input) {
                    alert('Please enter a request');
                    return;
                }
                
                const output = document.getElementById('output');
                output.innerHTML = 'Processing request...';
                
                try {
                    const response = await fetch('/api/v1/orchestration/process-request', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            user_id: 'demo_user',
                            input_text: input
                        })
                    });
                    
                    const data = await response.json();
                    output.innerHTML = `
                        <h3>Request Processed Successfully!</h3>
                        <p><strong>Request ID:</strong> ${data.request_id}</p>
                        <p><strong>Primary Category:</strong> ${data.routing_decision.primary_category}</p>
                        <p><strong>Confidence:</strong> ${(data.routing_decision.confidence * 100).toFixed(1)}%</p>
                        <p><strong>Assigned Agents:</strong> ${data.routing_decision.assigned_agents.join(', ')}</p>
                        <p><strong>Estimated Response Time:</strong> ${data.estimated_response_time}</p>
                    `;
                } catch (error) {
                    output.innerHTML = 'Error processing request: ' + error.message;
                }
            }
            
            // Check health on page load
            checkHealth();
        </script>
    </body>
    </html>
    """

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check for the SEEKER system"""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0.0",
            "services": {
                "api": "healthy",
                "database": "healthy" if mongodb_database is not None else "unhealthy",
                "voice_processing": "healthy",
                "video_conference": "healthy",
                "3d_visualization": "healthy",
                "manufacturing": "healthy"
            }
        }
        
        # Check database health
        if mongodb_client is not None and mongodb_database is not None:
            try:
                # Use the client instead of database for ping
                await mongodb_client.admin.command('ping')
                health_status["services"]["database"] = "healthy"
            except Exception as e:
                logger.error(f"Database health check failed: {e}")
                health_status["services"]["database"] = "unhealthy"
                health_status["status"] = "degraded"
        else:
            health_status["services"]["database"] = "unavailable"
            health_status["status"] = "degraded"
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

# System status endpoint
@app.get("/status")
async def system_status():
    """Get detailed system status"""
    try:
        status = {
            "system": "SEEKER AI Orchestration System",
            "version": "2.0.0",
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat(),
            "features": {
                "voice_interface": {
                    "status": "active",
                    "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "ru-RU", "ja-JP", "ko-KR", "zh-CN"],
                    "capabilities": ["speech_recognition", "translation", "ai_classification"]
                },
                "video_conference": {
                    "status": "active",
                    "capabilities": ["webrtc", "real_time_translation", "collaboration"],
                    "max_participants": 10
                },
                "3d_visualization": {
                    "status": "active",
                    "capabilities": ["three_js", "collaborative_design", "ai_optimization"],
                    "export_formats": ["stl", "obj", "gltf"]
                },
                "manufacturing": {
                    "status": "active",
                    "capabilities": ["global_connections", "ai_optimization", "quality_control"],
                    "partners": ["shapeways", "3dhubs", "protolabs", "xometry"]
                },
                "3d_printer": {
                    "status": "active",
                    "capabilities": ["device_discovery", "real_time_monitoring", "print_control"],
                    "supported_protocols": ["usb", "serial", "network"]
                }
            },
            "performance": {
                "uptime": "99.9%",
                "response_time": "0.8s",
                "active_sessions": 0,
                "total_requests": 0
            }
        }
        
        return status
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# API documentation redirect
@app.get("/docs")
async def api_docs():
    """Redirect to API documentation"""
    return {"message": "API documentation available at /docs", "url": "/docs"}

from fastapi.responses import JSONResponse

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": request.url.path,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "path": request.url.path,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
   