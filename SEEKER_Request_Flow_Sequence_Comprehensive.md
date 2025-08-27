# SEEKER Request Flow Sequence - Comprehensive Overview

```mermaid
sequenceDiagram
    participant User as User
    participant Voice as Voice Interface
    participant Web as Web Interface
    participant Main as Main Application
    participant Orchestration as Orchestration Router
    participant Classification as NLP Classification Engine
    participant AgentRouter as Agent Router
    participant SAIRLoop as SAIR Loop
    participant AIAgent as AI Agent
    participant Commerce as Commerce Platform
    participant Tactical as Tactical System
    participant MongoDB as MongoDB
    participant External as External Services

    Note over User,External: Complete Request Processing Flow

    %% Phase 1: Voice Input Processing
    rect rgb(240, 248, 255)
        Note over User,Classification: Phase 1: Voice Input & NLP Processing
        User->>Voice: Voice input (speech)
        Voice->>Voice: Speech Recognition
        Voice->>Voice: Convert to text
        Voice->>Web: Send text input
        User->>Web: Text input (alternative)
        Web->>Main: POST /api/v1/orchestration/process-request
    end

    %% Phase 2: NLP Classification
    rect rgb(255, 248, 240)
        Note over Main,Classification: Phase 2: NLP Classification & Analysis
        Main->>Orchestration: Forward request
        Orchestration->>Classification: classify_request(input_text)
        
        Classification->>Classification: Analyze keywords
        Classification->>Classification: Calculate category scores
        Classification->>Classification: Determine confidence level
        Classification-->>Orchestration: Return classification results
    end

    %% Phase 3: Agent Routing
    rect rgb(248, 255, 248)
        Note over Orchestration,AgentRouter: Phase 3: Intelligent Agent Routing
        Orchestration->>AgentRouter: determine_routing(classification_results)
        
        AgentRouter->>AgentRouter: Analyze agent capabilities
        AgentRouter->>AgentRouter: Check performance metrics
        AgentRouter->>AgentRouter: Apply routing weights
        AgentRouter->>AgentRouter: Select optimal agents
        AgentRouter-->>Orchestration: Return routing decision
    end

    %% Phase 4: Database Storage
    rect rgb(255, 255, 240)
        Note over Orchestration,MongoDB: Phase 4: Request Storage & Tracking
        Orchestration->>MongoDB: Store Task_Request
        MongoDB-->>Orchestration: Confirm storage
        
        Orchestration->>MongoDB: Store routing decision
        MongoDB-->>Orchestration: Confirm storage
    end

    %% Phase 5: Agent Processing
    rect rgb(248, 240, 255)
        Note over Orchestration,AIAgent: Phase 5: AI Agent Processing
        Orchestration->>AIAgent: Process request (background task)
        
        AIAgent->>Commerce: Execute commerce-related tasks
        AIAgent->>Tactical: Execute tactical system tasks
        AIAgent->>External: Call external services
        
        Commerce-->>AIAgent: Return commerce results
        Tactical-->>AIAgent: Return tactical results
        External-->>AIAgent: Return external data
        
        AIAgent->>AIAgent: Synthesize response
        AIAgent->>MongoDB: Store Agent_Response
        MongoDB-->>AIAgent: Confirm storage
    end

    %% Phase 6: Response Synthesis
    rect rgb(255, 240, 248)
        Note over AIAgent,Orchestration: Phase 6: Response Synthesis & Optimization
        AIAgent->>Orchestration: Return processed response
        
        Orchestration->>Orchestration: Combine agent responses
        Orchestration->>Orchestration: Calculate confidence scores
        Orchestration->>Orchestration: Format final response
        
        Orchestration-->>Main: Return ProcessingResponseModel
        Main-->>Web: Return immediate response with request_id
        Web-->>User: Display response preview
    end

    %% Phase 7: SAIR Loop Learning
    rect rgb(240, 255, 248)
        Note over Orchestration,SAIRLoop: Phase 7: SAIR Loop Learning & Optimization
        Orchestration->>SAIRLoop: process_feedback(request_id, satisfaction, accuracy)
        
        SAIRLoop->>SAIRLoop: search_patterns()
        Note over SAIRLoop: Search for performance patterns and trends
        
        SAIRLoop->>SAIRLoop: act_on_insights()
        Note over SAIRLoop: Take actions based on insights (threshold adjustments, weight updates)
        
        SAIRLoop->>SAIRLoop: interpret_results()
        Note over SAIRLoop: Generate insights from action results
        
        SAIRLoop->>SAIRLoop: refine_algorithms()
        Note over SAIRLoop: Update algorithms and routing weights
        
        SAIRLoop->>Classification: Update classification algorithms
        SAIRLoop->>AgentRouter: Update routing weights
        SAIRLoop->>MongoDB: Store SAIR_Loop_Data
        MongoDB-->>SAIRLoop: Confirm storage
    end

    %% Phase 8: Status Monitoring
    rect rgb(248, 248, 255)
        Note over User,MongoDB: Phase 8: Real-time Status Monitoring
        User->>Web: Check request status
        Web->>Main: GET /api/v1/orchestration/status/{request_id}
        Main->>Orchestration: Get status
        Orchestration->>MongoDB: Query Task_Request, Agent_Response, SAIR_Data
        MongoDB-->>Orchestration: Return status data
        Orchestration-->>Main: Return detailed status
        Main-->>Web: Return status information
        Web-->>User: Display complete results
    end

    Note over User,External: Request Processing Complete
```

