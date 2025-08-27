#!/usr/bin/env python3
"""
Simple MongoDB Check Script for SEEKER
Run this script to check MongoDB status
"""

import subprocess
import sys

def check_mongodb():
    print("🔍 Checking MongoDB installation...")
    
    # Check if mongod is available
    try:
        result = subprocess.run(['mongod', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ MongoDB is installed")
            print(f"   Version: {result.stdout.strip()}")
            return True
    except:
        pass
    
    print("❌ MongoDB is not installed")
    print("\n📋 To install MongoDB:")
    print("1. Go to: https://www.mongodb.com/try/download/community")
    print("2. Download MongoDB Community Server 7.0 for Windows")
    print("3. Run the installer and choose 'Complete' installation")
    print("4. Make sure to install MongoDB as a Service")
    return False

def check_service():
    print("\n🔍 Checking MongoDB service...")
    
    try:
        result = subprocess.run(['sc', 'query', 'MongoDB'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            if 'RUNNING' in result.stdout:
                print("✅ MongoDB service is running")
                return True
            else:
                print("❌ MongoDB service is not running")
                print("   To start: Start-Service -Name 'MongoDB'")
                return False
        else:
            print("❌ MongoDB service not found")
            return False
    except:
        print("⚠️  Could not check service status")
        return False

def test_connection():
    print("\n🔍 Testing MongoDB connection...")
    
    try:
        result = subprocess.run(['mongosh', '--eval', 'db.runCommand("ping")'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ MongoDB connection successful")
            return True
        else:
            print("❌ MongoDB connection failed")
            return False
    except:
        print("❌ Could not test connection")
        return False

def main():
    print("🚀 SEEKER MongoDB Check")
    print("=" * 40)
    
    installed = check_mongodb()
    if not installed:
        return
    
    service_ok = check_service()
    if not service_ok:
        print("\n💡 To start MongoDB service:")
        print("   Start-Service -Name 'MongoDB'")
        return
    
    connection_ok = test_connection()
    if connection_ok:
        print("\n🎉 MongoDB is ready for SEEKER!")
        print("\n📝 Next steps:")
        print("1. Start SEEKER: uvicorn app.main:app --reload")
        print("2. Test API: python test_seeker.py")
    else:
        print("\n❌ MongoDB connection failed")

if __name__ == "__main__":
    main() 