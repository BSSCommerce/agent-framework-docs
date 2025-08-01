from langchain_google_genai import ChatGoogleGenerativeAI
from bssagent.core import BaseAgent
from langgraph.graph import MessagesState, StateGraph, START, END
from bssagent.database.memory import setup_dbsaver, setup_dbstore
from bssagent.environment import setup_environment_variables

# Setup environment variables
setup_environment_variables()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Setup checkpointer and store
checkpointer = setup_dbsaver()
store = setup_dbstore()

# Define first node
def assistant_node(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

class MyAgent(BaseAgent):
    def define_graph(self):
        graph = StateGraph(MessagesState)
        graph.add_node("assistant", assistant_node)
        graph.add_edge(START, "assistant")
        graph.add_edge("assistant", END)
        self.graph = graph

# Create an agent
agent = MyAgent(name="my_agent", description="My first agent")

if __name__ == "__main__":
    # Define the thread
    thread = {"configurable": {"thread_id": "123"}}
 
    with checkpointer as cp, store as st:
        agent.compiled_graph = agent.graph.compile(checkpointer=cp, store=st)
        # Invoke the agent
        result = agent.invoke(
            {"messages": [f"Hello, how can I help you today?"]}, 
            thread
        )
        print(result)
    