#!/usr/bin/env python3
"""
Quick test script to verify SEEKER orchestration endpoints are working.
Run this after starting the server with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, description=""):
    """Test an endpoint and return the result."""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
            
        if response.status_code == 200 or response.status_code == 202:
            print(f"✅ {method} {endpoint} - {response.status_code} - {description}")
            return True
        else:
            print(f"❌ {method} {endpoint} - {response.status_code} - {description}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint} - Connection Error - {description}")
        print("   Make sure the server is running: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {str(e)} - {description}")
        return False

def main():
    """Test all orchestration endpoints."""
    print("🚀 Testing SEEKER Orchestration Endpoints")
    print("=" * 50)
    
    # Test basic system endpoints
    print("\n📋 Testing System Endpoints:")
    test_endpoint("GET", "/", description="Root endpoint")
    test_endpoint("GET", "/health", description="Health check")
    test_endpoint("GET", "/status", description="System status")
    test_endpoint("GET", "/docs", description="API documentation")
    
    # Test orchestration endpoints
    print("\n🎯 Testing Orchestration Endpoints:")
    test_endpoint("GET", "/api/v1/orchestration/status", description="Orchestration system status")
    test_endpoint("GET", "/api/v1/orchestration/performance-metrics", description="Performance metrics")
    
    # Test classification endpoint
    print("\n🔍 Testing Classification Endpoint:")
    classify_data = {
        "input_text": "Help me debug this Python code for performance optimization"
    }
    test_endpoint("POST", "/api/v1/orchestration/classify", data=classify_data, description="Text classification")
    
    # Test process request endpoint
    print("\n⚡ Testing Process Request Endpoint:")
    process_data = {
        "input_text": "I need help analyzing this code for performance optimization",
        "user_id": "test_user_123",
        "device_id": "test_device_456",
        "context": {
            "session_id": "test_session_789",
            "user_preferences": {"language": "en", "timezone": "UTC"}
        }
    }
    success = test_endpoint("POST", "/api/v1/orchestration/process-request", data=process_data, description="Process user request")
    
    # If process request was successful, test status endpoint
    if success:
        print("\n📊 Testing Request Status Endpoint:")
        # We need to get a request_id from the process response
        try:
            response = requests.post(f"{BASE_URL}/api/v1/orchestration/process-request", json=process_data, timeout=10)
            if response.status_code == 202:
                result = response.json()
                request_id = result.get("request_id")
                if request_id:
                    test_endpoint("GET", f"/api/v1/orchestration/status/{request_id}", description=f"Request status for {request_id}")
                else:
                    print("❌ Could not get request_id from process response")
            else:
                print("❌ Process request failed, cannot test status endpoint")
        except Exception as e:
            print(f"❌ Error testing status endpoint: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Endpoint testing completed!")
    print("\n📚 Next steps:")
    print("1. Visit http://localhost:8000/docs for interactive API documentation")
    print("2. Run the full test suite: python app/test_seeker.py")
    print("3. Start using the SEEKER orchestration system!")

if __name__ == "__main__":
    main() 