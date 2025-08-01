# Advanced Agent Architectures

This tutorial demonstrates how to build sophisticated multi-agent applications using LangGraph's built-in agent architectures. We'll explore two powerful patterns: **ReAct** and **Supervisor** architectures.

## Table of Contents

- [Basic Concepts](#basic-concepts)
  - [ReAct Architecture](#react-architecture)
  - [Supervisor Architecture](#supervisor-architecture)
- [Use Cases](#use-cases)
  - [ReAct Use Cases](#react-use-cases)
  - [Supervisor Use Cases](#supervisor-use-cases)
- [Code Example](#code-example)
  - [Complete Implementation](#complete-implementation)
  - [Running the Example](#running-the-example)

## Basic Concepts

### ReAct Architecture

The **ReAct** (Reasoning and Acting) architecture enables agents to reason about problems and take actions using tools. It follows a cycle of:

1. **Reasoning**: The agent thinks about the problem
2. **Acting**: The agent uses tools to gather information or perform actions
3. **Observing**: The agent observes the results and continues the cycle

**Key Features:**
- Tool-based reasoning
- Iterative problem-solving
- Structured decision-making
- Built-in error handling

### Supervisor Architecture

The **Supervisor** architecture orchestrates multiple specialized agents, acting as a coordinator that:

1. **Routes** requests to appropriate specialized agents
2. **Manages** agent interactions and workflows
3. **Combines** results from multiple agents
4. **Provides** unified responses

**Key Features:**
- Multi-agent coordination
- Specialized agent delegation
- Workflow management
- Unified interface

## Use Cases

### ReAct Use Cases

| Use Case | Description | Tools Required |
|----------|-------------|----------------|
| **Data Analysis** | Analyze datasets and generate insights | Calculator, Database tools |
| **Code Review** | Review and suggest improvements to code | Code analysis, Linting tools |
| **Research Assistant** | Gather and synthesize information | Web search, Document tools |
| **Task Automation** | Automate repetitive tasks | File operations, API calls |

### Supervisor Use Cases

| Use Case | Description | Agent Types |
|----------|-------------|-------------|
| **Customer Support** | Route queries to specialized departments | Technical, Billing, General support |
| **Content Creation** | Coordinate content generation workflows | Research, Writing, Editing |
| **Data Processing** | Orchestrate data transformation pipelines | Data extraction, Transformation, Loading |
| **Multi-domain QA** | Answer questions across different domains | Domain-specific experts |

## Code Example

This example demonstrates a **Supervisor** architecture that coordinates two specialized agents:
- **Math Agent**: Handles mathematical calculations
- **Web Search Agent**: Retrieves current information

### Complete Implementation

```python
# This example shows how to use Supervisor agent, a built-in agent template of LangGraph

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from bssagent.core import BaseAgent
from bssagent.database.memory import setup_dbsaver, setup_dbstore
from bssagent.environment import setup_environment_variables

setup_environment_variables()

# Create Tools
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def web_search(query: str) -> str:
    """Search the web for information."""
    return (
        "Here are the headcounts for each of the FAANG companies in 2024:\n"
        "1. **Facebook (Meta)**: 67,317 employees.\n"
        "2. **Apple**: 164,000 employees.\n"
        "3. **Amazon**: 1,551,000 employees.\n"
        "4. **Netflix**: 14,000 employees.\n"
        "5. **Google (Alphabet)**: 181,269 employees."
    )

# Define ChatModel
google_genai_chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Define store
store = setup_dbstore()

# Define checkpoint
checkpoint = setup_dbsaver()

# Define agent
class MyAgent(BaseAgent):
    def define_graph(self):
        # Create math agent
        math_agent = create_react_agent(
            model=google_genai_chat,
            tools=[add, multiply],
            name="math_agent",
            prompt="""
            You are a helpful assistant that can add and multiply numbers.
            """
        )
        
        # Create web search agent
        web_search_agent = create_react_agent(
            model=google_genai_chat,
            tools=[web_search],
            name="web_search_agent",
            prompt="""
            You are a helpful assistant that can search the web for information.
            """
        )

        graph = create_supervisor(
            [math_agent, web_search_agent],
            model=google_genai_chat,
            prompt="""
            You are a team supervisor managing a research expert and a math expert. 
            For current events, use research_agent. 
            For math problems, use math_agent.
            """
        )
        self.graph = graph

if __name__ == "__main__":
    with store as st, checkpoint as cp:
        agent = MyAgent(
            name="MyAgent", 
            description="A helpful assistant that can add and multiply numbers and search the web for information."
        )
        agent.compiled_graph = agent.graph.compile(store=st, checkpointer=cp)
        result = agent.invoke(
            {
                "messages": [{"role": "user", "content": "what's the combined headcount of the FAANG companies in 2024?"}]
            },
            {"configurable": {"thread_id": "123"}}
        )
        print(result)
```

### Running the Example

1. **Setup Environment**: Ensure you have the required dependencies installed
2. **Configure API Keys**: Set up your Google Generative AI API key
3. **Run the Script**: Execute the example to see the supervisor in action

**Expected Output:**
The agent will:
1. Use the web search agent to gather FAANG company headcounts
2. Use the math agent to calculate the total combined headcount
3. Return the final result with reasoning

## Architecture Benefits

### ReAct Benefits
- **Structured Reasoning**: Clear thinking process with tool usage
- **Error Recovery**: Built-in mechanisms to handle failures
- **Transparency**: Visible reasoning steps for debugging
- **Flexibility**: Easy to add new tools and capabilities

### Supervisor Benefits
- **Specialization**: Each agent focuses on specific domains
- **Scalability**: Easy to add new specialized agents
- **Coordination**: Centralized workflow management
- **Modularity**: Agents can be developed and tested independently

## Next Steps

- Explore more complex multi-agent workflows
- Implement custom tools for your specific use cases
- Add error handling and retry mechanisms
- Integrate with external APIs and services
- Build custom agent architectures for specialized domains
