from langchain_ollama import OllamaLLM
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory

# 实例化 OllamaLLM，替换为你实际使用的模型名称和 base_url
llm = OllamaLLM(
    model="deepseek-r1:14b",           # 例如 "llama2"
)

# 使用 ConversationBufferMemory 来存储对话历史，注意 memory_key 要和默认 prompt 变量保持一致（例如 "history"）
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# 创建对话链，结合 LLM 与记忆对象
conversation = RunnableWithMessageHistory(llm=llm, memory=memory)

# 示例对话
response1 = conversation.predict(input="你好，今天过得怎么样？")
print("Bot:", response1)

response2 = conversation.predict(input="你能告诉我更多细节吗？")
print("Bot:", response2)