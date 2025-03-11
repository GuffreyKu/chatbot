from typing import TypedDict, Annotated,  List
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    pdfPath: str
    historyMsg: list