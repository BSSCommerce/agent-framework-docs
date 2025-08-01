# User Session Management

## Overview

User session management is a critical component for multi-user AI applications. It enables the system to maintain separate conversation contexts for different users, ensuring that each user's interactions remain isolated and persistent across sessions.

## Basic Concepts

### User Session vs Thread

- **User Session**: A persistent record that tracks a user's interaction history and preferences
- **Thread**: A conversation context that maintains the flow of messages between a user and the AI agent

### Why Multi-User AI Needs Session Management

1. **Isolation**: Each user's conversations remain private and separate
2. **Persistence**: Conversation history is maintained across application restarts
3. **Context Continuity**: Users can resume conversations from where they left off
4. **Scalability**: The system can handle multiple concurrent users efficiently
5. **State Management**: User preferences and session data are preserved

## Usage

### AgentSessionManager Class

The `AgentSessionManager` class provides comprehensive session management with database persistence.

#### Key Features

- **Database Persistence**: Automatic table creation and data storage
- **Memory Caching**: Fast access to frequently used sessions
- **Thread Management**: Unique thread IDs for each user session
- **Session Lifecycle**: Create, update, deactivate, and list sessions

#### Database Schema

The manager automatically creates a `user_sessions` table with the following structure:

```sql
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    thread_id VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### Core Methods

#### Session Creation and Retrieval

```python
# Create a new session
session = session_manager.create_user_session(user_id="user123", title="New Chat")

# Get existing session or create new one
session = session_manager.get_or_create_user_session(user_id="user123", title="New Chat")

# Get current session (raises error if not found)
session = session_manager.get_current_user_session(user_id="user123")
```

#### Session Management

```python
# Update session data
session_manager.update_session(user_id="user123", updates={"title": "Updated Chat"})

# Deactivate session
session_manager.deactivate_session(user_id="user123")

# List all active sessions
active_sessions = session_manager.list_active_sessions()

# Clear memory cache
session_manager.clear_memory_cache()
```

#### Utility Methods

```python
# Check if user has active session
has_session = session_manager.has_session(user_id="user123")

# Get session count in memory
count = session_manager.get_session_count()
```

## Code Example

### Complete Implementation

Here's a complete example demonstrating user session management with an AI agent:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from bssagent.core import BaseAgent
from langgraph.graph import MessagesState, StateGraph, START, END
from bssagent.core import AgentSessionManager
from bssagent.environment import setup_environment_variables

# Setup environment variables
setup_environment_variables()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Define assistant node
def assistant_node(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

# Define custom agent
class MyAgent(BaseAgent):
    def define_graph(self):
        graph = StateGraph(MessagesState)
        graph.add_node("assistant", assistant_node)
        graph.add_edge(START, "assistant")
        graph.add_edge("assistant", END)
        self.set_compiled_graph(graph.compile())

def main():
    # Initialize session manager
    session_manager = AgentSessionManager()
    
    # Create or retrieve user session
    user_session = session_manager.get_or_create_user_session(
        user_id="123", 
        title="My First Chat"
    )
    
    # Display active sessions
    print("Active sessions:", session_manager.list_active_sessions())
    
    # Create agent instance
    agent = MyAgent(name="my_agent", description="My first agent")
    
    # Define thread configuration
    thread = {"configurable": {"thread_id": user_session["thread_id"]}}
    
    # Invoke agent with session context
    result = agent.invoke(
        {"messages": ["Hello, how can I help you today?"]}, 
        thread
    )
    
    print("Agent response:", result)
    
    # Update session with new title
    session_manager.update_session(
        user_id="123", 
        updates={"title": "Updated Chat Session"}
    )
    
    # Display updated session info
    updated_session = session_manager.get_current_user_session("123")
    print("Updated session:", updated_session)

if __name__ == "__main__":
    main()
```

### Key Components Explained

1. **Session Manager Initialization**: Creates database tables and manages session lifecycle
2. **Session Creation**: Generates unique thread IDs and stores session data
3. **Thread Configuration**: Links agent conversations to specific user sessions
4. **Session Updates**: Modifies session data and persists changes
5. **Session Retrieval**: Loads existing sessions from database or memory

### Session Data Structure

Each session contains:

```python
{
    "title": "Chat Session Title",
    "thread_id": "user123_uuid-string",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:30:00",
    "is_active": True
}
```

### Best Practices

1. **Always use `get_or_create_user_session()`** for new user interactions
2. **Update session titles** to reflect conversation context
3. **Deactivate sessions** when users log out or conversations end
4. **Monitor active sessions** to manage system resources
5. **Handle database errors gracefully** as the system falls back to memory-only mode

### Error Handling

The session manager includes built-in error handling:

- Database connection failures fall back to memory-only mode
- Missing sessions raise `ValueError` with descriptive messages
- Database operations are wrapped in try-catch blocks with warning messages

This robust session management system ensures reliable multi-user AI application operation with proper data persistence and user isolation.
