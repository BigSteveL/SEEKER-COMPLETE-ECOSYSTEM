#!/usr/bin/env python3
"""
Check registered routes in SEEKER app
"""

import sys
sys.path.append('.')

from app.main import app

print("🔍 Checking SEEKER App Routes")
print("=" * 50)

for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        print(f"  {route.methods} {route.path}")
    elif hasattr(route, 'routes'):
        print(f"  Router: {route}")
        for subroute in route.routes:
            if hasattr(subroute, 'methods') and hasattr(subroute, 'path'):
                print(f"    {subroute.methods} {subroute.path}")

print("=" * 50)
print("✅ Route check completed") 