from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode, tools_condition
from bssagent.core import BaseAgent
from langgraph.graph import MessagesState, StateGraph, START, END

# Define tools: add, multiply, subtract, divide
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

# Define state
class State(MessagesState):
    user_id: str

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_with_tools = llm.bind_tools(tools)

# Define first node
def assistant_node(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


class MyAgent(BaseAgent):
    def define_graph(self):
        graph = StateGraph(State)
        graph.add_node("assistant", assistant_node)
        graph.add_node("tools", ToolNode(tools))

        graph.add_edge(START, "assistant")
        graph.add_conditional_edges("assistant", tools_condition)
        graph.add_edge("tools", "assistant")

        self.set_compiled_graph(graph.compile())


if __name__ == "__main__":
    agent = MyAgent(name="my_agent", description="My first agent")
    result = agent.invoke({"messages": [f"Hello, what is (2 + 2 - 3) * 2?"]}, {"configurable": {"thread_id": "123"}})
    print(result)
   
            