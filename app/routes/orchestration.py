from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import logging
import asyncio
from uuid import uuid4

# Import services
from app.services.classification_engine import TaskClassificationEngine
from app.services.agent_router import AgentRouter
from app.services.sair_loop import SAIRLoop

# Import models
from app.models.orchestration.task_request import Task_Request
from app.models.orchestration.agent_response import Agent_Response
from app.models.orchestration.sair_loop import SAIR_Loop_Data
from app.models.api_models import UserRequestModel, ProcessingResponseModel, RequestStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["orchestration"])

# Error response model for consistent error handling
class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Initialize services
classification_engine = TaskClassificationEngine()
agent_router = AgentRouter()
sair_loop = SAIRLoop()

async def get_db_connection(request: Request):
    """Dependency to get database connection."""
    if request.app.state.mongodb is None:
        # Return a mock database for demo mode
        class MockDB:
            def __getitem__(self, key):
                return MockCollection()
        class MockCollection:
            async def insert_one(self, data):
                return {"inserted_id": "mock_id"}
            async def find_one(self, query):
                return None
            async def find(self, query):
                return []
            async def count_documents(self, query):
                return 0
        return MockDB()
    return request.app.state.mongodb

@router.post("/process-request", response_model=ProcessingResponseModel, status_code=202)
async def process_request(
    user_request: UserRequestModel,
    background_tasks: BackgroundTasks,
    request: Request,
    db=Depends(get_db_connection)
):
    """
    Process a user request through the SEEKER orchestration system.
    
    This endpoint:
    1. Classifies the input using TaskClassificationEngine
    2. Determines optimal routing using AgentRouter
    3. Stores the task request in MongoDB
    4. Returns immediate response with routing decision
    5. Processes agent responses asynchronously
    """
    request_id = str(uuid4())
    start_time = datetime.utcnow()
    
    try:
        logger.info(f"Processing request {request_id} for user {user_request.user_id}")
        
        # Step 1: Classify the request
        logger.info(f"Classifying request {request_id}")
        classification_results = classification_engine.classify_request(user_request.input_text)
        
        if not classification_results:
            raise HTTPException(
                status_code=500,
                detail="Failed to classify request"
            )
        
        # Step 2: Determine routing
        logger.info(f"Determining routing for request {request_id}")
        routing_decision = await agent_router.determine_routing(classification_results)
        
        if not routing_decision:
            raise HTTPException(
                status_code=500,
                detail="Failed to determine routing"
            )
        
        # Step 3: Create Task_Request instance
        task_request = Task_Request(
            request_id=request_id,
            user_id=user_request.user_id,
            input_text=user_request.input_text,
            classification_results=classification_results.get("classification_results", {}),
            routing_decision=routing_decision,
            created_at=start_time
        )
        
        # Step 4: Store in MongoDB
        try:
            await db["task_requests"].insert_one(task_request.dict())
            logger.info(f"Task request {request_id} stored in database")
        except Exception as db_error:
            logger.error(f"Database error storing task request: {str(db_error)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to store task request"
            )
        
        # Step 5: Add background task for agent processing
        background_tasks.add_task(
            process_agent_responses,
            request_id,
            user_request.input_text,
            routing_decision,
            db
        )
        
        # Step 6: Calculate processing time and format response
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        estimated_time = routing_decision.get("estimated_processing_time", 5.0)
        
        # Format estimated response time as human-readable string
        if estimated_time < 1:
            estimated_response_time = "less than 1 second"
        elif estimated_time < 60:
            estimated_response_time = f"{int(estimated_time)}-{int(estimated_time + 1)} seconds"
        else:
            minutes = int(estimated_time // 60)
            estimated_response_time = f"{minutes}-{minutes + 1} minutes"
        
        # Step 7: Return immediate response using ProcessingResponseModel
        response = ProcessingResponseModel(
            request_id=request_id,
            status=RequestStatus.PROCESSING,
            classification_results=classification_results.get("classification_results", {}),
            routing_decision={
                "assigned_agents": routing_decision.get("assigned_agents", []),
                "routing_logic": routing_decision.get("routing_logic", ""),
                "primary_category": classification_results.get("routing_decision", {}).get("primary_category", "unknown"),
                "confidence": classification_results.get("confidence", 0.0),
                "estimated_processing_time": estimated_time
            },
            estimated_response_time=estimated_response_time,
            confidence=classification_results.get("confidence", 0.0),
            timestamp=datetime.utcnow(),
            message="Request accepted and being processed"
        )
        
        logger.info(f"Request {request_id} processed successfully in {processing_time:.3f}s")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing request {request_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

async def process_agent_responses(
    request_id: str,
    input_text: str,
    routing_decision: Dict[str, Any],
    db
):
    """
    Background task to process agent responses asynchronously.
    
    This function:
    1. Simulates agent processing
    2. Creates Agent_Response instances
    3. Stores responses in MongoDB
    4. Updates SAIR loop with feedback
    """
    try:
        logger.info(f"Processing agent responses for request {request_id}")
        
        assigned_agents = routing_decision.get("assigned_agents", [])
        responses = []
        
        # Process each assigned agent
        for agent_id in assigned_agents:
            # Simulate agent processing time
            processing_time = 2.0 + (hash(agent_id) % 3)  # Random processing time between 2-5 seconds
            await asyncio.sleep(processing_time)
            
            # Generate mock response content based on agent type
            if "technical" in agent_id:
                response_content = f"Technical analysis of: {input_text[:100]}..."
            elif "strategic" in agent_id:
                response_content = f"Strategic insights for: {input_text[:100]}..."
            elif "local" in agent_id:
                response_content = f"Secure processing completed for: {input_text[:100]}..."
            else:
                response_content = f"Processed request: {input_text[:100]}..."
            
            # Create Agent_Response instance
            agent_response = Agent_Response(
                response_id=str(uuid4()),
                request_id=request_id,
                agent_id=agent_id,
                response_content=response_content,
                response_confidence=0.85 + (hash(agent_id) % 15) / 100,  # Random confidence 0.85-1.0
                processing_time=processing_time,
                vector_embedding=[0.1, 0.2, 0.3, 0.4, 0.5],  # Mock embedding
                created_at=datetime.utcnow()
            )
            
            # Store in MongoDB
            await db["agent_responses"].insert_one(agent_response.dict())
            responses.append(agent_response)
            
            logger.info(f"Agent {agent_id} response stored for request {request_id}")
        
        # Update SAIR loop with mock feedback
        await update_sair_loop_with_feedback(request_id, responses, db)
        
        logger.info(f"All agent responses processed for request {request_id}")
        
    except Exception as e:
        logger.error(f"Error processing agent responses for request {request_id}: {str(e)}")

async def update_sair_loop_with_feedback(
    request_id: str,
    responses: list,
    db
):
    """
    Update SAIR loop with feedback data for learning.
    """
    try:
        # Calculate mock feedback scores based on response quality
        avg_confidence = sum(r.response_confidence for r in responses) / len(responses) if responses else 0.0
        avg_processing_time = sum(r.processing_time for r in responses) / len(responses) if responses else 0.0
        
        # Mock user satisfaction and accuracy scores
        user_satisfaction = min(0.95, avg_confidence + 0.1)  # High satisfaction for good confidence
        accuracy_score = min(0.90, avg_confidence + 0.05)    # High accuracy for good confidence
        
        # Process feedback through SAIR loop
        sair_result = await sair_loop.process_feedback(
            request_id=request_id,
            user_satisfaction=user_satisfaction,
            accuracy_score=accuracy_score
        )
        
        # Store SAIR loop data in MongoDB
        sair_loop_data = SAIR_Loop_Data(
            loop_id=f"sair_{datetime.utcnow().timestamp()}",
            request_id=request_id,
            success_metrics={
                "user_satisfaction": user_satisfaction,
                "accuracy_score": accuracy_score,
                "avg_confidence": avg_confidence,
                "avg_processing_time": avg_processing_time
            },
            learning_updates=sair_result.get("insights_generated", 0),
            routing_adjustments=sair_result.get("refinements_applied", 0),
            timestamp=datetime.utcnow()
        )
        
        await db["sair_loop_data"].insert_one(sair_loop_data.dict())
        
        logger.info(f"SAIR loop updated for request {request_id}")
        
    except Exception as e:
        logger.error(f"Error updating SAIR loop for request {request_id}: {str(e)}")

@router.get("/status/{request_id}")
async def get_request_status(
    request_id: str,
    request: Request,
    db=Depends(get_db_connection)
):
    """
    Get the status of a processed request.
    
    This endpoint provides detailed information about the processing status,
    including task request details, agent responses, and SAIR loop data.
    """
    try:
        # Validate request_id format
        if not request_id or len(request_id.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid request ID format"
            )
        
        # Get task request
        task_request = await db["task_requests"].find_one({"request_id": request_id})
        if not task_request:
            raise HTTPException(
                status_code=404,
                detail="Request not found"
            )
        
        # Get agent responses
        agent_responses = await db["agent_responses"].find({"request_id": request_id}).to_list(100)
        
        # Get SAIR loop data
        sair_data = await db["sair_loop_data"].find_one({"request_id": request_id})
        
        # Determine status based on responses
        if agent_responses:
            status = "completed"
            total_processing_time = sum(r.get("processing_time", 0) for r in agent_responses)
            avg_confidence = sum(r.get("response_confidence", 0) for r in agent_responses) / len(agent_responses)
        else:
            status = "processing"
            total_processing_time = 0.0
            avg_confidence = 0.0
        
        # Format response
        response = {
            "request_id": request_id,
            "status": status,
            "task_request": {
                "user_id": task_request.get("user_id"),
                "input_text": task_request.get("input_text", "")[:100] + "..." if len(task_request.get("input_text", "")) > 100 else task_request.get("input_text", ""),
                "classification_results": task_request.get("classification_results", {}),
                "routing_decision": task_request.get("routing_decision", ""),
                "created_at": task_request.get("created_at")
            },
            "agent_responses": [
                {
                    "response_id": r.get("response_id"),
                    "agent_id": r.get("agent_id"),
                    "response_content": r.get("response_content", "")[:200] + "..." if len(r.get("response_content", "")) > 200 else r.get("response_content", ""),
                    "confidence": r.get("response_confidence", 0.0),
                    "processing_time": r.get("processing_time", 0.0),
                    "created_at": r.get("created_at")
                }
                for r in agent_responses
            ],
            "sair_loop_data": sair_data,
            "response_count": len(agent_responses),
            "total_processing_time": round(total_processing_time, 3),
            "average_confidence": round(avg_confidence, 3),
            "timestamp": datetime.utcnow()
        }
        
        logger.info(f"Status retrieved for request {request_id}: {status}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting request status for {request_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/performance-metrics")
async def get_performance_metrics(
    request: Request,
    db=Depends(get_db_connection)
):
    """
    Get performance metrics for the orchestration system.
    """
    try:
        # Get analytics from agent router
        router_analytics = await agent_router.get_performance_analytics()
        
        # Get learning summary from SAIR loop
        learning_summary = await sair_loop.get_learning_summary()
        
        # Get database statistics
        total_requests = await db["task_requests"].count_documents({})
        total_responses = await db["agent_responses"].count_documents({})
        total_sair_loops = await db["sair_loop_data"].count_documents({})
        
        return {
            "router_analytics": router_analytics,
            "learning_summary": learning_summary,
            "database_stats": {
                "total_requests": total_requests,
                "total_responses": total_responses,
                "total_sair_loops": total_sair_loops
            },
            "timestamp": datetime.utcnow()
        } 
    except Exception as e:
        logger.error(f"Error getting performance metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/status")
async def get_system_status(
    request: Request,
    db=Depends(get_db_connection)
):
    """
    Get overall system status and recent activity.
    
    This endpoint provides a high-level overview of the orchestration system,
    including recent requests, system health, and basic statistics.
    """
    try:
        # Get recent requests (last 10)
        recent_requests = await db["task_requests"].find().sort("created_at", -1).limit(10).to_list(10)
        
        # Get basic statistics
        total_requests = await db["task_requests"].count_documents({})
        total_responses = await db["agent_responses"].count_documents({})
        total_sair_loops = await db["sair_loop_data"].count_documents({})
        
        # Calculate processing status
        processing_requests = await db["task_requests"].count_documents({"status": "processing"})
        completed_requests = await db["task_requests"].count_documents({"status": "completed"})
        
        # Get recent activity summary
        recent_activity = []
        for req in recent_requests:
            recent_activity.append({
                "request_id": req.get("request_id"),
                "user_id": req.get("user_id"),
                "status": req.get("status", "unknown"),
                "created_at": req.get("created_at"),
                "input_preview": req.get("input_text", "")[:50] + "..." if len(req.get("input_text", "")) > 50 else req.get("input_text", "")
            })
        
        response = {
            "system_status": "operational",
            "total_requests": total_requests,
            "total_responses": total_responses,
            "total_sair_loops": total_sair_loops,
            "processing_requests": processing_requests,
            "completed_requests": completed_requests,
            "recent_activity": recent_activity,
            "timestamp": datetime.utcnow()
        }
        
        logger.info("System status retrieved successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/classify")
async def classify_request(
    request_data: Dict[str, Any],
    request: Request
):
    """
    Classify a text input without processing it through the full orchestration system.
    
    This endpoint is useful for testing classification logic or getting
    classification results without creating a full task request.
    """
    try:
        input_text = request_data.get("input_text")
        if not input_text or not input_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Input text is required"
            )
        
        # Classify the input
        classification_results = classification_engine.classify_request(input_text)
        
        if not classification_results:
            raise HTTPException(
                status_code=500,
                detail="Failed to classify request"
            )
        
        # Format response
        response = {
            "input_text": input_text,
            "classification_results": classification_results.get("classification_results", {}),
            "confidence": classification_results.get("confidence", 0.0),
            "routing_suggestion": classification_results.get("routing_decision", {}),
            "timestamp": datetime.utcnow()
        }
        
        logger.info(f"Request classified successfully: confidence={classification_results.get('confidence', 0.0):.3f}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error classifying request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) 