from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


# # Instantiate the Ollama LLM
# llm = OllamaLLM(
#     model="deepseek-r1:14b",  # e.g., "llama2" or whichever model you have installed
#     base_url="http://localhost:11434"  # adjust if your Ollama API is on a different port or host
# )

# # Create a simple prompt template
# prompt = PromptTemplate(
#     template="Answer the following question: {question}",
#     input_variables=["question"]
# )

# # Set up an LLM chain using the prompt and LLM
# chain = prompt | llm

# # Run the chain with a sample question
# question = "What is the capital of France?"
# response = chain.invoke(question)

# print(response)
# Write a test code that asserts the response from the LLM chain matches an expected output.
import unittest


class TestOllamaLLM(unittest.TestCase):
    def setUp(self):
        self.llm = OllamaLLM(
            model="deepseek-r1:14b",  # e.g., "llama2" or whichever model you have installed
            base_url="http://localhost:11434"  # adjust if your Ollama API is on a different port or host
        )
        self.prompt = PromptTemplate(
            template="Answer the following question: {question}",
            input_variables=["question"]
        )
        self.chain = self.prompt | self.llm

    def test_response(self):
        question = "What is the capital of France?"
        expected_output = "Paris."
        response = self.chain.invoke(question)
        print(response)
        self.assertIn(expected_output, response)


if __name__ == '__main__':
    unittest.main()