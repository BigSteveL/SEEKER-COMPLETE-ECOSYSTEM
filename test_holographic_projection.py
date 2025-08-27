#!/usr/bin/env python3
"""
SEEKER Holographic Projection System Test Suite
Tests for real-time 3D holographic displays for business presentations
"""

import asyncio
import json
import requests
import time
from typing import Dict, List

# Test configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1/holographic"

class HolographicProjectionTester:
    """Test suite for SEEKER Holographic Projection System"""
    
    def __init__(self):
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": time.time()
        })
    
    def test_server_health(self):
        """Test if the server is running"""
        try:
            response = self.session.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                self.log_test("Server Health Check", True, "Server is running")
                return True
            else:
                self.log_test("Server Health Check", False, f"Server returned {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Server Health Check", False, f"Connection error: {e}")
            return False
    
    def test_get_devices(self):
        """Test getting holographic devices"""
        try:
            response = self.session.get(f"{API_BASE}/devices")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "devices" in data.get("data", {}):
                    devices = data["data"]["devices"]
                    self.log_test("Get Devices", True, f"Found {len(devices)} devices")
                    return devices
                else:
                    self.log_test("Get Devices", False, "Invalid response format")
                    return None
            else:
                self.log_test("Get Devices", False, f"HTTP {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Get Devices", False, f"Error: {e}")
            return None
    
    def test_get_device_status(self, device_id: str):
        """Test getting specific device status"""
        try:
            response = self.session.get(f"{API_BASE}/devices/{device_id}")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "device" in data.get("data", {}):
                    device = data["data"]["device"]
                    self.log_test("Get Device Status", True, f"Device {device_id}: {device.get('name', 'Unknown')}")
                    return device
                else:
                    self.log_test("Get Device Status", False, "Invalid response format")
                    return None
            else:
                self.log_test("Get Device Status", False, f"HTTP {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Get Device Status", False, f"Error: {e}")
            return None
    
    def test_create_projection(self, device_id: str):
        """Test creating a holographic projection"""
        try:
            projection_data = {
                "device_id": device_id,
                "projection_type": "static_3d",
                "model_url": "https://example.com/test_model.gltf",
                "position": [0.0, 0.0, 0.0],
                "rotation": [0.0, 0.0, 0.0],
                "scale": 1.0,
                "is_interactive": False
            }
            
            response = self.session.post(
                f"{API_BASE}/projections",
                json=projection_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "projection_id" in data.get("data", {}):
                    projection_id = data["data"]["projection_id"]
                    self.log_test("Create Projection", True, f"Created projection: {projection_id}")
                    return projection_id
                else:
                    self.log_test("Create Projection", False, "Invalid response format")
                    return None
            else:
                self.log_test("Create Projection", False, f"HTTP {response.status_code}: {response.text}")
                return None
        except Exception as e:
            self.log_test("Create Projection", False, f"Error: {e}")
            return None
    
    def test_get_projections(self):
        """Test getting active projections"""
        try:
            response = self.session.get(f"{API_BASE}/projections")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "projections" in data.get("data", {}):
                    projections = data["data"]["projections"]
                    self.log_test("Get Projections", True, f"Found {len(projections)} active projections")
                    return projections
                else:
                    self.log_test("Get Projections", False, "Invalid response format")
                    return None
            else:
                self.log_test("Get Projections", False, f"HTTP {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Get Projections", False, f"Error: {e}")
            return None
    
    def test_update_projection(self, projection_id: str):
        """Test updating a projection"""
        try:
            update_data = {
                "position": [1.0, 2.0, 3.0],
                "rotation": [45.0, 90.0, 0.0],
                "scale": 1.5
            }
            
            response = self.session.put(
                f"{API_BASE}/projections/{projection_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Update Projection", True, f"Updated projection: {projection_id}")
                    return True
                else:
                    self.log_test("Update Projection", False, "Invalid response format")
                    return False
            else:
                self.log_test("Update Projection", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Update Projection", False, f"Error: {e}")
            return False
    
    def test_start_streaming(self, projection_id: str):
        """Test starting real-time streaming"""
        try:
            stream_config = {
                "quality": "presentation",
                "latency_target": 16,
                "enable_interaction": True
            }
            
            response = self.session.post(
                f"{API_BASE}/projections/{projection_id}/streaming",
                json=stream_config,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Start Streaming", True, f"Started streaming for projection: {projection_id}")
                    return True
                else:
                    self.log_test("Start Streaming", False, "Invalid response format")
                    return False
            else:
                self.log_test("Start Streaming", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Start Streaming", False, f"Error: {e}")
            return False
    
    def test_enable_collaborative(self, projection_id: str):
        """Test enabling collaborative mode"""
        try:
            participants = ["user_1", "user_2", "user_3"]
            
            response = self.session.post(
                f"{API_BASE}/projections/{projection_id}/collaborative",
                json=participants,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Enable Collaborative", True, f"Enabled collaborative mode for projection: {projection_id}")
                    return True
                else:
                    self.log_test("Enable Collaborative", False, "Invalid response format")
                    return False
            else:
                self.log_test("Enable Collaborative", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Enable Collaborative", False, f"Error: {e}")
            return False
    
    def test_get_business_scenarios(self):
        """Test getting business scenarios"""
        try:
            response = self.session.get(f"{API_BASE}/business-scenarios")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "scenarios" in data.get("data", {}):
                    scenarios = data["data"]["scenarios"]
                    self.log_test("Get Business Scenarios", True, f"Found {len(scenarios)} business scenarios")
                    return scenarios
                else:
                    self.log_test("Get Business Scenarios", False, "Invalid response format")
                    return None
            else:
                self.log_test("Get Business Scenarios", False, f"HTTP {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Get Business Scenarios", False, f"Error: {e}")
            return None
    
    def test_activate_scenario(self, scenario_id: str):
        """Test activating a business scenario"""
        try:
            scenario_config = {
                "elements": [
                    {
                        "device_id": "holo_proj_001",
                        "type": "interactive_3d",
                        "model_url": f"/models/scenario_{scenario_id}.gltf",
                        "position": [0.0, 0.0, 0.0],
                        "rotation": [0.0, 0.0, 0.0],
                        "scale": 1.0,
                        "is_interactive": True
                    }
                ]
            }
            
            response = self.session.post(
                f"{API_BASE}/scenarios/{scenario_id}/activate",
                json=scenario_config,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "projection_ids" in data.get("data", {}):
                    projection_ids = data["data"]["projection_ids"]
                    self.log_test("Activate Scenario", True, f"Activated scenario {scenario_id} with {len(projection_ids)} projections")
                    return projection_ids
                else:
                    self.log_test("Activate Scenario", False, "Invalid response format")
                    return None
            else:
                self.log_test("Activate Scenario", False, f"HTTP {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Activate Scenario", False, f"Error: {e}")
            return None
    
    def test_create_business_presentation(self):
        """Test creating a business presentation"""
        try:
            presentation_data = {
                "title": "Test Business Presentation",
                "slides": [
                    {"title": "Slide 1", "content": "Introduction"},
                    {"title": "Slide 2", "content": "Main Content"}
                ],
                "holographic_elements": [
                    {
                        "device_id": "holo_proj_001",
                        "type": "static_3d",
                        "model_url": "https://example.com/presentation_model.gltf",
                        "position": [0.0, 0.0, 0.0],
                        "rotation": [0.0, 0.0, 0.0],
                        "scale": 1.0,
                        "is_interactive": False
                    }
                ]
            }
            
            response = self.session.post(
                f"{API_BASE}/business-presentation",
                json=presentation_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "projection_ids" in data.get("data", {}):
                    projection_ids = data["data"]["projection_ids"]
                    self.log_test("Create Business Presentation", True, f"Created presentation with {len(projection_ids)} projections")
                    return projection_ids
                else:
                    self.log_test("Create Business Presentation", False, "Invalid response format")
                    return None
            else:
                self.log_test("Create Business Presentation", False, f"HTTP {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Create Business Presentation", False, f"Error: {e}")
            return None
    
    def test_remove_projection(self, projection_id: str):
        """Test removing a projection"""
        try:
            response = self.session.delete(f"{API_BASE}/projections/{projection_id}")
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Remove Projection", True, f"Removed projection: {projection_id}")
                    return True
                else:
                    self.log_test("Remove Projection", False, "Invalid response format")
                    return False
            else:
                self.log_test("Remove Projection", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Remove Projection", False, f"Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all holographic projection tests"""
        print("🔮 SEEKER Holographic Projection System Test Suite")
        print("=" * 60)
        
        # Test server health
        if not self.test_server_health():
            print("❌ Server not available. Please start the SEEKER server first.")
            return
        
        print("\n📱 Testing Device Management...")
        devices = self.test_get_devices()
        if devices:
            # Test device status for first device
            if devices:
                first_device = devices[0]
                self.test_get_device_status(first_device["device_id"])
        
        print("\n🎬 Testing Projection Management...")
        # Create a projection
        if devices:
            projection_id = self.test_create_projection(devices[0]["device_id"])
            if projection_id:
                # Test projection operations
                self.test_get_projections()
                self.test_update_projection(projection_id)
                self.test_start_streaming(projection_id)
                self.test_enable_collaborative(projection_id)
        
        print("\n💼 Testing Business Scenarios...")
        scenarios = self.test_get_business_scenarios()
        if scenarios:
            # Test activating first scenario
            first_scenario = scenarios[0]
            self.test_activate_scenario(first_scenario["id"])
        
        print("\n📊 Testing Business Presentations...")
        self.test_create_business_presentation()
        
        print("\n🧹 Cleanup...")
        # Clean up test projections
        projections = self.test_get_projections()
        if projections:
            for projection in projections[:3]:  # Remove first 3 projections
                self.test_remove_projection(projection["projection_id"])
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        if passed_tests == total_tests:
            print("\n🎉 All tests passed! SEEKER Holographic Projection System is working correctly.")
        else:
            print(f"\n⚠️  {failed_tests} test(s) failed. Please check the implementation.")

def main():
    """Main test runner"""
    tester = HolographicProjectionTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 