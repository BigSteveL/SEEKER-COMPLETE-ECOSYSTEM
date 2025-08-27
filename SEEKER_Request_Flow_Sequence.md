# SEEKER Request Flow Sequence Diagram

```mermaid
sequenceDiagram
    participant User as User
    participant UI as Web Interface
    participant Voice as Voice Interface
    participant Main as Main Application
    participant Orchestration as Orchestration Router
    participant Classification as Classification Engine
    participant AgentRouter as Agent Router
    participant SAIRLoop as SAIR Loop
    participant MongoDB as MongoDB
    participant Agent as AI Agent
    participant Service as Specialized Service

    Note over User,Service: Request Processing Flow

    %% User Input Phase
    User->>UI: Submit request via web interface
    User->>Voice: Voice input (alternative)
    Voice->>UI: Convert speech to text
    UI->>Main: POST /api/v1/orchestration/process-request

    %% Request Processing Phase
    Main->>Orchestration: Forward request
    Orchestration->>Classification: classify_request(input_text)
    
    Note over Classification: Analyze keywords and determine category
    Classification-->>Orchestration: Return classification results
    
    Orchestration->>AgentRouter: determine_routing(classification_results)
    
    Note over AgentRouter: Assign optimal agents based on category and confidence
    AgentRouter-->>Orchestration: Return routing decision
    
    %% Database Storage Phase
    Orchestration->>MongoDB: Store Task_Request
    MongoDB-->>Orchestration: Confirm storage
    
    %% Background Processing Phase
    Orchestration->>Agent: Process request (background task)
    Agent->>Service: Execute specialized processing
    
    Note over Service: Handle category-specific logic
    Service-->>Agent: Return processing results
    
    Agent->>MongoDB: Store Agent_Response
    MongoDB-->>Agent: Confirm storage
    
    %% SAIR Loop Learning Phase
    Agent->>SAIRLoop: process_feedback(request_id, satisfaction, accuracy)
    
    Note over SAIRLoop: Search, Act, Interpret, Refine
    SAIRLoop->>SAIRLoop: search_patterns()
    SAIRLoop->>SAIRLoop: act_on_insights()
    SAIRLoop->>SAIRLoop: interpret_results()
    SAIRLoop->>SAIRLoop: refine_algorithms()
    
    SAIRLoop->>MongoDB: Store SAIR_Loop_Data
    MongoDB-->>SAIRLoop: Confirm storage
    
    %% Response Generation Phase
    Orchestration-->>Main: Return ProcessingResponseModel
    Main-->>UI: Return immediate response with request_id
    
    %% Status Checking Phase
    User->>UI: Check request status
    UI->>Main: GET /api/v1/orchestration/status/{request_id}
    Main->>Orchestration: Get status
    Orchestration->>MongoDB: Query Task_Request, Agent_Response, SAIR_Data
    MongoDB-->>Orchestration: Return status data
    Orchestration-->>Main: Return detailed status
    Main-->>UI: Return status information
    UI-->>User: Display results

    Note over User,Service: End of Request Flow
```

## Request Flow Stages:

### 1. User Input Phase
- **Web Interface**: User submits request via form
- **Voice Interface**: Alternative input method with speech-to-text conversion
- **Request Format**: JSON payload with user_id and input_text

### 2. Request Processing Phase
- **Classification Engine**: Analyzes input text using keyword matching
- **Categories**: Product search, price negotiation, verification, supply chain, translation
- **Confidence Scoring**: Determines routing confidence (0-1 scale)
- **Agent Router**: Assigns optimal agents based on category and confidence

### 3. Database Storage Phase
- **Task Request**: Stores initial request with classification and routing data
- **Request ID**: Unique identifier for tracking throughout the process
- **Metadata**: Timestamp, user_id, input_text, classification_results

### 4. Background Processing Phase
- **Agent Assignment**: Routes to specialized AI agents
- **Service Processing**: Category-specific business logic execution
- **Response Generation**: Creates structured agent responses
- **Database Storage**: Stores agent responses with confidence scores

### 5. SAIR Loop Learning Phase
- **Search**: Analyze patterns in recent performance data
- **Act**: Take actions based on insights (threshold adjustments, weight updates)
- **Interpret**: Generate insights from action results
- **Refine**: Update algorithms and routing weights
- **Learning**: Continuous improvement based on feedback

### 6. Response Generation Phase
- **Immediate Response**: Returns request_id and estimated processing time
- **Status Tracking**: Provides endpoint for checking request status
- **Performance Metrics**: Includes confidence scores and routing decisions

### 7. Status Checking Phase
- **Real-time Updates**: Users can check processing status
- **Detailed Information**: Shows task request, agent responses, and SAIR data
- **Completion Status**: Indicates when processing is finished

## Key Features:

### Asynchronous Processing
- Immediate response with request ID
- Background processing for complex tasks
- Real-time status updates

### Intelligent Routing
- AI-powered classification
- Confidence-based agent assignment
- Load balancing across agents

### Continuous Learning
- SAIR loop for performance optimization
- Pattern recognition and adaptation
- Algorithm refinement based on feedback

### Multi-modal Input
- Text-based requests
- Voice input with speech recognition
- Multilingual support (10 languages)

### Comprehensive Tracking
- Full request lifecycle monitoring
- Performance metrics collection
- Learning data storage 