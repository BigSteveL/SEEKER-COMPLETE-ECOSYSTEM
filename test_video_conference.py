#!/usr/bin/env python3
"""
Test script for SEEKER Video Conferencing System
Tests WebRTC video calling with real-time translation for cross-border negotiations
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any

# Test configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1/video-conference"

class VideoConferenceTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f"   {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    async def test_health_check(self):
        """Test video conference service health"""
        try:
            async with self.session.get(f"{API_BASE}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_test(
                        "Video Conference Health Check",
                        True,
                        f"Active conferences: {data.get('active_conferences', 0)}, Total: {data.get('total_conferences', 0)}"
                    )
                else:
                    self.log_test("Video Conference Health Check", False, f"Status: {response.status}")
        except Exception as e:
            self.log_test("Video Conference Health Check", False, f"Error: {str(e)}")
    
    async def test_create_conference(self):
        """Test conference creation"""
        try:
            conference_data = {
                "title": "SEEKER Price Negotiation Session",
                "description": "Cross-border negotiation with real-time translation",
                "scheduled_start": datetime.now().isoformat(),
                "scheduled_end": (datetime.now() + timedelta(hours=2)).isoformat(),
                "max_participants": 6,
                "languages": ["en-US", "es-ES", "fr-FR"],
                "translation_enabled": True,
                "recording_enabled": False,
                "negotiation_type": "price_negotiation",
                "parties_involved": ["TechCorp Inc", "Global Suppliers Ltd"],
                "estimated_duration": 90
            }
            
            async with self.session.post(
                f"{API_BASE}/conferences/",
                json=conference_data
            ) as response:
                if response.status == 200:
                    conference = await response.json()
                    self.log_test(
                        "Create Conference",
                        True,
                        f"Conference ID: {conference['id']}, Title: {conference['title']}"
                    )
                    return conference['id']
                else:
                    self.log_test("Create Conference", False, f"Status: {response.status}")
                    return None
        except Exception as e:
            self.log_test("Create Conference", False, f"Error: {str(e)}")
            return None
    
    async def test_join_conference(self, conference_id: str):
        """Test participant joining conference"""
        try:
            participant_data = {
                "conference_id": conference_id,
                "user_id": f"test_user_{int(time.time())}",
                "name": "John Negotiator",
                "email": "john@techcorp.com",
                "role": "negotiator",
                "language": "en-US",
                "timezone": "UTC"
            }
            
            async with self.session.post(
                f"{API_BASE}/conferences/{conference_id}/join",
                json=participant_data
            ) as response:
                if response.status == 200:
                    participant = await response.json()
                    self.log_test(
                        "Join Conference",
                        True,
                        f"Participant: {participant['name']}, Role: {participant['role']}"
                    )
                    return participant['id']
                else:
                    self.log_test("Join Conference", False, f"Status: {response.status}")
                    return None
        except Exception as e:
            self.log_test("Join Conference", False, f"Error: {str(e)}")
            return None
    
    async def test_multilingual_join(self, conference_id: str):
        """Test multiple participants joining with different languages"""
        participants = [
            {
                "name": "Maria Compras",
                "role": "buyer",
                "language": "es-ES",
                "email": "maria@techcorp.es"
            },
            {
                "name": "Pierre Fournisseur",
                "role": "seller",
                "language": "fr-FR",
                "email": "pierre@globalsuppliers.fr"
            },
            {
                "name": "AI Mediator",
                "role": "mediator",
                "language": "en-US",
                "email": "ai@seeker.com"
            }
        ]
        
        participant_ids = []
        for i, participant_data in enumerate(participants):
            try:
                join_data = {
                    "conference_id": conference_id,
                    "user_id": f"test_user_{int(time.time())}_{i}",
                    "name": participant_data["name"],
                    "email": participant_data["email"],
                    "role": participant_data["role"],
                    "language": participant_data["language"],
                    "timezone": "UTC"
                }
                
                async with self.session.post(
                    f"{API_BASE}/conferences/{conference_id}/join",
                    json=join_data
                ) as response:
                    if response.status == 200:
                        participant = await response.json()
                        participant_ids.append(participant['id'])
                        self.log_test(
                            f"Join Conference - {participant_data['name']}",
                            True,
                            f"Language: {participant_data['language']}, Role: {participant_data['role']}"
                        )
                    else:
                        self.log_test(f"Join Conference - {participant_data['name']}", False, f"Status: {response.status}")
                        
            except Exception as e:
                self.log_test(f"Join Conference - {participant_data['name']}", False, f"Error: {str(e)}")
        
        return participant_ids
    
    async def test_translation(self, conference_id: str, participant_id: str):
        """Test real-time translation functionality"""
        test_translations = [
            {
                "original_text": "What is your best price for 1000 units?",
                "source_language": "en-US",
                "target_language": "es-ES",
                "expected_keywords": ["precio", "unidades"]
            },
            {
                "original_text": "We can offer a 15% discount for bulk orders",
                "source_language": "en-US",
                "target_language": "fr-FR",
                "expected_keywords": ["remise", "commande"]
            },
            {
                "original_text": "Necesitamos entrega en 30 días",
                "source_language": "es-ES",
                "target_language": "en-US",
                "expected_keywords": ["delivery", "days"]
            }
        ]
        
        for i, translation_test in enumerate(test_translations):
            try:
                translation_request = {
                    "conference_id": conference_id,
                    "participant_id": participant_id,
                    "original_text": translation_test["original_text"],
                    "source_language": translation_test["source_language"],
                    "target_language": translation_test["target_language"],
                    "translation_mode": "simultaneous"
                }
                
                async with self.session.post(
                    f"{API_BASE}/conferences/{conference_id}/translate",
                    json=translation_request
                ) as response:
                    if response.status == 200:
                        translation = await response.json()
                        
                        # Check if translation contains expected keywords
                        translated_text = translation.get("translated_text", "").lower()
                        expected_keywords = translation_test["expected_keywords"]
                        has_keywords = any(keyword.lower() in translated_text for keyword in expected_keywords)
                        
                        self.log_test(
                            f"Translation Test {i+1}",
                            has_keywords,
                            f"{translation_test['source_language']} → {translation_test['target_language']}: {translation.get('translated_text', 'N/A')}"
                        )
                    else:
                        self.log_test(f"Translation Test {i+1}", False, f"Status: {response.status}")
                        
            except Exception as e:
                self.log_test(f"Translation Test {i+1}", False, f"Error: {str(e)}")
    
    async def test_conference_stats(self, conference_id: str):
        """Test conference statistics"""
        try:
            async with self.session.get(f"{API_BASE}/conferences/{conference_id}/stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    self.log_test(
                        "Conference Statistics",
                        True,
                        f"Participants: {stats.get('total_participants', 0)}, Languages: {stats.get('languages_used', [])}"
                    )
                else:
                    self.log_test("Conference Statistics", False, f"Status: {response.status}")
        except Exception as e:
            self.log_test("Conference Statistics", False, f"Error: {str(e)}")
    
    async def test_leave_conference(self, conference_id: str, participant_id: str):
        """Test participant leaving conference"""
        try:
            async with self.session.post(
                f"{API_BASE}/conferences/{conference_id}/leave/{participant_id}"
            ) as response:
                if response.status == 200:
                    self.log_test("Leave Conference", True, f"Participant {participant_id} left successfully")
                else:
                    self.log_test("Leave Conference", False, f"Status: {response.status}")
        except Exception as e:
            self.log_test("Leave Conference", False, f"Error: {str(e)}")
    
    async def test_list_conferences(self):
        """Test listing conferences"""
        try:
            async with self.session.get(f"{API_BASE}/conferences/") as response:
                if response.status == 200:
                    conferences = await response.json()
                    self.log_test(
                        "List Conferences",
                        True,
                        f"Found {len(conferences)} conferences"
                    )
                else:
                    self.log_test("List Conferences", False, f"Status: {response.status}")
        except Exception as e:
            self.log_test("List Conferences", False, f"Error: {str(e)}")
    
    async def test_active_conferences(self):
        """Test listing active conferences"""
        try:
            async with self.session.get(f"{API_BASE}/conferences/active/") as response:
                if response.status == 200:
                    conferences = await response.json()
                    self.log_test(
                        "List Active Conferences",
                        True,
                        f"Found {len(conferences)} active conferences"
                    )
                else:
                    self.log_test("List Active Conferences", False, f"Status: {response.status}")
        except Exception as e:
            self.log_test("List Active Conferences", False, f"Error: {str(e)}")
    
    async def run_all_tests(self):
        """Run all video conference tests"""
        print("📹 SEEKER Video Conference Testing")
        print("=" * 80)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Basic health check
        await self.test_health_check()
        print()
        
        # List existing conferences
        await self.test_list_conferences()
        await self.test_active_conferences()
        print()
        
        # Create and manage conference
        conference_id = await self.test_create_conference()
        if conference_id:
            print(f"🎯 Testing conference: {conference_id}")
            print()
            
            # Join participants
            participant_id = await self.test_join_conference(conference_id)
            if participant_id:
                # Test multilingual participants
                await self.test_multilingual_join(conference_id)
                print()
                
                # Test translation
                await self.test_translation(conference_id, participant_id)
                print()
                
                # Test statistics
                await self.test_conference_stats(conference_id)
                print()
                
                # Test leaving
                await self.test_leave_conference(conference_id, participant_id)
                print()
        
        # Final conference listing
        await self.test_list_conferences()
        await self.test_active_conferences()
        print()
        
        # Summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print("📊 Test Summary")
        print("=" * 80)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "N/A")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   - {result['test']}: {result['details']}")

async def main():
    """Main test function"""
    async with VideoConferenceTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    print("🚀 Starting SEEKER Video Conference Tests...")
    asyncio.run(main()) 