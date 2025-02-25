from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain


def pdf_embeding(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()  # This returns a list of Document objects
    # 2. Split the PDF content into smaller text chunks for better embedding results
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    # 3. Initialize an embedding model.
    # Here we use HuggingFaceEmbeddings with a SentenceTransformer model.
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # 4. Create a vector store (using FAISS) from the split documents and their embeddings.
    vector_store = FAISS.from_documents(docs, embedding_model)
    return vector_store


pdf_path = "../pdf/Evo2.pdf"

vector_store = pdf_embeding(pdf_path)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

llm = OllamaLLM(
    model="deepseek-r1:14b"
    )

conversation_chain = ConversationalRetrievalChain.from_llm(llm, retriever)

chat_history = []

query = "请问文档中提到了哪些关键点？"
result = conversation_chain.invoke({"question": query, "chat_history": chat_history})
print("回答：", result['answer'])
