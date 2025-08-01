# Server API

The Server API provides a robust foundation for deploying AI agents as web services using FastAPI. This module enables you to create scalable, production-ready endpoints for your LangGraph-based agents with built-in streaming support, session management, and security features.

## Basic Concepts

### Why Server API for AI Agents?

When developing AI agents with LangGraph, you need a way to expose your agents as web services. The Server API addresses several key challenges:

1. **Streaming Support**: LangGraph agents can stream responses in real-time, providing better user experience
2. **Session Management**: Handle multiple concurrent user sessions with proper isolation
3. **Production Deployment**: FastAPI provides high performance, automatic API documentation, and built-in validation
4. **Security**: Built-in rate limiting, CORS support, and authentication mechanisms
5. **Monitoring**: Health checks and metrics endpoints for production monitoring

### LangGraph Invoke vs Stream

The Server API supports both synchronous and streaming execution modes:

- **Invoke Mode**: Traditional request-response pattern, suitable for quick responses
- **Stream Mode**: Real-time streaming of agent responses, ideal for long-running conversations

```python
# Invoke mode - returns complete response
result = agent.invoke(initial_state)

# Stream mode - yields responses as they're generated
for chunk in agent.stream(initial_state):
    yield chunk
```

## Usage

### Core Classes

#### `Server`
The base server class that provides FastAPI application management and configuration.

```python
from bssagent.infrastructure import Server

server = Server(
    title="My Agent Server",
    description="A server for my AI agent",
    version="1.0.0",
    host="0.0.0.0",
    port=8000,
    enable_cors=True
)
```

#### `AgentServer`
A specialized server class designed specifically for agent applications with built-in agent endpoints.

```python
from bssagent.infrastructure import AgentServer

server = AgentServer(
    agent_instance=my_agent,
    use_rate_limiter=True,
    title="Agent API Server"
)
```

### Key Methods

#### Server Configuration
- `create_app()`: Creates and configures the FastAPI application
- `add_endpoint()`: Adds custom endpoints to the server
- `add_health_check()`: Adds a health check endpoint
- `add_metrics_endpoint()`: Adds monitoring metrics endpoint

#### Agent Integration
- `add_agent_endpoints()`: Adds standard agent endpoints (sessions, etc.)
- `add_limiter()`: Adds rate limiting capabilities
- `add_custom_middleware()`: Adds custom middleware to the application

#### Server Management
- `run()`: Starts the server with uvicorn
- `get_app()`: Returns the FastAPI app instance

### Standard Endpoints

The `AgentServer` automatically provides these endpoints:

- `GET /health`: Health check endpoint
- `GET /metrics`: Server metrics and monitoring
- `GET /sessions`: List active sessions
- `DELETE /sessions/{user_id}`: Delete a specific session

## Code Example

This example demonstrates how to create a complete agent server with streaming support.

### Complete Implementation

```python
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, MessagesState, StateGraph
from bssagent.core import BaseAgent
from bssagent.environment import setup_environment_variables
from bssagent.infrastructure import AgentServer

# Setup environment variables
setup_environment_variables()

# Setup LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Define assistant node
def assistant_node(state: MessagesState):
    """Process user messages and generate responses."""
    return {"messages": [llm.invoke(state["messages"])]}

# Define agent with LangGraph
class MyAgent(BaseAgent):
    def define_graph(self):
        """Define the agent's conversation flow."""
        graph = StateGraph(MessagesState)
        graph.add_node("assistant", assistant_node)
        graph.add_edge(START, "assistant")
        graph.add_edge("assistant", END)
        self.set_compiled_graph(graph.compile())

# Create agent instance
agent = MyAgent(name="test_agent", description="A test agent")

# Create server with the agent
server = AgentServer(
    agent_instance=agent,
    use_rate_limiter=False,
    title="TestAgent server with FastAPI",
    description="A server for running simple agent",
    version="1.0.0",
    host="0.0.0.0",
    port=8000
)
app = server.get_app()

# Define custom endpoint for agent interaction
@app.post("/run_agent")
async def run_agent_endpoint(request: Request):
    """Endpoint to run the agent with streaming response."""
    try:
        data = await request.json()
        message = data.get("message", "Hello")
        
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

### Key Features Explained

1. **Agent Definition**: The `MyAgent` class extends `BaseAgent` and defines a simple conversation flow using LangGraph
2. **Server Setup**: `AgentServer` creates a FastAPI application with built-in agent support
3. **Streaming Endpoint**: The `/run_agent` endpoint uses `StreamingResponse` to provide real-time responses
4. **Error Handling**: Comprehensive error handling with proper logging
5. **CORS Support**: Built-in CORS headers for web client integration

### Usage Patterns

#### Basic Server Setup
```python
# Simple server without agent
server = Server(title="My API", port=8000)
app = server.get_app()
server.run()
```

#### Agent Server with Rate Limiting
```python
# Agent server with rate limiting
server = AgentServer(
    agent_instance=my_agent,
    use_rate_limiter=True,
    title="Production Agent API"
)
```

#### Custom Endpoints
```python
# Add custom endpoints
@app.post("/custom_endpoint")
async def custom_handler(request: Request):
    # Your custom logic here
    return {"result": "success"}
```

### Testing the Server

Once running, you can test the endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Run agent (with streaming)
curl -X POST http://localhost:8000/run_agent \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'

# List sessions
curl http://localhost:8000/sessions
```

The Server API provides a production-ready foundation for deploying AI agents as web services, with built-in support for streaming, session management, and monitoring capabilities.
