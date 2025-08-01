from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, MessagesState, StateGraph
from bssagent.core import BaseAgent
from bssagent.environment  import setup_environment_variables
from bssagent.infrastructure import AgentServer


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
    use_rate_limiter=False,
    title="TestAgent server with FastAPI",
    description="A server for running simple agent",
    version="1.0.0",
    host="0.0.0.0",
    port=8000
)
app = server.get_app()

# Define endpoint
@app.post("/run_agent")
async def run_agent_endpoint(request: Request):
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

    