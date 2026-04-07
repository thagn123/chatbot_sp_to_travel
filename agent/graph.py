from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.nodes import call_model, tool_node, should_continue

def create_travel_agent():
    # Define the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    # Set entry point
    workflow.add_edge(START, "agent")

    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )

    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")

    # Compile the graph
    return workflow.compile()

# Instance of the agent
travel_buddy = create_travel_agent()
