# API Key Authentication

## Overview

The BSS Agent framework provides robust API key authentication to secure agent endpoints and protect sensitive operations. This authentication system ensures that only authorized users can access agent functionality while maintaining flexibility for different deployment scenarios.

## Basic Concepts

### Why Agent APIs Need API Key Authentication

Agent APIs require authentication for several critical reasons:

1. **Security**: Protect sensitive agent operations and prevent unauthorized access
2. **Rate Limiting**: Track usage per user for fair resource allocation
3. **Audit Trail**: Maintain logs of who accessed what functionality
4. **Multi-tenancy**: Support multiple users with isolated sessions
5. **Compliance**: Meet security requirements for enterprise deployments

### Authentication Flow

```
Client Request → Extract API Key → Validate Key → Return User ID → Process Request
     ↓              ↓              ↓              ↓              ↓
   Headers    →  Key Manager  →  Database   →  User Context →  Endpoint
```

## Usage

### API Key Management

The `APIKeyManagement` class provides comprehensive API key operations:

#### Core Functions

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `generate_api_key(user_id)` | Create new API key for user | `user_id: str` | `str` (API key) |
| `validate_api_key(api_key)` | Verify API key validity | `api_key: str` | `Optional[str]` (user_id) |
| `revoke_api_key(api_key)` | Disable an API key | `api_key: str` | `bool` (success) |

#### Database Schema

```sql
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked BOOLEAN DEFAULT FALSE
);
```

### Authentication Dependency

The `AuthenticationWithKey` class provides FastAPI dependency injection:

#### Supported Header Formats

1. **X-API-Key header**: `X-API-Key: your_api_key_here`
2. **Authorization header**: `Authorization: ApiKey your_api_key_here`

#### Usage as Dependency

```python
from bssagent.auth.authentication_with_key import AuthenticationWithKey
from fastapi import Depends

auth = AuthenticationWithKey()

@app.get("/protected")
async def protected_endpoint(user_id: str = Depends(auth)):
    return {"user_id": user_id, "message": "Access granted"}
```

## Code Examples

### Simple Authentication Example

The following example demonstrates basic API key authentication setup:

```python
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
```

### Complete Authentication Example

For a more comprehensive example with global authentication middleware and agent integration, see the complete example in `src/bssagent/examples/server/auth_key/complete_auth_example.py`.

## Testing Your Authentication

### 1. Generate API Key

```python
from bssagent.auth.api_key_management import APIKeyManagement

key_manager = APIKeyManagement()
api_key = key_manager.generate_api_key("your_user_id")
print(f"API Key: {api_key}")
```

### 2. Test Protected Endpoint

```bash
# Success case
curl -H "X-API-Key: your_api_key" http://localhost:8000/protected

# Failure case (missing key)
curl http://localhost:8000/protected
```

### 3. Revoke API Key

```python
success = key_manager.revoke_api_key("your_api_key")
print(f"Key revoked: {success}")
```

## Security Best Practices

1. **Store API keys securely**: Never commit API keys to version control
2. **Use HTTPS**: Always use HTTPS in production environments
3. **Rotate keys regularly**: Implement key rotation policies
4. **Monitor usage**: Track API key usage for security monitoring
5. **Implement rate limiting**: Prevent abuse through rate limiting
6. **Log access**: Maintain audit logs of all API access

## Error Handling

The authentication system provides clear error responses:

- **401 Unauthorized**: Missing or invalid API key
- **Proper headers**: Includes `WWW-Authenticate: ApiKey` header
- **Detailed messages**: Clear error descriptions for debugging

## Integration with Agent Framework

The authentication system integrates seamlessly with the BSS Agent framework:

- **Session Management**: User context available in agent sessions
- **Database Integration**: Automatic table creation and management
- **Middleware Support**: Global authentication middleware available
- **Privacy Controls**: Works with data privacy middleware

This authentication system provides a solid foundation for securing your BSS Agent deployments while maintaining flexibility for different use cases.
