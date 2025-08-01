# Security Framework

## Overview

The BSS Agent framework provides a comprehensive security layer to protect AI agents from malicious inputs, ensure data privacy, and prevent API abuse. This document covers three core security components:

- **Data Privacy Management**: Detects and handles sensitive information
- **Prompt Sanitization**: Prevents prompt injection attacks
- **Rate Limiting**: Protects API endpoints from abuse

## Basic Concepts

### Data Privacy in AI Agent Development

AI agents often process sensitive user data including personal information, API keys, and confidential business data. The data privacy manager helps:

- **Detect sensitive patterns** in user inputs and agent outputs
- **Log security events** for monitoring and compliance
- **Mask sensitive data** in logs and responses
- **Prevent data leakage** through proper sanitization

### Prompt Sanitization

Prompt injection attacks attempt to manipulate AI agents by injecting malicious instructions. The prompt sanitizer:

- **Removes dangerous patterns** like "ignore previous instructions"
- **Limits input length** to prevent resource exhaustion
- **Validates agent outputs** to prevent sensitive data exposure
- **Blocks script injection** attempts

### Rate Limiting for API Endpoints

AI Agent API servers are particularly vulnerable to abuse due to:

- **High computational costs** of LLM inference
- **Resource-intensive operations** that can be exploited
- **Potential for prompt injection** through rapid requests
- **Cost implications** of unlimited API access

Rate limiting provides:
- **Request throttling** per user/IP
- **Cost protection** against abuse
- **Resource management** for fair usage
- **Security against DDoS** attacks

## Usage

### Data Privacy Manager

The `DataPrivacyManager` class provides comprehensive data protection:

```python
from bssagent.security.data_privacy_manager import DataPrivacyManager

# Initialize privacy manager
privacy_manager = DataPrivacyManager()

# Detect sensitive data in text
sensitive_findings = privacy_manager.detect_sensitive_data(user_input)

# Mask sensitive data in responses
masked_text = privacy_manager.mask_sensitive_data(text)
```

**Key Features:**
- **PII Detection**: Email, phone, SSN, credit card, API keys
- **Pattern Matching**: Regex-based sensitive data identification
- **Data Masking**: Automatic replacement with safe placeholders
- **Middleware Integration**: FastAPI middleware for automatic processing

### Prompt Sanitizer

The `PromptSanitizer` class prevents prompt injection and validates outputs:

```python
from bssagent.security.prompt_sanitizer import PromptSanitizer

# Initialize sanitizer
sanitizer = PromptSanitizer(input_max_length=4000)

# Sanitize user input
clean_input = sanitizer.sanitize_input(user_message)

# Validate agent output
if sanitizer.validate_agent_output(agent_response):
    return agent_response
else:
    return "Error: Sensitive information detected"
```

**Key Features:**
- **Dangerous Pattern Removal**: Blocks injection attempts
- **Input Length Limiting**: Prevents resource exhaustion
- **Output Validation**: Ensures no sensitive data in responses
- **Configurable Patterns**: Customizable security rules

### Rate Limiting

The rate limiting system provides API protection:

```python
from bssagent.security.rate_limit import get_limiter

# Initialize rate limiter
limiter = get_limiter()

# Apply to endpoints
@app.post("/agent/chat")
@limiter.limit("10/minute")
async def chat_endpoint(request: Request):
    # Your endpoint logic
    pass
```

**Key Features:**
- **Redis Integration**: Scalable rate limiting storage
- **Configurable Limits**: Per-endpoint rate limits
- **Custom Handlers**: Graceful rate limit exceeded responses
- **Environment Configuration**: Flexible limit settings

## Code Example

The following example demonstrates a secure AI agent server with all security components integrated:

```python
# Apply security to an agent
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, MessagesState, StateGraph
from bssagent.core import BaseAgent
from bssagent.environment import setup_environment_variables
from bssagent.infrastructure import AgentServer
from bssagent.security import PromptSanitizer

# Setup environment variables
setup_environment_variables()

# Setup LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Define first node
def assistant_node(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

# Define agent
class MyAgent(BaseAgent):
    def define_graph(self):
        graph = StateGraph(MessagesState)
        graph.add_node("assistant", assistant_node)
        graph.add_edge(START, "assistant")
        graph.add_edge("assistant", END)
        self.set_compiled_graph(graph.compile())

# Create agent
agent = MyAgent(name="test_agent", description="A test agent")

# Create server with the agent
server = AgentServer(
    agent_instance=agent,
    # Use rate limiter to limit the number of requests to the agent
    use_rate_limiter=True,
    title="TestAgent server with FastAPI",
    description="A server for running simple agent",
    version="1.0.0",
    host="0.0.0.0",
    port=8000
)
app = server.get_app()

# Get limiter
limiter = server.limiter

# Define input sanitizer
input_sanitizer = PromptSanitizer()

# Define endpoint
@app.post("/run_agent")
@limiter.limit("2/minute")
async def run_agent_endpoint(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "Hello")
        # Sanitize input
        message = input_sanitizer.sanitize_input(message)
        # Create user-specific initial state
        initial_state = {
            "messages": [{"role": "user", "content": message}]
        }
        
        # Return streaming response
        return StreamingResponse(
            agent.stream(initial_state, {"configurable": {"thread_id": "123"}}),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control"
            }
        )
        
    except Exception as e:
        server.logger.error(f"Error in run_agent: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    # Run the server
    server.run()
```

### Security Features in the Example

1. **Rate Limiting**: `@limiter.limit("2/minute")` restricts requests to 2 per minute
2. **Input Sanitization**: `input_sanitizer.sanitize_input(message)` cleans user input
3. **Error Handling**: Graceful error responses without exposing sensitive information
4. **Streaming Response**: Efficient handling of long-running agent operations

### Environment Configuration

Set up your environment variables for security:

```bash
# Redis for rate limiting
REDIS_URL=redis://localhost:6379

# Rate limit configuration
RATE_LIMIT_DEFAULT_LIMITS=200/day,50/hour

# Optional: Custom rate limits per path
RATE_LIMIT_AGENT_CHAT=10/minute
```

### Complete Security Setup

For a production-ready security setup, add data privacy middleware:

```python
from bssagent.security.data_privacy_manager import DataPrivacyMiddlewareFactory

# Create custom privacy middleware
CustomPrivacyMiddleware = DataPrivacyMiddlewareFactory.create(
    enable_logging=True,
    enable_masking=True,
    log_level="INFO"
)

# Add to server
server.add_custom_middleware(CustomPrivacyMiddleware)
```

This comprehensive security framework ensures your AI agents are protected against common threats while maintaining performance and usability.
