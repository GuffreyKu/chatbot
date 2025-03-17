from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from PROMPT import AGENT_PROMPT
from tools import tools


# Instantiate the Ollama LLM
llm = ChatOllama(
    model="qwen2",
    temperature=0
)

agent_executor = create_react_agent(llm, tools, state_modifier=AGENT_PROMPT)

if __name__ == '__main__':
    while True:
        user_input = input("user : ")
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        inputs = {"messages": [("user", user_input)]}

        for s in agent_executor.stream(inputs, stream_mode="values"):

            message = s["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()