#!/usr/bin/env python3
"""
Test script for SEEKER API endpoints
"""

import requests
import json

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 Testing SEEKER API Endpoints")
    print("=" * 50)
    
    # Test 1: Health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Database: {data.get('services', {}).get('database')}")
            print("   ✅ Health endpoint working")
        else:
            print("   ❌ Health endpoint failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Orchestration endpoint
    print("2. Testing orchestration endpoint...")
    try:
        test_data = {
            "user_id": "test_user",
            "input_text": "Find electronic components for prototyping"
        }
        
        response = requests.post(
            f"{base_url}/api/v1/orchestration/process-request",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 202]:
            data = response.json()
            print(f"   Request ID: {data.get('request_id')}")
            print(f"   Primary Category: {data.get('routing_decision', {}).get('primary_category')}")
            print(f"   Confidence: {data.get('routing_decision', {}).get('confidence', 0)}")
            print("   ✅ Orchestration endpoint working")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: System status
    print("3. Testing system status...")
    try:
        response = requests.get(f"{base_url}/status")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   System: {data.get('system')}")
            print(f"   Version: {data.get('version')}")
            print("   ✅ System status working")
        else:
            print("   ❌ System status failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("🎉 API testing completed!")

if __name__ == "__main__":
    test_api() 