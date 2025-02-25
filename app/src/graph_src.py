from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import MessagesState
from langchain.chains import ConversationalRetrievalChain
from langchain_core.messages import HumanMessage, AIMessage
from .pdf_embeding import pdf_embeding


def addUserMessageNode(state: MessagesState):
    state["messages"].append(HumanMessage(content=state["messages"][-1].content))
    return state

def addAIMessageNode(state: MessagesState):
    state["messages"].append(AIMessage(content=state["messages"][-1].content))
    return state

def generator_prompt_template():
    prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks"),
    ("human", "{question}"),
    ])
    return prompt_template


def pdf_conditional(state: MessagesState):
    print("!!!!!", state)
    if "pdf" in state["messages"][0].content:
        return "pdf_path"
    else:
        return "root"


def get_pdf_path(state: MessagesState):
    pdf_path = input("tell me pdf path : ")
    return pdf_path

def pdf_model(state: MessagesState, config: dict):
    
    chat_history = []

    vector_store = pdf_embeding(state["messages"])
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    model = config["configurable"]["model"]

    conversation_chain = ConversationalRetrievalChain.from_llm(model, retriever)

    result = conversation_chain.invoke({"question": "Summary pdf", "chat_history": chat_history})

    return {"messages": result}

def call_model(state: MessagesState, config: dict):
    prompt = config["configurable"]["prompt_template"]
    chain = prompt|config["configurable"]["model"]
    response = chain.invoke({"question": state["messages"]})
    
    return {"messages": AIMessage(response)}