from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


# Instantiate the Ollama LLM
llm = OllamaLLM(
    model="deepseek-r1:14b",  # e.g., "llama2" or whichever model you have installed
    base_url="http://localhost:11434"  # adjust if your Ollama API is on a different port or host
)

# Create a simple prompt template
prompt = PromptTemplate(
    template="Answer the following question: {question}",
    input_variables=["question"]
)

# Set up an LLM chain using the prompt and LLM
chain = prompt | llm

# Run the chain with a sample question
question = "What is the capital of France?"
response = chain.invoke(question)

print(response)