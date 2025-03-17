from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode
from .graph_src import call_model
from .graph_state import AgentState
from .tools.image_tool import image_model
from .tools.pdf_tool import pdf_model


tools = [pdf_model, image_model]

def route_tools(state) -> bool:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "continue"
    return "end"

class Graph:
    def __init__(self):
        self.workflow = StateGraph(AgentState)
       
    def compile(self, memory):

        self.workflow.add_node("agent", call_model)
        self.workflow.add_node("tools", ToolNode(tools))

        self.workflow.add_edge(START, "agent")
        self.workflow.add_conditional_edges("agent", route_tools, {"continue":"tools", "end":END})
        self.workflow.add_edge("tools", "agent")

        return self.workflow.compile(checkpointer=memory)