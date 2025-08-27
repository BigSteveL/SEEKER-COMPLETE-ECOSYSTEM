#!/usr/bin/env python3
"""
MongoDB Setup Script for SEEKER AI Orchestration System
This script helps configure and test MongoDB connection.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_mongodb_installation():
    """Check if MongoDB is installed and running."""
    print("🔍 Checking MongoDB installation...")
    
    # Check if mongod is in PATH
    try:
        result = subprocess.run(['mongod', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ MongoDB is installed")
            print(f"   Version: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ MongoDB is not installed or not in PATH")
    return False

def check_mongodb_service():
    """Check if MongoDB service is running."""
    print("\n🔍 Checking MongoDB service status...")
    
    try:
        # Check Windows service
        result = subprocess.run(['sc', 'query', 'MongoDB'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and 'RUNNING' in result.stdout:
            print("✅ MongoDB service is running")
            return True
        else:
            print("❌ MongoDB service is not running")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  Could not check service status")
        return False

def test_mongodb_connection():
    """Test MongoDB connection."""
    print("\n🔍 Testing MongoDB connection...")
    
    try:
        # Try to connect using mongosh
        result = subprocess.run(['mongosh', '--eval', 'db.runCommand("ping")'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ MongoDB connection successful")
            return True
        else:
            print("❌ MongoDB connection failed")
            print(f"   Error: {result.stderr}")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Could not test connection (mongosh not found)")
        return False

def install_mongodb_instructions():
    """Provide MongoDB installation instructions."""
    print("\n📋 MongoDB Installation Instructions:")
    print("=" * 50)
    print("1. Download MongoDB Community Server:")
    print("   https://www.mongodb.com/try/download/community")
    print()
    print("2. Installation Steps:")
    print("   - Run the downloaded .msi file")
    print("   - Choose 'Complete' installation")
    print("   - Install MongoDB as a Service (recommended)")
    print("   - Install MongoDB Compass (optional GUI)")
    print()
    print("3. Default Settings:")
    print("   - Port: 27017")
    print("   - Data Directory: C:\\Program Files\\MongoDB\\Server\\7.0\\data")
    print("   - Service Name: MongoDB")
    print()
    print("4. After Installation:")
    print("   - MongoDB service should start automatically")
    print("   - Run this script again to verify")
    print()
    print("5. Manual Service Start (if needed):")
    print("   - Open Services (services.msc)")
    print("   - Find 'MongoDB' service")
    print("   - Right-click and select 'Start'")

def create_env_file():
    """Create .env file with MongoDB configuration."""
    env_content = """# SEEKER AI Orchestration System - Environment Configuration

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
DB_NAME=seeker_db

# Environment Settings
ENVIRONMENT=development
DEBUG=true

# Security Settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,*

# Logging
LOG_LEVEL=INFO

# API Settings
API_PREFIX=/api/v1
"""
    
    env_file = Path('.env')
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with MongoDB configuration")
    else:
        print("⚠️  .env file already exists")

def main():
    """Main setup function."""
    print("🚀 SEEKER AI Orchestration System - MongoDB Setup")
    print("=" * 60)
    
    # Check MongoDB installation
    mongodb_installed = check_mongodb_installation()
    
    if not mongodb_installed:
        install_mongodb_instructions()
        return
    
    # Check service status
    service_running = check_mongodb_service()
    
    if not service_running:
        print("\n⚠️  MongoDB service is not running")
        print("   Please start the MongoDB service and run this script again")
        return
    
    # Test connection
    connection_ok = test_mongodb_connection()
    
    if connection_ok:
        print("\n🎉 MongoDB is ready for SEEKER!")
        create_env_file()
        print("\n📝 Next Steps:")
        print("1. Start the SEEKER server: uvicorn app.main:app --reload")
        print("2. Test the API: python test_seeker.py")
        print("3. View API docs: http://localhost:8000/docs")
    else:
        print("\n❌ MongoDB connection failed")
        print("   Please check your MongoDB installation and try again")

if __name__ == "__main__":
    main() 