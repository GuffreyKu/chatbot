from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode
from .graph_src import call_model, collect_history
from .graph_state import AgentState
from .graph_tools import tools


def route_tools(state) -> bool:

    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "history"

class Graph:
    def __init__(self):
        self.workflow = StateGraph(AgentState)
       
    def compile(self, memory):

        self.workflow.add_node("agent", call_model)
        self.workflow.add_node("tools", ToolNode(tools))
        self.workflow.add_node("history", collect_history)

        self.workflow.add_edge(START, "agent")
        self.workflow.add_conditional_edges("agent", route_tools, {"tools":"tools", "history":"history"})
        self.workflow.add_edge("tools", "agent")
        self.workflow.add_edge("agent", "history")
        self.workflow.add_edge("history", END)

        return self.workflow.compile(checkpointer=memory)