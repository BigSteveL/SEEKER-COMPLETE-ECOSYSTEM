#!/usr/bin/env python3
"""
SEEKER 3D Ecosystem Test Script
Tests the complete 3D integration system
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime

class SEEKER3DEcosystemTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_health_check(self):
        """Test system health"""
        print("🏥 Testing system health...")
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Health check passed: {data['status']}")
                    return True
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    async def test_3d_file_service(self):
        """Test 3D file processing service"""
        print("\n📁 Testing 3D file service...")
        try:
            # Test getting models
            async with self.session.get(f"{self.base_url}/api/v1/3d-files/models") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ 3D file service working: {len(data.get('models', []))} models found")
                    return True
                else:
                    print(f"❌ 3D file service failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ 3D file service error: {e}")
            return False
    
    async def test_3d_printer_service(self):
        """Test 3D printer service"""
        print("\n🖨️ Testing 3D printer service...")
        try:
            # Test printer discovery
            async with self.session.get(f"{self.base_url}/api/v1/3d-printer/discover") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ 3D printer service working: {len(data.get('printers', []))} printers discovered")
                    return True
                else:
                    print(f"❌ 3D printer service failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ 3D printer service error: {e}")
            return False
    
    async def test_manufacturing_service(self):
        """Test manufacturing service"""
        print("\n🏭 Testing manufacturing service...")
        try:
            # Test manufacturing connections
            async with self.session.get(f"{self.base_url}/api/v1/manufacturing/connections") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Manufacturing service working: {len(data.get('connections', []))} connections available")
                    return True
                else:
                    print(f"❌ Manufacturing service failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Manufacturing service error: {e}")
            return False
    
    async def test_file_upload(self):
        """Test file upload functionality"""
        print("\n📤 Testing file upload...")
        try:
            # Create a simple test STL file content
            stl_content = """solid test
facet normal 0 0 1
  outer loop
    vertex 0 0 0
    vertex 1 0 0
    vertex 0 1 0
  endloop
endfacet
endsolid test"""
            
            # Create form data
            data = aiohttp.FormData()
            data.add_field('file', 
                          stl_content.encode(), 
                          filename='test.stl',
                          content_type='application/octet-stream')
            
            async with self.session.post(f"{self.base_url}/api/v1/3d-files/upload", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ File upload successful: {result.get('model_id')}")
                    return result.get('model_id')
                else:
                    print(f"❌ File upload failed: {response.status}")
                    return None
        except Exception as e:
            print(f"❌ File upload error: {e}")
            return None
    
    async def test_print_preview(self, model_id):
        """Test print preview generation"""
        if not model_id:
            print("❌ No model ID for print preview test")
            return False
            
        print(f"\n🖨️ Testing print preview for model {model_id}...")
        try:
            preview_data = {
                "layer_height": 0.2,
                "infill_density": 20.0,
                "print_speed": 60.0,
                "support_enabled": False,
                "bed_temperature": 60.0,
                "extruder_temperature": 200.0
            }
            
            async with self.session.post(
                f"{self.base_url}/api/v1/3d-files/models/{model_id}/preview",
                json=preview_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Print preview generated: {result.get('print_time_hours', 0):.1f} hours")
                    return True
                else:
                    print(f"❌ Print preview failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Print preview error: {e}")
            return False
    
    async def test_system_status(self):
        """Test system status endpoint"""
        print("\n📊 Testing system status...")
        try:
            async with self.session.get(f"{self.base_url}/status") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ System status: {data.get('status')}")
                    print(f"   Features: {len(data.get('features', {}))} active")
                    return True
                else:
                    print(f"❌ System status failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ System status error: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting SEEKER 3D Ecosystem Tests")
        print("=" * 50)
        
        results = {
            'health_check': await self.test_health_check(),
            '3d_file_service': await self.test_3d_file_service(),
            '3d_printer_service': await self.test_3d_printer_service(),
            'manufacturing_service': await self.test_manufacturing_service(),
            'system_status': await self.test_system_status()
        }
        
        # Test file upload and print preview
        model_id = await self.test_file_upload()
        if model_id:
            results['file_upload'] = True
            results['print_preview'] = await self.test_print_preview(model_id)
        else:
            results['file_upload'] = False
            results['print_preview'] = False
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 Test Results Summary:")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
            if result:
                passed += 1
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! SEEKER 3D Ecosystem is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the server logs for details.")
        
        return results

async def main():
    """Main test function"""
    print("SEEKER 3D Ecosystem Test Suite")
    print("Testing complete 3D integration system")
    print()
    
    async with SEEKER3DEcosystemTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 