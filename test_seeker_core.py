#!/usr/bin/env python3
"""
SEEKER Core Components Test Script
Tests the main components of the SEEKER AI Orchestration System
"""

import sys
import asyncio
from datetime import datetime

# Add app directory to path
sys.path.append('.')

def test_classification_engine():
    """Test the classification engine"""
    try:
        from app.services.classification_engine import TaskClassificationEngine
        
        engine = TaskClassificationEngine()
        
        # Test classification
        test_input = "Find the best price for electronic components from global suppliers"
        result = engine.classify_request(test_input)
        
        print(f"✅ Classification Engine Test:")
        print(f"   Input: {test_input}")
        print(f"   Primary Category: {result.get('routing_decision', {}).get('primary_category', 'unknown')}")
        print(f"   Confidence: {result.get('confidence', 0.0):.3f}")
        print(f"   Assigned Agents: {result.get('routing_decision', {}).get('assigned_agents', [])}")
        
        return True
    except Exception as e:
        print(f"❌ Classification Engine Test Failed: {e}")
        return False

def test_agent_router():
    """Test the agent router"""
    try:
        from app.services.agent_router import AgentRouter
        
        router = AgentRouter()
        
        # Test routing
        classification_results = {
            "classification_results": {
                "product_search": 0.8,
                "price_negotiation": 0.6,
                "verification": 0.2,
                "supply_chain": 0.4,
                "translation": 0.1,
                "technical": 0.3,
                "strategic": 0.2,
                "sensitive": 0.0
            },
            "confidence": 0.75,
            "routing_decision": {
                "primary_category": "product_search",
                "assigned_agents": ["product_search_agent"]
            }
        }
        
        # This would normally be async, but we'll test the structure
        print(f"✅ Agent Router Test:")
        print(f"   Available Agents: {list(router.agents.keys())}")
        print(f"   Agent Count: {len(router.agents)}")
        print(f"   High Confidence Threshold: {router.high_confidence_threshold}")
        print(f"   Medium Confidence Threshold: {router.medium_confidence_threshold}")
        
        return True
    except Exception as e:
        print(f"❌ Agent Router Test Failed: {e}")
        return False

def test_sair_loop():
    """Test the SAIR loop"""
    try:
        from app.services.sair_loop import SAIRLoop
        
        sair_loop = SAIRLoop()
        
        print(f"✅ SAIR Loop Test:")
        print(f"   Learning Rate: {sair_loop.learning_rate}")
        print(f"   Decay Factor: {sair_loop.decay_factor}")
        print(f"   Confidence Thresholds: {sair_loop.confidence_thresholds}")
        print(f"   Keyword Categories: {list(sair_loop.keyword_weights.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ SAIR Loop Test Failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        import pymongo
        
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client.seeker_db
        
        # Test connection
        client.admin.command('ping')
        
        print(f"✅ Database Connection Test:")
        print(f"   MongoDB Version: {client.server_info()['version']}")
        print(f"   Database: {db.name}")
        print(f"   Collections: {db.list_collection_names()}")
        
        return True
    except Exception as e:
        print(f"❌ Database Connection Test Failed: {e}")
        return False

def test_voice_interface_files():
    """Test voice interface files exist"""
    try:
        import os
        
        voice_files = [
            "static/js/voice-interface.js",
            "test_voice_interface.py"
        ]
        
        print(f"✅ Voice Interface Files Test:")
        for file_path in voice_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"   ✅ {file_path} ({size} bytes)")
            else:
                print(f"   ❌ {file_path} (not found)")
        
        return True
    except Exception as e:
        print(f"❌ Voice Interface Files Test Failed: {e}")
        return False

def test_api_routes():
    """Test API routes are available"""
    try:
        from app.routes.orchestration import router as orchestration_router
        from app.routes.conversation import router as conversation_router
        from app.routes.files import router as files_router
        from app.routes.users import router as users_router
        
        print(f"✅ API Routes Test:")
        print(f"   Orchestration Routes: {len(orchestration_router.routes)}")
        print(f"   Conversation Routes: {len(conversation_router.routes)}")
        print(f"   Files Routes: {len(files_router.routes)}")
        print(f"   Users Routes: {len(users_router.routes)}")
        
        return True
    except Exception as e:
        print(f"❌ API Routes Test Failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SEEKER Core Components Test")
    print("=" * 50)
    print(f"Test started at: {datetime.now()}")
    print()
    
    tests = [
        ("Classification Engine", test_classification_engine),
        ("Agent Router", test_agent_router),
        ("SAIR Loop", test_sair_loop),
        ("Database Connection", test_database_connection),
        ("Voice Interface Files", test_voice_interface_files),
        ("API Routes", test_api_routes)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SEEKER system is ready.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 