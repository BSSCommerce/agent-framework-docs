# This exmample show how to use SuperVisor agent, a built-in agent template of LangGraph

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
        agent = MyAgent(name="MyAgent", description="A helpful assistant that can add and multiply numbers and search the web for information.")
        agent.compiled_graph = agent.graph.compile(store=st, checkpointer=cp)
        result = agent.invoke(
            {
                "messages": [{"role": "user", "content": "what's the combined headcount of the FAANG companies in 2024?"}]
            },
            {"configurable": {"thread_id": "123"}}
        )
        print(result)