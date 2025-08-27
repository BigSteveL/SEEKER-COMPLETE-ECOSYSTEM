#!/usr/bin/env python3
"""
Test script for SEEKER AI Orchestration System
Tests the enhanced classification and routing based on patent specifications
"""

import asyncio
import json
import requests
from datetime import datetime

# Test cases based on SEEKER patent categories
TEST_CASES = [
    {
        "name": "Product Search Request",
        "input_text": "Find the best price for electronic components from global suppliers with shipping costs included",
        "expected_category": "product_search"
    },
    {
        "name": "Price Negotiation Request", 
        "input_text": "Negotiate better pricing for bulk purchase of industrial equipment with competitive quotes",
        "expected_category": "price_negotiation"
    },
    {
        "name": "Verification Request",
        "input_text": "Verify the authenticity of luxury goods and check compliance with safety standards",
        "expected_category": "verification"
    },
    {
        "name": "Supply Chain Request",
        "input_text": "Track my order status and monitor inventory levels across the supply chain",
        "expected_category": "supply_chain"
    },
    {
        "name": "Translation Request",
        "input_text": "Translate business documents from English to Chinese for cross-border communication",
        "expected_category": "translation"
    },
    {
        "name": "Technical Request (Legacy)",
        "input_text": "Analyze this code for performance optimization and debugging issues",
        "expected_category": "technical"
    },
    {
        "name": "Strategic Request (Legacy)",
        "input_text": "Develop a business strategy for market expansion and competitive analysis",
        "expected_category": "strategic"
    }
]

def test_classification_engine():
    """Test the classification engine directly"""
    print("🔍 Testing SEEKER Classification Engine...")
    print("=" * 60)
    
    from app.services.classification_engine import TaskClassificationEngine
    
    engine = TaskClassificationEngine()
    
    for test_case in TEST_CASES:
        print(f"\n📋 Test: {test_case['name']}")
        print(f"Input: {test_case['input_text']}")
        
        result = engine.classify_request(test_case['input_text'])
        
        print(f"Classification Results:")
        for category, score in result['classification_results'].items():
            print(f"  {category}: {score:.3f}")
        
        print(f"Confidence: {result['confidence']:.3f}")
        print(f"Primary Category: {result['routing_decision']['primary_category']}")
        print(f"Assigned Agents: {result['routing_decision']['assigned_agents']}")
        
        # Check if expected category has highest score
        scores = result['classification_results']
        primary_category = result['routing_decision']['primary_category']
        
        if primary_category == test_case['expected_category']:
            print("✅ PASS - Correct category identified")
        else:
            print(f"❌ FAIL - Expected {test_case['expected_category']}, got {primary_category}")

async def test_agent_router():
    """Test the agent router directly"""
    print("\n🎯 Testing SEEKER Agent Router...")
    print("=" * 60)
    
    from app.services.agent_router import AgentRouter
    from app.services.classification_engine import TaskClassificationEngine
    
    router = AgentRouter()
    engine = TaskClassificationEngine()
    
    for test_case in TEST_CASES:
        print(f"\n📋 Test: {test_case['name']}")
        
        # Get classification
        classification = engine.classify_request(test_case['input_text'])
        
        # Get routing decision
        routing = await router.determine_routing(classification)
        
        print(f"Primary Category: {classification['routing_decision']['primary_category']}")
        print(f"Confidence: {classification['confidence']:.3f}")
        print(f"Assigned Agents: {routing['assigned_agents']}")
        print(f"Routing Logic: {routing['routing_logic']}")
        print(f"Estimated Processing Time: {routing.get('estimated_processing_time', 'N/A')}s")

async def test_api_endpoints():
    """Test the API endpoints"""
    print("\n🌐 Testing SEEKER API Endpoints...")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test orchestration endpoint with sample requests
    for i, test_case in enumerate(TEST_CASES[:3]):  # Test first 3 cases
        print(f"\n📋 API Test {i+1}: {test_case['name']}")
        
        payload = {
            "user_id": f"test_user_{i+1}",
            "input_text": test_case['input_text']
        }
        
        try:
            response = requests.post(
                f"{base_url}/api/v1/orchestration/process-request",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 202:
                result = response.json()
                print(f"✅ Request accepted: {result['request_id']}")
                print(f"   Status: {result['status']}")
                print(f"   Primary Category: {result['routing_decision']['primary_category']}")
                print(f"   Assigned Agents: {result['routing_decision']['assigned_agents']}")
                print(f"   Estimated Time: {result['estimated_response_time']}")
                
                # Test status endpoint
                await asyncio.sleep(1)  # Wait a bit for processing
                status_response = requests.get(f"{base_url}/api/v1/orchestration/status/{result['request_id']}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"   Status Check: {status_data['status']}")
                else:
                    print(f"   Status Check: Failed ({status_response.status_code})")
                    
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ API test error: {e}")

def test_web_interface():
    """Test the web interface"""
    print("\n🌐 Testing SEEKER Web Interface...")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:8000")
        if response.status_code == 200:
            print("✅ Web interface accessible")
            if "SEEKER AI" in response.text:
                print("✅ Web interface content loaded correctly")
            else:
                print("❌ Web interface content not found")
        else:
            print(f"❌ Web interface failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Web interface error: {e}")

async def main():
    """Run all tests"""
    print("🚀 SEEKER AI Orchestration System - Enhanced Testing")
    print("=" * 80)
    print(f"Test started at: {datetime.now()}")
    
    # Test classification engine
    test_classification_engine()
    
    # Test agent router
    await test_agent_router()
    
    # Test API endpoints
    await test_api_endpoints()
    
    # Test web interface
    test_web_interface()
    
    print("\n" + "=" * 80)
    print("🎯 SEEKER Testing Complete!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main()) 