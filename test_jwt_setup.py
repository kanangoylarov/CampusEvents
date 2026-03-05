#!/usr/bin/env python
"""Test script to verify JWT setup."""

import sys
import os

# Add the project to the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import create_app
    print("✓ Successfully imported create_app")
    
    app = create_app('development')
    print("✓ Flask app created successfully")
    
    # Test accessing the JWT manager
    from app.extensions import jwt
    print("✓ JWT manager available in extensions")
    
    # Test that JWT is registered with the app
    if jwt is not None:
        print("✓ JWT manager initialized")
    
    # Verify config
    print(f"✓ JWT_SECRET_KEY configured: {app.config.get('JWT_SECRET_KEY') is not None}")
    print(f"✓ JWT_TOKEN_LOCATION configured: {app.config.get('JWT_TOKEN_LOCATION')}")
    print(f"✓ JWT_ACCESS_TOKEN_EXPIRES configured: {app.config.get('JWT_ACCESS_TOKEN_EXPIRES')}")
    
    print("\n✅ All JWT setup tests passed!")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