## Request Flow Phases Explained:

### **Phase 1: Voice Input & NLP Processing**
- **Voice Input**: User provides voice input through speech recognition
- **Speech Recognition**: Web Speech API converts speech to text
- **Text Processing**: Voice interface processes and formats text input
- **Request Submission**: Formatted request sent to orchestration system

### **Phase 2: NLP Classification & Analysis**
- **Keyword Analysis**: Classification engine analyzes input text
- **Category Scoring**: Calculates scores for 8 SEEKER categories:
  - Product Search, Price Negotiation, Verification
  - Supply Chain, Translation, Technical, Strategic, Sensitive
- **Confidence Calculation**: Determines overall classification confidence
- **Routing Preparation**: Prepares classification results for routing

### **Phase 3: Intelligent Agent Routing**
- **Agent Analysis**: Evaluates available AI agents and their capabilities
- **Performance Metrics**: Considers historical performance data
- **Routing Weights**: Applies learned routing weights from SAIR loop
- **Agent Selection**: Selects optimal agents based on classification and confidence
- **Load Balancing**: Ensures efficient distribution across agents

### **Phase 4: Request Storage & Tracking**
- **Task Request Storage**: Stores initial request with metadata
- **Routing Decision Storage**: Records routing decisions for tracking
- **Request ID Generation**: Creates unique identifier for request lifecycle
- **Audit Trail**: Maintains complete request history

### **Phase 5: AI Agent Processing**
- **Background Processing**: Executes agent tasks asynchronously
- **Commerce Platform Integration**: Handles product search, pricing, marketplace tasks
- **Tactical System Integration**: Manages video, holographic, file operations
- **External Service Calls**: Integrates with manufacturing, shipping, analytics
- **Response Synthesis**: Combines results from multiple agents

### **Phase 6: Response Synthesis & Optimization**
- **Response Combination**: Merges responses from multiple agents
- **Confidence Scoring**: Calculates overall response confidence
- **Format Optimization**: Formats response for user consumption
- **Immediate Feedback**: Provides immediate response with request tracking

### **Phase 7: SAIR Loop Learning & Optimization**
- **Search**: Analyzes patterns in recent performance data
- **Act**: Takes actions based on insights (threshold adjustments, weight updates)
- **Interpret**: Generates insights from action results
- **Refine**: Updates algorithms and routing weights
- **Continuous Learning**: Improves system performance over time

### **Phase 8: Real-time Status Monitoring**
- **Status Tracking**: Users can monitor request processing in real-time
- **Detailed Information**: Provides comprehensive status information
- **Performance Metrics**: Shows processing time, confidence scores
- **Complete Results**: Delivers final processed results to user

## Key Features:

### **Asynchronous Processing**
- Immediate response with request ID
- Background processing for complex tasks
- Real-time status updates

### **Intelligent Routing**
- AI-powered classification with 8 categories
- Confidence-based agent assignment
- Load balancing and performance optimization

### **Continuous Learning**
- SAIR loop for performance optimization
- Pattern recognition and adaptation
- Algorithm refinement based on feedback

### **Multi-modal Integration**
- Voice input with speech recognition
- Text input processing
- Multilingual support (10 languages)

### **Comprehensive Tracking**
- Full request lifecycle monitoring
- Performance metrics collection
- Learning data storage and analysis 