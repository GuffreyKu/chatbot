from langchain_ollama import OllamaLLM
from langchain_core.tools import tool
from langchain.chains import ConversationalRetrievalChain
from .pdf_embedding import pdf_embeding


@tool(parse_docstring=True)
def pdf_model(pdf_path:str, question:str):
    """
    This tool processes a PDF file and answers questions using a conversational retrieval model.

    Args:
        question: The user's question about the document. Example:
                  "What is the main topic of the document?"
        pdf_path: The path to the PDF file. Example:
                  "path/to/document.pdf"

    Returns:
        str: The generated response to the input question.
    """
    # print(f"Question: {question}")
    # print(f"PDF Path: {pdf_path}")

    if not question or not pdf_path:
        raise ValueError("Both 'question' and 'pdf_path' must be provided in the query.")
    
    chat_history = []  # Stores previous conversation history
    vector_store = pdf_embeding(pdf_path)  # Converts PDF content into embeddings for retrieval
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})  # Retrieves relevant content
    
    model = OllamaLLM(
        model="llama3.1:8b"  
    )

    if model is None:
        raise ValueError("Model configuration is missing in the config dictionary.")
    
    conversation_chain = ConversationalRetrievalChain.from_llm(model, retriever)  # Creates a conversational retrieval chain
    result = conversation_chain.invoke({"question": question, "chat_history": chat_history})  # Queries the model

    return result.get("answer", "No answer found.")  # Returns the answer or a default response

tools =[
    pdf_model,
]

if __name__ == '__main__':
    print(pdf_model)
    print(pdf_model.name)
    print(pdf_model.description)
    print(pdf_model.args)
    pdf_model.invoke({'question':"Summarize the key points of the document", 
                      'pdf_path':'/Users/guffrey/chatbot/pdf/Evo2.pdf'})