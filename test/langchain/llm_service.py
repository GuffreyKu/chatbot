from flask import Flask, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from .memory import InMemoryHistory


app = Flask(__name__)

# Instantiate the Ollama LLM
llm = OllamaLLM(
    model="deepseek-r1:14b"
    )

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an assistant who's good at {ability}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm

store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


chain_with_history = RunnableWithMessageHistory(
    chain,
    get_by_session_id,
    input_messages_key="question",
    history_messages_key="history",
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    print(store)
    # Get response from the conversation chain
    response = chain_with_history.invoke({"ability": "math", "question": user_input}, 
                                         config={"configurable": {"session_id": "foo"}})
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)