#!/usr/bin/env python3
"""
Simple example demonstrating basic API key authentication.
This example shows the minimal setup required to protect endpoints with API keys.
"""

from bssagent.infrastructure import Server
from bssagent.auth import AuthenticationWithKey, APIKeyManagement
from fastapi import Depends

def simple_auth_example():
    """Simple example with one protected endpoint."""
    print("=== Simple API Key Authentication Example ===")
    
    # Create server
    server = Server(title="Simple Auth Server")
    server.create_app()
    
    # Create authentication dependency
    auth = AuthenticationWithKey()
    
    # Create API key manager for testing
    key_manager = APIKeyManagement()
    
    # Generate a test API key
    test_user_id = "test_user_123"
    api_key = key_manager.generate_api_key(test_user_id)
    print(f"Generated API key for user {test_user_id}: {api_key[:20]}...")
    
    # Protected endpoint that requires API key
    async def protected_endpoint(user_id: str = Depends(auth)):
        return {
            "message": "Access granted!",
            "user_id": user_id,
            "status": "authenticated"
        }
    
    # Public endpoint (no authentication required)
    async def public_endpoint():
        return {
            "message": "This endpoint is public",
            "status": "no_auth_required"
        }
    
    # Add endpoints
    server.add_endpoint("/public", "GET", public_endpoint, tags=["public"])
    server.add_endpoint("/protected", "GET", protected_endpoint, tags=["protected"])
    
    print("✓ Added endpoints:")
    print("  - GET /public (no auth required)")
    print("  - GET /protected (requires API key)")
    
    return server, api_key

if __name__ == "__main__":
    server, api_key = simple_auth_example()
    
    print("\n" + "="*50)
    print("TESTING INSTRUCTIONS:")
    print("1. Start the server: server.run()")
    print("2. Test public endpoint: GET /public")
    print("3. Test protected endpoint with API key:")
    print(f"   GET /protected")
    print(f"   Headers: X-API-Key: {api_key}")
    print("4. Test without API key (should fail with 401)")
    
    # Uncomment to run the server
    # server.run(host="0.0.0.0", port=8000) 