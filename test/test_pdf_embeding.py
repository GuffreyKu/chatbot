from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Load the PDF file (replace "example.pdf" with your file)
pdf_path = "../pdf/Evo2.pdf"
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

# 5. (Optional) Test the retrieval by querying the vector store.
query = "What is the main topic of the document?"
results = vector_store.similarity_search(query, k=3)

# Print out the retrieved document chunks
for idx, doc in enumerate(results):
    print(f"--- Document Chunk {idx+1} ---")
    print(doc.page_content)
    print()