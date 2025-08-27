#!/usr/bin/env python3
"""
Test script for SEEKER Conversation Endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_conversation_endpoints():
    """Test all conversation endpoints"""
    print("🚀 Testing SEEKER Conversation Endpoints")
    print("=" * 50)
    
    # Test 1: Create a new conversation
    print("\n📝 Testing Conversation Creation:")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/conversation/conversations/?user_id=test_user_123")
        if response.status_code == 200:
            conversation_data = response.json()
            session_id = conversation_data["session_id"]
            print(f"✅ POST /api/v1/conversation/conversations/ - 200 - Created conversation: {session_id}")
        else:
            print(f"❌ POST /api/v1/conversation/conversations/ - {response.status_code} - Failed")
            return
    except Exception as e:
        print(f"❌ Error creating conversation: {e}")
        return
    
    # Test 2: Get the conversation
    print("\n📖 Testing Get Conversation:")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/conversation/conversations/{session_id}")
        if response.status_code == 200:
            print(f"✅ GET /api/v1/conversation/conversations/{session_id} - 200 - Retrieved conversation")
        else:
            print(f"❌ GET /api/v1/conversation/conversations/{session_id} - {response.status_code} - Failed")
    except Exception as e:
        print(f"❌ Error getting conversation: {e}")
    
    # Test 3: Add a message to the conversation
    print("\n💬 Testing Add Message:")
    try:
        message_data = {
            "user_input": "Hello, how are you?",
            "system_response": "I am doing well, thank you for asking!"
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/conversation/conversations/{session_id}/messages/",
            json=message_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print(f"✅ POST /api/v1/conversation/conversations/{session_id}/messages/ - 200 - Message added")
        else:
            print(f"❌ POST /api/v1/conversation/conversations/{session_id}/messages/ - {response.status_code} - Failed")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error adding message: {e}")
    
    # Test 4: Get the conversation again to see the message
    print("\n📖 Testing Get Conversation (with message):")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/conversation/conversations/{session_id}")
        if response.status_code == 200:
            conversation_data = response.json()
            message_count = len(conversation_data.get("messages", []))
            print(f"✅ GET /api/v1/conversation/conversations/{session_id} - 200 - Conversation has {message_count} messages")
        else:
            print(f"❌ GET /api/v1/conversation/conversations/{session_id} - {response.status_code} - Failed")
    except Exception as e:
        print(f"❌ Error getting conversation: {e}")
    
    # Test 5: Test non-existent conversation
    print("\n🔍 Testing Non-existent Conversation:")
    try:
        fake_session_id = "fake-session-id-123"
        response = requests.get(f"{BASE_URL}/api/v1/conversation/conversations/{fake_session_id}")
        if response.status_code == 404:
            print(f"✅ GET /api/v1/conversation/conversations/{fake_session_id} - 404 - Correctly not found")
        else:
            print(f"❌ GET /api/v1/conversation/conversations/{fake_session_id} - {response.status_code} - Expected 404")
    except Exception as e:
        print(f"❌ Error testing non-existent conversation: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Conversation endpoint testing completed!")
    print("\n📚 Next steps:")
    print("1. Visit http://localhost:8000/docs for interactive API documentation")
    print("2. Test the conversation endpoints manually")
    print("3. Integrate conversation system with orchestration!")

if __name__ == "__main__":
    test_conversation_endpoints() 