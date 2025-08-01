# Database Management

The BSS Agent framework provides comprehensive database management capabilities through two main components: **Database Connections** and **Memory Management**. This document covers the fundamental concepts, supported database types, and practical usage examples.

## Table of Contents

- [Basic Concepts](#basic-concepts)
- [Supported Database Types](#supported-database-types)
- [Database Connection Management](#database-connection-management)
- [Memory Management](#memory-management)
- [Code Examples](#code-examples)

## Basic Concepts

### Checkpoint and Store in LangGraph

LangGraph uses two key concepts for state management:

- **Checkpointer**: Manages the persistence of graph state and execution history
- **Store**: Handles the storage of intermediate results and conversation context

These components work together to maintain conversation continuity and enable stateful agent interactions across sessions.

## Supported Database Types

The framework supports the following database types for both connections and memory management:

| Database | Connection Support | Memory Support | Use Case |
|----------|-------------------|----------------|----------|
| PostgreSQL | ✅ | ✅ | Production applications |
| MongoDB | ✅ | ✅ | Document-based storage |
| MySQL | ✅ | ✅ | Traditional relational data |
| Redis | ✅ | ✅ | High-performance caching |
| SQLite | ✅ | ✅ | Development and testing |

## Database Connection Management

### Core Classes

The `db_connection.py` module provides a unified interface for database connections:

```python
from bssagent.database.db_connection import (
    DatabaseConnection,
    PostgresConnection,
    MongoConnection,
    MySQLConnection,
    RedisConnection,
    SQLiteConnection
)
```

### Connection Factory

Use the `get_db_connection()` function to create database connections:

```python
from bssagent.database.db_connection import get_db_connection

# Create a PostgreSQL connection
connection = get_db_connection(
    db_type="postgres",
    username="user",
    password="password",
    host="localhost",
    port=5432,
    database="myapp"
)
```

### Environment-Based Setup

Configure connections using environment variables:

```bash
# Database configuration
DB_TYPE=postgres
DB_USERNAME=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
```

```python
from bssagent.database.db_connection import setup_db_connection

# Automatically uses environment variables
connection = setup_db_connection()
```

### Context Manager Usage

Use the context manager for automatic connection cleanup:

```python
from bssagent.database.db_connection import get_db_connection_context

with get_db_connection_context() as db:
    # Use database connection
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
```

## Memory Management

### Database Saver Setup

The `memory.py` module provides functions for setting up LangGraph's checkpoint and store components:

```python
from bssagent.database.memory import setup_dbsaver, setup_dbstore

# Setup checkpointer for state persistence
checkpointer = setup_dbsaver()

# Setup store for intermediate results
store = setup_dbstore()
```

### Environment Configuration

Configure memory management using environment variables:

```bash
# Single database for all purposes
ONE_DB=1

# Or separate databases for different purposes
LANGGRAPH_CHECKPOINTER_TYPE=postgres
LANGGRAPH_CHECKPOINTER_HOST=localhost
LANGGRAPH_CHECKPOINTER_PORT=5432
LANGGRAPH_CHECKPOINTER_DATABASE=checkpoints
LANGGRAPH_CHECKPOINTER_USERNAME=user
LANGGRAPH_CHECKPOINTER_PASSWORD=password

LANGGRAPH_STORE_TYPE=postgres
LANGGRAPH_STORE_HOST=localhost
LANGGRAPH_STORE_PORT=5432
LANGGRAPH_STORE_DATABASE=store
LANGGRAPH_STORE_USERNAME=user
LANGGRAPH_STORE_PASSWORD=password
```

## Code Examples

### Basic Database Integration

Here's a complete example showing how to integrate database management with an agent:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from bssagent.core import BaseAgent
from langgraph.graph import MessagesState, StateGraph, START, END
from bssagent.database.memory import setup_dbsaver, setup_dbstore
from bssagent.environment import setup_environment_variables

# Setup environment variables
setup_environment_variables()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Setup database components
checkpointer = setup_dbsaver()
store = setup_dbstore()

# Define agent node
def assistant_node(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

# Create agent class
class MyAgent(BaseAgent):
    def define_graph(self):
        graph = StateGraph(MessagesState)
        graph.add_node("assistant", assistant_node)
        graph.add_edge(START, "assistant")
        graph.add_edge("assistant", END)
        self.graph = graph

# Initialize agent
agent = MyAgent(name="my_agent", description="My first agent")

# Main execution
if __name__ == "__main__":
    # Define thread configuration
    thread = {"configurable": {"thread_id": "123"}}
 
    # Execute with database context
    with checkpointer as cp, store as st:
        agent.compiled_graph = agent.graph.compile(checkpointer=cp, store=st)
        
        # Invoke the agent
        result = agent.invoke(
            {"messages": [f"Hello, how can I help you today?"]}, 
            thread
        )
        print(result)
```

### Advanced Usage Patterns

#### Custom Database Connection

```python
from bssagent.database.db_connection import get_db_connection

# Custom PostgreSQL connection
pg_conn = get_db_connection(
    db_type="postgres",
    username="admin",
    password="secure_password",
    host="db.example.com",
    port=5432,
    database="production_db"
)

# Use connection
with pg_conn:
    cursor = pg_conn.cursor()
    cursor.execute("SELECT version()")
    version = cursor.fetchone()
    print(f"PostgreSQL version: {version}")
```

#### Redis for Caching

```python
from bssagent.database.db_connection import get_redis_connection

# Get Redis connection
redis_conn = get_redis_connection()

# Cache data
redis_conn.set("user:123", "user_data", ex=3600)  # Expire in 1 hour

# Retrieve cached data
user_data = redis_conn.get("user:123")
```

#### MongoDB Document Storage

```python
from bssagent.database.db_connection import get_mongo_connection

# Get MongoDB connection
mongo_conn = get_mongo_connection()

# Access collection
users_collection = mongo_conn.get_collection("users")

# Insert document
user_doc = {"name": "John", "email": "john@example.com"}
users_collection.insert_one(user_doc)
```

## Best Practices

1. **Environment Variables**: Always use environment variables for database credentials
2. **Connection Pooling**: Use context managers for automatic connection cleanup
3. **Error Handling**: Implement proper error handling for database operations
4. **Security**: Never hardcode database credentials in your code
5. **Testing**: Use SQLite for development and testing environments

## Troubleshooting

### Common Issues

1. **Connection Errors**: Verify database credentials and network connectivity
2. **Missing Dependencies**: Install required database drivers (psycopg2, pymongo, etc.)
3. **Environment Variables**: Ensure all required environment variables are set
4. **Database Permissions**: Verify database user has appropriate permissions

### Debug Mode

Enable debug logging to troubleshoot database issues:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

This comprehensive database management system provides the foundation for building scalable, stateful AI agents with persistent memory and robust data storage capabilities.
