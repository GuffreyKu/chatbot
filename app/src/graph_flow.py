from langgraph.graph import START, END, StateGraph
from .graph_src import call_model, pdf_conditional, get_pdf_path
from .graph_state import AgentState

class Graph:
    def __init__(self):
        self.workflow = StateGraph(AgentState)

    def compile(self, memory):

        self.workflow.add_node("root", call_model)
        self.workflow.add_node("pdf_path", get_pdf_path)

        self.workflow.add_conditional_edges(START, pdf_conditional)
        self.workflow.add_edge("pdf_path", END)
        self.workflow.add_edge("root", END)


        return self.workflow.compile(checkpointer=memory)