from flask import Flask, request, jsonify
from langchain_ollama import OllamaLLM
from langgraph.checkpoint.memory import MemorySaver
from src.graph_flow import Graph
from src.graph_src import generator_prompt_template


app = Flask(__name__)

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
graph_flow = graph.compile(memory)

@app.route('/chat', methods=['POST'])
def chat():
    
    data = request.get_json()
    user_input = data.get("input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Get response from the conversation chain
    response = graph_flow.invoke({"messages": user_input}, config)
    return jsonify({"response": response["messages"][-1].content})

if __name__ == '__main__':
    app.run(debug=True, port=5000)