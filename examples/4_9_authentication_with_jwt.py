#!/usr/bin/env python3
"""
Comprehensive example demonstrating JWT authentication with BSS Agent Server.
This example shows JWT token generation, validation, refresh tokens, and protected endpoints.

This tutorial uses PyJWT for JWT token handling, which is the recommended JWT library for Python.
"""

from bssagent.infrastructure import Server
from bssagent.auth import JWTAuth, AuthenticationWithJWT, RefreshTokenAuth
from fastapi import Depends, HTTPException
from pydantic import BaseModel

# Pydantic models for request/response
class LoginRequest(BaseModel):
    user_id: str
    password: str  # In real applications, this would be hashed

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class RefreshRequest(BaseModel):
    refresh_token: str

def jwt_auth_example():
    """Comprehensive JWT authentication example."""
    print("=== JWT Authentication Example ===")
    print("Using PyJWT for JWT token handling")
    
    # Create server
    server = Server(title="JWT Auth Server")
    server.create_app()
    
    # Create JWT authentication manager
    jwt_auth = JWTAuth(
        secret_key="your-super-secret-key-change-in-production",
        token_expiry_hours=1,  # 1 hour for access tokens
        refresh_token_expiry_days=30  # 30 days for refresh tokens
    )
    
    # Create authentication dependencies
    auth = AuthenticationWithJWT(jwt_auth)
    refresh_auth = RefreshTokenAuth(jwt_auth)
    
    # Simulated user database (in real apps, this would be a proper database)
    users_db = {
        "user1": {"password": "password123", "name": "John Doe", "email": "john@example.com"},
        "user2": {"password": "password456", "name": "Jane Smith", "email": "jane@example.com"},
        "admin": {"password": "admin123", "name": "Admin User", "email": "admin@example.com"}
    }
    
    # Login endpoint
    async def login_endpoint(login_data: LoginRequest):
        """Login endpoint that returns JWT tokens."""
        user_id = login_data.user_id
        password = login_data.password
        
        # Check if user exists and password is correct
        if user_id not in users_db or users_db[user_id]["password"] != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Generate tokens
        access_token = jwt_auth.create_access_token(
            user_id=user_id,
            additional_claims={
                "name": users_db[user_id]["name"],
                "email": users_db[user_id]["email"]
            }
        )
        refresh_token = jwt_auth.create_refresh_token(user_id=user_id)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=3600  # 1 hour in seconds
        )
    
    # Refresh token endpoint
    async def refresh_endpoint(user_id: str = Depends(refresh_auth)):
        """Refresh access token using refresh token."""
        # Generate new access token
        access_token = jwt_auth.create_access_token(
            user_id=user_id,
            additional_claims={
                "name": users_db.get(user_id, {}).get("name", ""),
                "email": users_db.get(user_id, {}).get("email", "")
            }
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token="",  # Don't return new refresh token
            expires_in=3600
        )
    
    # Protected endpoint that requires JWT authentication
    async def protected_endpoint(user_id: str = Depends(auth)):
        """Protected endpoint that requires valid JWT access token."""
        user_info = users_db.get(user_id, {})
        return {
            "message": "Access granted!",
            "user_id": user_id,
            "user_info": {
                "name": user_info.get("name", ""),
                "email": user_info.get("email", "")
            },
            "status": "authenticated"
        }
    
    # User profile endpoint
    async def profile_endpoint(user_id: str = Depends(auth)):
        """Get user profile information."""
        user_info = users_db.get(user_id, {})
        return {
            "user_id": user_id,
            "profile": {
                "name": user_info.get("name", ""),
                "email": user_info.get("email", ""),
                "created_at": "2024-01-01T00:00:00Z"  # Mock data
            }
        }
    
    # Logout endpoint
    async def logout_endpoint(user_id: str = Depends(auth)):
        """Logout endpoint that revokes all user tokens."""
        success = jwt_auth.revoke_all_user_tokens(user_id)
        if success:
            return {"message": "Successfully logged out", "user_id": user_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to logout")
    
    # Public endpoint (no authentication required)
    async def public_endpoint():
        """Public endpoint that doesn't require authentication."""
        return {
            "message": "This endpoint is public",
            "status": "no_auth_required",
            "available_endpoints": [
                "POST /login - Login with user_id and password",
                "POST /refresh - Refresh access token",
                "GET /protected - Protected endpoint (requires JWT)",
                "GET /profile - User profile (requires JWT)",
                "POST /logout - Logout (requires JWT)",
                "GET /public - Public endpoint (no auth required)"
            ]
        }
    
    # Add endpoints
    server.add_endpoint("/login", "POST", login_endpoint, tags=["authentication"])
    server.add_endpoint("/refresh", "POST", refresh_endpoint, tags=["authentication"])
    server.add_endpoint("/protected", "GET", protected_endpoint, tags=["protected"])
    server.add_endpoint("/profile", "GET", profile_endpoint, tags=["protected"])
    server.add_endpoint("/logout", "POST", logout_endpoint, tags=["authentication"])
    server.add_endpoint("/public", "GET", public_endpoint, tags=["public"])
    
    print("✓ Added endpoints:")
    print("  - POST /login - Login and get JWT tokens")
    print("  - POST /refresh - Refresh access token")
    print("  - GET /protected - Protected endpoint (requires JWT)")
    print("  - GET /profile - User profile (requires JWT)")
    print("  - POST /logout - Logout and revoke tokens")
    print("  - GET /public - Public endpoint (no auth required)")
    
    return server, users_db

def demonstrate_jwt_usage():
    """Demonstrate how to use JWT authentication."""
    print("\n=== JWT Usage Demonstration ===")
    print("Using PyJWT for JWT token handling")
    
    # Create JWT auth instance
    jwt_auth = JWTAuth(secret_key="demo-secret-key")
    
    # Example user
    user_id = "demo_user"
    
    # Generate tokens
    access_token = jwt_auth.create_access_token(
        user_id=user_id,
        additional_claims={"role": "user", "permissions": ["read", "write"]}
    )
    refresh_token = jwt_auth.create_refresh_token(user_id=user_id)
    
    print(f"Generated access token: {access_token[:50]}...")
    print(f"Generated refresh token: {refresh_token[:50]}...")
    
    # Validate token
    payload = jwt_auth.validate_token(access_token)
    if payload:
        print(f"✓ Token is valid for user: {payload['sub']}")
        print(f"  - Token type: {payload['type']}")
        print(f"  - Role: {payload.get('role', 'N/A')}")
        print(f"  - Permissions: {payload.get('permissions', [])}")
    else:
        print("✗ Token is invalid")
    
    return access_token, refresh_token

if __name__ == "__main__":
    # Create server and demonstrate usage
    server, users_db = jwt_auth_example()
    access_token, refresh_token = demonstrate_jwt_usage()
    
    print("\n" + "="*60)
    print("TESTING INSTRUCTIONS:")
    print("="*60)
    print("1. Start the server: server.run()")
    print("\n2. Test login endpoint:")
    print("   curl -X POST http://localhost:8000/login \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"user_id\": \"user1\", \"password\": \"password123\"}'")
    print("\n3. Test protected endpoint with JWT token:")
    print("   curl -X GET http://localhost:8000/protected \\")
    print("     -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'")
    print("\n4. Test refresh token endpoint:")
    print("   curl -X POST http://localhost:8000/refresh \\")
    print("     -H 'Authorization: Bearer YOUR_REFRESH_TOKEN'")
    print("\n5. Test logout endpoint:")
    print("   curl -X POST http://localhost:8000/logout \\")
    print("     -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'")
    print("\n6. Test public endpoint (no auth required):")
    print("   curl -X GET http://localhost:8000/public")
    
    print("\n" + "="*60)
    print("EXAMPLE TOKENS (for testing):")
    print("="*60)
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")
    print("\nExample curl commands with tokens:")
    print(f"curl -X GET http://localhost:8000/protected \\")
    print(f"  -H 'Authorization: Bearer {access_token}'")
    
    print("\n" + "="*60)
    print("JWT FEATURES:")
    print("="*60)
    print("✓ Uses PyJWT library for JWT handling")
    print("✓ Automatic token expiration handling")
    print("✓ Refresh token support")
    print("✓ Token revocation in database")
    print("✓ Additional claims support")
    print("✓ Secure token validation")
    print("✓ FastAPI dependency injection")
    
    # Uncomment to run the server
    # server.run(host="0.0.0.0", port=8000) 