from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def pdf_embeding(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()  # This returns a list of Document objects

    # 2. Split the PDF content into smaller text chunks for better embedding results
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # 3. Initialize an embedding model.
    # Here we use HuggingFaceEmbeddings with a SentenceTransformer model.
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 4. Create a vector store (using FAISS) from the split documents and their embeddings.
    vector_store = FAISS.from_documents(docs, embedding_model)

    return vector_store
