from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_core.messages import AIMessage
from .pdf_embeding import pdf_embeding
from .graph_state import AgentState
from .PROMPT import AGENT_PROMPT


def generator_prompt_template():
    prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant, you can read pdf and chat with user"),
    ("system", "%s"%AGENT_PROMPT),
    ("human", "Hello, how are you ?"),
    ("ai", "I'm ai assistant."),
    ("{history}"),
    ("human", "{question}"),
    ])
    return prompt_template

def collect_history(state: AgentState):
    if "historyMsg" not in state.keys():
        state["historyMsg"] = []
    for i, msg in enumerate(state["messages"][-2:]):
        if i%2 == 0:
            state["historyMsg"].append(("human", msg.content))
        else:
            state["historyMsg"].append(("ai", msg.content))

    return state

def call_model(state: AgentState, config: dict):

    if "historyMsg" not in state.keys():
        state["historyMsg"] = []

    prompt = config["configurable"]["prompt_template"]
    chain = prompt|config["configurable"]["model"]
    response = chain.invoke({"question": state["messages"][-1], "history":state["historyMsg"]})

    return {"messages": AIMessage(response["messages"][-1].content)}