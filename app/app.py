from langchain_ollama import OllamaLLM
from langgraph.checkpoint.memory import MemorySaver
from src.graph_flow import Graph
from src.graph_src import generator_prompt_template
from src.graph_state import AgentState
import requests
from bs4 import BeautifulSoup

# Instantiate the Ollama LLM
llm = OllamaLLM(
    model="deepseek-r1:14b"  # e.g., "llama2" or whichever model you have installed
)

prompt_template = generator_prompt_template()

config = {"configurable": {"thread_id": "1",
                           "prompt_template":prompt_template,
                           "model":llm}
          }

graph = Graph()
memory = MemorySaver()

if __name__ == '__main__':
    app = graph.compile(memory)
    agentState = AgentState()
    
    while True:
        user_input = input("user: ")
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        # input_messages = user_input
        output = app.invoke({"messages": user_input}, config)
        

        output["messages"][-1].pretty_print()

        # data = {"input": user_input}

        # response = requests.post(url, json=data).json()

        # soup = BeautifulSoup(response["response"], 'html.parser')
        # pretty_html = soup.prettify()

        # print(pretty_html)