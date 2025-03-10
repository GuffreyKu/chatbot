from PIL import Image
from langchain_ollama import OllamaLLM, ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from app.src.graph_flow import Graph
from app.src.graph_src import generator_prompt_template
from app.src.graph_state import AgentState
from app.src.graph_tools import tools
from app.src.PROMPT import AGENT_PROMPT

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)
llm = create_react_agent(llm, tools, state_modifier=AGENT_PROMPT)

prompt_template = generator_prompt_template()

config = {"configurable": {"thread_id": "1",
                           "prompt_template":prompt_template,
                           "model":llm}
                           }

graph = Graph()
memory = MemorySaver()

if __name__ == '__main__':
    app = graph.compile(memory)
    app.get_graph().draw_mermaid_png(output_file_path="graph.png")

    # while True:
    #     user_input = input("user: ")
        
    #     if user_input.lower() in ["quit", "exit", "q"]:
    #         print("Goodbye!")
    #         break

    #     output = app.invoke({"messages": user_input}, config)
    #     output["messages"][-1].pretty_print()
    #  "Summarize the key points of the document, path is /Users/guffrey/chatbot/pdf/Evo2.pdf"
    for chunk in app.stream(
        {"messages": [("user", "Summarize the key points of the document, path is /Users/guffrey/chatbot/pdf/Evo2.pdf")]},
        stream_mode="values",
        config=config):
        chunk["messages"][-1].pretty_print()