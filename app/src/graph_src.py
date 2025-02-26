from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import MessagesState
from langchain.chains import ConversationalRetrievalChain
from langchain_core.messages import HumanMessage, AIMessage
from .pdf_embeding import pdf_embeding
from .graph_state import AgentState



def addUserMessageNode(state: AgentState):
    state["messages"].append(HumanMessage(content=state["messages"][-1].content))
    return state

def addAIMessageNode(state: AgentState):
    state["messages"].append(AIMessage(content=state["messages"][-1].content))
    return state

def generator_prompt_template():
    prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant, you can read pdf and chat with user"),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks"),
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

def pdf_conditional(state: AgentState):
    if "pdf" in state["messages"][-1].content:
        return "pdf_path"
    else:
        return "root"


def get_pdf_path(state: AgentState):
    pdf_path = input("tell me pdf path : ")
    state["pdfPath"] = pdf_path
    return state

def pdf_model(state: AgentState, config: dict):
    print("!!! pdf model", state)

    question = input("What do you want to know : ")

    chat_history = []
    vector_store = pdf_embeding(state["pdfPath"])
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    model = config["configurable"]["model"]

    conversation_chain = ConversationalRetrievalChain.from_llm(model, retriever)

    result = conversation_chain.invoke({"question": question, "chat_history": chat_history})

    return {"messages": AIMessage(result['answer'])}

def call_model(state: AgentState, config: dict):
    print("!!! call model", state)
    if "historyMsg" not in state.keys():
        state["historyMsg"] = []
    prompt = config["configurable"]["prompt_template"]
    chain = prompt|config["configurable"]["model"]
    response = chain.invoke({"question": state["messages"][-1], "history":state["historyMsg"]})
    
    return {"messages": AIMessage(response)}