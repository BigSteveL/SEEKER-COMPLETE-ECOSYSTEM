#!/usr/bin/env python3
"""
SEEKER AI Orchestration System - Test Script

This script demonstrates the SEEKER prototype's multi-intelligence orchestration
by testing different types of requests and showing classification and routing responses.

Usage:
    1. Start the FastAPI server: uvicorn app.main:app --reload
    2. Run this test script: python app/test_seeker.py
"""

import requests
import json
import time
import sys
from typing import Dict, Any
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1/orchestration"

class SeekerTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def print_header(self, title: str):
        """Print a formatted header."""
        print("\n" + "="*60)
        print(f"🧪 {title}")
        print("="*60)
    
    def print_response(self, response: requests.Response, test_name: str):
        """Print formatted response."""
        print(f"\n📤 Response for: {test_name}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.3f}s")
        
        if response.status_code == 200 or response.status_code == 202:
            data = response.json()
            print("\n🎯 Classification Results:")
            classification = data.get('classification_results', {})
            for category, score in classification.items():
                if isinstance(score, (int, float)):
                    print(f"   {category.capitalize()}: {score:.3f}")
            
            print(f"\n🎯 Overall Confidence: {data.get('confidence', 0):.3f}")
            print(f"🎯 Estimated Response Time: {data.get('estimated_response_time', 'Unknown')}")
            
            routing = data.get('routing_decision', {})
            print(f"\n🚀 Routing Decision:")
            print(f"   Assigned Agents: {routing.get('assigned_agents', [])}")
            print(f"   Routing Logic: {routing.get('routing_logic', 'Unknown')}")
            print(f"   Primary Category: {routing.get('primary_category', 'Unknown')}")
            
            print(f"\n🆔 Request ID: {data.get('request_id', 'Unknown')}")
            print(f"📝 Message: {data.get('message', 'No message')}")
            
        else:
            print(f"❌ Error: {response.text}")
    
    def test_health_check(self):
        """Test the health check endpoint."""
        self.print_header("Health Check Test")
        
        try:
            response = self.session.get(f"{BASE_URL}/health")
            print(f"Health Check Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"System Status: {data.get('status', 'Unknown')}")
                print(f"Environment: {data.get('environment', 'Unknown')}")
                print("✅ Health check passed!")
            else:
                print("❌ Health check failed!")
        except Exception as e:
            print(f"❌ Health check error: {e}")
    
    def test_system_status(self):
        """Test the system status endpoint."""
        self.print_header("System Status Test")
        
        try:
            response = self.session.get(f"{BASE_URL}/status")
            print(f"System Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"System Status: {data.get('status', 'Unknown')}")
                print(f"Environment: {data.get('environment', 'Unknown')}")
                print(f"Version: {data.get('version', 'Unknown')}")
                
                stats = data.get('database_stats', {})
                print(f"\n📊 Database Statistics:")
                print(f"   Total Users: {stats.get('total_users', 0)}")
                print(f"   Total Requests: {stats.get('total_requests', 0)}")
                print(f"   Total Responses: {stats.get('total_responses', 0)}")
                print(f"   Total SAIR Loops: {stats.get('total_sair_loops', 0)}")
                
                print("✅ System status check passed!")
            else:
                print("❌ System status check failed!")
        except Exception as e:
            print(f"❌ System status error: {e}")
    
    def test_technical_request(self):
        """Test a technical request."""
        self.print_header("Technical Request Test")
        
        test_data = {
            "input_text": "Help me debug this Python code error: 'IndexError: list index out of range' in my data processing function",
            "user_id": "test_user_001",
            "device_id": "dev_python_laptop",
            "context": {
                "session_id": "sess_tech_001",
                "user_preferences": {"language": "en", "expertise_level": "intermediate"},
                "previous_requests": []
            }
        }
        
        try:
            response = self.session.post(f"{API_BASE}/process-request", json=test_data)
            self.print_response(response, "Technical Debugging Request")
            
            # Expected behavior:
            # - High technical classification score
            # - Assigned to technical_ai_agent
            # - High confidence routing
            
        except Exception as e:
            print(f"❌ Technical request error: {e}")
    
    def test_strategic_request(self):
        """Test a strategic request."""
        self.print_header("Strategic Request Test")
        
        test_data = {
            "input_text": "Create a comprehensive business plan for expanding our software company to European markets, including market analysis and competitive positioning",
            "user_id": "test_user_002",
            "device_id": "dev_strategy_tablet",
            "context": {
                "session_id": "sess_strategy_001",
                "user_preferences": {"language": "en", "business_focus": "expansion"},
                "previous_requests": []
            }
        }
        
        try:
            response = self.session.post(f"{API_BASE}/process-request", json=test_data)
            self.print_response(response, "Strategic Business Planning Request")
            
            # Expected behavior:
            # - High strategic classification score
            # - Assigned to strategic_ai_agent
            # - Business-focused routing
            
        except Exception as e:
            print(f"❌ Strategic request error: {e}")
    
    def test_sensitive_request(self):
        """Test a sensitive request."""
        self.print_header("Sensitive Request Test")
        
        test_data = {
            "input_text": "I need to store my personal financial information, medical records, and legal documents securely with encryption",
            "user_id": "test_user_003",
            "device_id": "dev_secure_phone",
            "context": {
                "session_id": "sess_sensitive_001",
                "user_preferences": {"language": "en", "security_level": "high"},
                "previous_requests": []
            }
        }
        
        try:
            response = self.session.post(f"{API_BASE}/process-request", json=test_data)
            self.print_response(response, "Sensitive Data Storage Request")
            
            # Expected behavior:
            # - High sensitive classification score
            # - Assigned to local_ai_system (for security)
            # - Secure processing routing
            
        except Exception as e:
            print(f"❌ Sensitive request error: {e}")
    
    def test_mixed_request(self):
        """Test a mixed request with multiple categories."""
        self.print_header("Mixed Request Test")
        
        test_data = {
            "input_text": "Analyze our company's technical architecture for scalability issues and provide strategic recommendations for market expansion in Asia",
            "user_id": "test_user_004",
            "device_id": "dev_executive_laptop",
            "context": {
                "session_id": "sess_mixed_001",
                "user_preferences": {"language": "en", "analysis_depth": "comprehensive"},
                "previous_requests": []
            }
        }
        
        try:
            response = self.session.post(f"{API_BASE}/process-request", json=test_data)
            self.print_response(response, "Mixed Technical & Strategic Analysis Request")
            
            # Expected behavior:
            # - Medium scores for both technical and strategic
            # - Dual-AI processing (technical_ai_agent + strategic_ai_agent)
            # - Comprehensive analysis routing
            
        except Exception as e:
            print(f"❌ Mixed request error: {e}")
    
    def test_low_confidence_request(self):
        """Test a low confidence request."""
        self.print_header("Low Confidence Request Test")
        
        test_data = {
            "input_text": "What should I do about the weather today and my lunch plans?",
            "user_id": "test_user_005",
            "device_id": "dev_general_phone",
            "context": {
                "session_id": "sess_general_001",
                "user_preferences": {"language": "en"},
                "previous_requests": []
            }
        }
        
        try:
            response = self.session.post(f"{API_BASE}/process-request", json=test_data)
            self.print_response(response, "Low Confidence General Request")
            
            # Expected behavior:
            # - Low classification scores across categories
            # - Human escalation routing
            # - Low confidence handling
            
        except Exception as e:
            print(f"❌ Low confidence request error: {e}")
    
    def test_request_status(self, request_id: str):
        """Test checking request status."""
        self.print_header(f"Request Status Test for {request_id}")
        
        try:
            response = self.session.get(f"{API_BASE}/status/{request_id}")
            print(f"Status Check: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Request Status: {data.get('status', 'Unknown')}")
                print(f"Response Count: {data.get('response_count', 0)}")
                print(f"Total Processing Time: {data.get('total_processing_time', 0):.3f}s")
                print(f"Average Confidence: {data.get('average_confidence', 0):.3f}")
                
                # Show agent responses
                responses = data.get('agent_responses', [])
                if responses:
                    print(f"\n🤖 Agent Responses:")
                    for i, resp in enumerate(responses, 1):
                        print(f"   {i}. {resp.get('agent_id', 'Unknown')} - Confidence: {resp.get('confidence', 0):.3f}")
                        print(f"      Content: {resp.get('response_content', '')[:100]}...")
                
                print("✅ Status check completed!")
            else:
                print(f"❌ Status check failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Status check error: {e}")
    
    def test_performance_metrics(self):
        """Test performance metrics endpoint."""
        self.print_header("Performance Metrics Test")
        
        try:
            response = self.session.get(f"{API_BASE}/performance-metrics")
            print(f"Performance Metrics: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("📊 Performance Metrics Retrieved Successfully!")
                print(f"Router Analytics: {len(data.get('router_analytics', {}))} metrics")
                print(f"Learning Summary: {len(data.get('learning_summary', {}))} items")
                print(f"Database Stats: {len(data.get('database_stats', {}))} collections")
                
            else:
                print(f"❌ Performance metrics failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Performance metrics error: {e}")
    
    def run_all_tests(self):
        """Run all test cases."""
        print("🚀 SEEKER AI Orchestration System - Test Suite")
        print("="*60)
        print("This test suite demonstrates SEEKER's multi-intelligence orchestration")
        print("by testing different types of requests and showing classification")
        print("and routing responses.")
        print("\n📋 Test Cases:")
        print("1. Health Check")
        print("2. System Status")
        print("3. Technical Request (Debugging)")
        print("4. Strategic Request (Business Planning)")
        print("5. Sensitive Request (Secure Data)")
        print("6. Mixed Request (Technical + Strategic)")
        print("7. Low Confidence Request (General)")
        print("8. Performance Metrics")
        print("\n" + "="*60)
        
        # Store request IDs for status checking
        request_ids = []
        
        # Run basic system tests
        self.test_health_check()
        self.test_system_status()
        
        # Run request tests
        self.test_technical_request()
        self.test_strategic_request()
        self.test_sensitive_request()
        self.test_mixed_request()
        self.test_low_confidence_request()
        
        # Run performance test
        self.test_performance_metrics()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("\n📝 Expected SEEKER Intelligence Behavior:")
        print("• Technical requests → technical_ai_agent (high confidence)")
        print("• Strategic requests → strategic_ai_agent (high confidence)")
        print("• Sensitive requests → local_ai_system (any confidence)")
        print("• Mixed requests → dual-AI processing (medium confidence)")
        print("• Low confidence → human escalation")
        print("\n🎯 SEEKER demonstrates intelligent routing based on:")
        print("• Content classification (technical/strategic/sensitive)")
        print("• Confidence scoring")
        print("• SAIR loop learning")
        print("• Performance optimization")
        print("="*60)

def main():
    """Main function to run the test suite."""
    print("🔧 SEEKER Test Suite Setup")
    print("="*40)
    print("Before running tests, ensure:")
    print("1. FastAPI server is running: uvicorn app.main:app --reload")
    print("2. MongoDB is running and accessible")
    print("3. All dependencies are installed")
    print("\nTo start the server:")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("\n" + "="*40)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible!")
        else:
            print("⚠️  Server responded but health check failed")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the FastAPI server first:")
        print("   uvicorn app.main:app --reload")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        sys.exit(1)
    
    # Run tests
    tester = SeekerTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 