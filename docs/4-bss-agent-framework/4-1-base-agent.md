
## Basic Concepts

### AI Agent
An AI agent is an autonomous system that can perceive its environment, make decisions, and take actions to achieve specific goals. In the BSS Agent framework, agents are built using LangGraph's state management and workflow capabilities.

### Workflow Graph
A workflow graph defines the execution flow of an agent through nodes and edges:
- **Nodes**: Represent processing steps (e.g., LLM calls, tool execution)
- **Edges**: Define the flow between nodes
- **State**: Maintains conversation context and data throughout execution

### Tools
Tools are functions that agents can call to perform specific tasks:
- Mathematical operations (add, multiply, subtract, divide)
- API calls and external integrations
- Data processing and transformation
- Custom business logic

### Breakpoints
Breakpoints allow agents to pause execution at specific points:
- Enable debugging and inspection
- Support step-by-step execution
- Allow for manual intervention when needed

### Interrupts
Interrupts provide mechanisms to handle external events:
- Pause and resume execution
- Handle user input during processing
- Manage long-running operations

## Usage

### BaseAgent Class

The `BaseAgent` class serves as the foundation for all agents in the framework:

```python
from bssagent.core import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
    
    def define_graph(self):
        # Define your workflow graph here
        pass
```

### Core Features

#### 1. Agent Information
```python
agent = MyAgent(name="my_agent", description="My first agent")
print(agent.get_name())  # "my_agent"
```

#### 2. Workflow Graph Definition
```python
def define_graph(self):
    graph = StateGraph(State)
    
    # Add nodes
    graph.add_node("assistant", assistant_node)
    graph.add_node("tools", ToolNode(tools))
    
    # Add edges
    graph.add_edge(START, "assistant")
    graph.add_conditional_edges("assistant", tools_condition)
    graph.add_edge("tools", "assistant")
    
    self.set_compiled_graph(graph.compile())
```

#### 3. Invoke Method
Execute the agent with initial state:
```python
result = agent.invoke(
    {"messages": ["Hello, what is 2 + 2?"]}, 
    {"configurable": {"thread_id": "123"}}
)
```

#### 4. Stream Method
Stream agent responses in real-time:
```python
async for chunk in agent.stream(state, thread, stream_mode="values"):
    print(chunk)  # Process streaming data
```

#### 5. Continue Execution
Resume execution after interruptions:
```python
# Get current state
current_state = agent.get_state(thread)

# Continue from current state
result = agent.continue_execution(thread)
```

## Code Example

### Complete Implementation

Here's a complete example demonstrating a mathematical agent:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode, tools_condition
from bssagent.core import BaseAgent
from langgraph.graph import MessagesState, StateGraph, START, END

# Define mathematical tools
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

def subtract(a: float, b: float) -> float:
    """Subtract two numbers"""
    return a - b

def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    return a / b

tools = [add, multiply, subtract, divide]

# Define state with user identification
class State(MessagesState):
    user_id: str

# Initialize LLM with tool binding
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_with_tools = llm.bind_tools(tools)

# Define assistant processing node
def assistant_node(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Create custom agent class
class MathAgent(BaseAgent):
    def define_graph(self):
        # Create workflow graph
        graph = StateGraph(State)
        
        # Add processing nodes
        graph.add_node("assistant", assistant_node)
        graph.add_node("tools", ToolNode(tools))
        
        # Define execution flow
        graph.add_edge(START, "assistant")
        graph.add_conditional_edges("assistant", tools_condition)
        graph.add_edge("tools", "assistant")
        
        # Compile and set the graph
        self.set_compiled_graph(graph.compile())

# Usage example
if __name__ == "__main__":
    # Create and configure agent
    agent = MathAgent(
        name="math_agent", 
        description="An agent that performs mathematical calculations"
    )
    
    # Execute with mathematical query
    result = agent.invoke(
        {"messages": ["What is (2 + 2 - 3) * 2?"]}, 
        {"configurable": {"thread_id": "123"}}
    )
    
    print(result)
```

### Key Components Explained

1. **Tool Definition**: Mathematical functions that the agent can call
2. **State Management**: `State` class extends `MessagesState` with user identification
3. **LLM Integration**: Google's Gemini model with tool binding
4. **Graph Structure**: Defines the workflow with assistant and tool nodes
5. **Conditional Execution**: Uses `tools_condition` to determine when to call tools

### Execution Flow

1. **Input**: User sends a mathematical query
2. **Assistant Node**: LLM processes the query and decides which tools to use
3. **Tool Execution**: Mathematical operations are performed
4. **Response**: Results are formatted and returned to the user

This framework provides a robust foundation for building intelligent agents that can handle complex workflows, maintain state, and interact with external tools seamlessly.
