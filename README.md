# SEEKER Multi-Intelligence Orchestration Framework

A sophisticated AI agent orchestration and routing system built with FastAPI, MongoDB, and intelligent classification algorithms.

## 🏗️ Architecture Overview

The SEEKER framework provides intelligent routing and orchestration of AI agents based on request classification and confidence scoring. It implements a SAIR (Self-Adaptive Intelligent Routing) loop for continuous learning and optimization.

### Core Components

```
/app
├── main.py                 # FastAPI app entry point with CORS, middleware, health checks
├── models/
│   ├── core.py            # Consolidated core data models (User, Task_Request, Agent_Response, Device)
│   ├── api_models.py      # API request/response models
│   ├── core/              # Individual core models
│   └── orchestration/     # Orchestration-specific models
├── services/
│   ├── classification_engine.py  # NLP task classification engine
│   ├── agent_router.py           # AI agent routing with confidence thresholds
│   └── sair_loop.py              # Adaptive learning system
├── routes/
│   └── orchestration.py   # API endpoints for request processing
└── test_seeker.py         # Comprehensive test suite
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- MongoDB (running on localhost:27017)
- Required Python packages (see requirements.txt)

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install fastapi uvicorn motor pymongo pydantic
   ```

2. **Install and start MongoDB:**
   - Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
   - Install and start the MongoDB service
   - Verify it's running on port 27017

3. **Start the SEEKER server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API documentation:**
   - OpenAPI docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📋 Core Models

### User Model
```python
class User(BaseModel):
    user_id: str                    # Unique user identifier
    personal_profile: Dict[str, Any] # User profile information
    device_registrations: List[Dict] # Registered devices
    created_at: datetime           # Creation timestamp
    updated_at: Optional[datetime] # Last update timestamp
```

### Task_Request Model
```python
class Task_Request(BaseModel):
    request_id: str                # Unique request identifier
    user_id: str                   # User making the request
    input_text: Optional[str]      # Text input (max 10,000 chars)
    input_audio: Optional[bytes]   # Audio input
    classification_results: Dict   # Classification scores
    routing_decision: Optional[str] # Routing logic used
    status: RequestStatus          # Current processing status
    created_at: datetime          # Creation timestamp
```

### Agent_Response Model
```python
class Agent_Response(BaseModel):
    response_id: str               # Unique response identifier
    request_id: str                # Related task request
    agent_id: str                  # Responding agent ID
    agent_type: AgentType          # Agent type (technical/strategic/sensitive)
    response_content: str          # Response content (max 50,000 chars)
    response_confidence: float     # Confidence score (0.0-1.0)
    processing_time: float         # Processing time in seconds
    vector_embedding: List[float]  # Response embedding
    metadata: Optional[Dict]       # Additional metadata
    created_at: datetime          # Creation timestamp
```

## 🔧 Services

### Classification Engine
- **Purpose**: Analyzes input text and classifies requests into categories
- **Categories**: Technical, Strategic, Sensitive
- **Features**: 
  - Keyword-based scoring
  - Confidence calculation
  - Routing decision logic

### Agent Router
- **Purpose**: Determines optimal AI agent routing based on classification
- **Features**:
  - Confidence threshold-based routing
  - Multi-agent assignment for complex requests
  - Human escalation for low-confidence cases

### SAIR Loop
- **Purpose**: Self-Adaptive Intelligent Routing for continuous learning
- **Features**:
  - Performance feedback collection
  - Routing optimization
  - Confidence threshold adjustment

## 🌐 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | System overview and available endpoints |
| `GET` | `/health` | Health check with service status |
| `GET` | `/status` | Comprehensive system status |
| `POST` | `/api/v1/users` | Create new user |

### Orchestration Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/orchestration/process-request` | Process user request |
| `GET` | `/api/v1/orchestration/status/{request_id}` | Check request status |
| `GET` | `/api/v1/orchestration/performance-metrics` | System performance metrics |

## 🔄 Request Processing Flow

1. **Request Reception**: User submits request via `/process-request`
2. **Classification**: TaskClassificationEngine analyzes input text
3. **Routing Decision**: AgentRouter determines optimal agent assignment
4. **Immediate Response**: Returns processing status and routing info
5. **Background Processing**: Agents process request asynchronously
6. **Response Storage**: Agent responses stored in MongoDB
7. **SAIR Learning**: System learns from performance feedback

## 🧪 Testing

Run the comprehensive test suite:

```bash
python app/test_seeker.py
```

The test suite includes:
- Technical request testing
- Strategic request testing
- Sensitive request testing
- Mixed request testing
- Performance validation

## 🔒 Security Features

- **CORS Middleware**: Configurable cross-origin resource sharing
- **Trusted Host Middleware**: Host validation for security
- **Request Monitoring**: Processing time and request ID tracking
- **Global Exception Handling**: Comprehensive error management
- **Input Validation**: Pydantic model validation for all inputs

## 📊 Monitoring & Logging

- **Request/Response Logging**: All API calls logged with timing
- **Performance Metrics**: Processing time tracking
- **Error Tracking**: Comprehensive error logging
- **Database Monitoring**: Connection health checks
- **System Status**: Real-time system health monitoring

## 🚀 Deployment

### Environment Variables

```bash
MONGODB_URI=mongodb://localhost:27017
DB_NAME=seeker_db
ENVIRONMENT=production
DEBUG=false
ALLOWED_HOSTS=your-domain.com
CORS_ORIGINS=https://your-frontend.com
```

### Production Considerations

1. **Database**: Use MongoDB Atlas or production MongoDB instance
2. **Security**: Configure proper CORS origins and allowed hosts
3. **Logging**: Enable file logging in production
4. **Monitoring**: Set up application monitoring
5. **Scaling**: Use multiple worker processes with uvicorn

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the test suite for usage examples
- Check system logs for error details
- Verify MongoDB connection and status

---

**SEEKER AI Orchestration System** - Intelligent AI agent orchestration and routing with adaptive learning capabilities. 