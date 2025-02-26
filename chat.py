from langchain_ollama import OllamaLLM
from langgraph.checkpoint.memory import MemorySaver
from app.src.graph_flow import Graph
from app.src.graph_src import generator_prompt_template
from app.src.graph_state import AgentState


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

        output = app.invoke({"messages": user_input}, config)
        output["messages"][-1].pretty_print()