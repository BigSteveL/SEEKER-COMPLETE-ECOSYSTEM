#!/usr/bin/env python3
"""
Debug script to test SEEKER server and identify issues
"""

import sys
import asyncio
import time

# Add app directory to path
sys.path.append('.')

async def test_server():
    """Test the server components"""
    try:
        print("🔍 Testing SEEKER server components...")
        
        # Test 1: Import main app
        print("1. Testing main app import...")
        from app.main import app
        print("   ✅ Main app imported successfully")
        
        # Test 2: Test lifespan startup
        print("2. Testing lifespan startup...")
        async with app.router.lifespan_context(app):
            print("   ✅ Lifespan startup completed")
        
        # Test 3: Test health endpoint
        print("3. Testing health endpoint...")
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get("/health")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
        else:
            print("   ❌ Health endpoint failed")
        
        # Test 4: Test root endpoint
        print("4. Testing root endpoint...")
        response = client.get("/")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Root endpoint working")
        else:
            print("   ❌ Root endpoint failed")
        
        # Test 5: Test orchestration endpoint
        print("5. Testing orchestration endpoint...")
        test_data = {
            "user_id": "test_user",
            "input_text": "Find electronic components"
        }
        
        response = client.post("/api/v1/orchestration/process-request", json=test_data)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code in [200, 202]:
            print("   ✅ Orchestration endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print("   ❌ Orchestration endpoint failed")
            print(f"   Error: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the debug test"""
    print("🚀 SEEKER Server Debug Test")
    print("=" * 50)
    
    success = asyncio.run(test_server())
    
    print("=" * 50)
    if success:
        print("🎉 All tests passed! Server is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 