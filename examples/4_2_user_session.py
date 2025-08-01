from langchain_google_genai import ChatGoogleGenerativeAI
from bssagent.core import BaseAgent
from langgraph.graph import MessagesState, StateGraph, START, END

from bssagent.core import AgentSessionManager
from bssagent.environment import setup_environment_variables

# Setup environment variables
setup_environment_variables()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Define first node
def assistant_node(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

class MyAgent(BaseAgent):
    def define_graph(self):
        graph = StateGraph(MessagesState)
        graph.add_node("assistant", assistant_node)
        graph.add_edge(START, "assistant")
        graph.add_edge("assistant", END)
        self.set_compiled_graph(graph.compile())

if __name__ == "__main__":

    # Create a new session for the user
    session_manager = AgentSessionManager()
    user_session = session_manager.get_or_create_user_session(user_id="123")

    # Define the thread
    thread = {"configurable": {"thread_id": user_session["thread_id"]}}

    # Show live sessions
    print("Live sessions: ", session_manager.list_active_sessions())

    # Create an agent
    agent = MyAgent(name="my_agent", description="My first agent")

    # Invoke the agent
    result = agent.invoke(
        {"messages": [f"Hello, how can I help you today?"]}, 
        thread
    )
    print(result)
   