#!/usr/bin/env python3
"""
Test script to verify SEEKER Storyboard accessibility
"""

import os
import webbrowser
from pathlib import Path

def test_storyboard():
    """Test the storyboard HTML file"""
    storyboard_path = Path("static/seeker_storyboard.html")
    
    print("🚀 SEEKER Storyboard Test")
    print("=" * 50)
    
    if storyboard_path.exists():
        print(f"✅ Storyboard file found: {storyboard_path}")
        print(f"📁 File size: {storyboard_path.stat().st_size:,} bytes")
        
        # Try to open in browser
        try:
            webbrowser.open(f"file://{storyboard_path.absolute()}")
            print("🌐 Opened storyboard in default browser")
        except Exception as e:
            print(f"⚠️ Could not open browser: {e}")
            print(f"📄 Manual access: file://{storyboard_path.absolute()}")
        
        return True
    else:
        print(f"❌ Storyboard file not found: {storyboard_path}")
        return False

if __name__ == "__main__":
    success = test_storyboard()
    print("=" * 50)
    if success:
        print("🎉 Storyboard test completed successfully!")
    else:
        print("⚠️ Storyboard test failed!") 