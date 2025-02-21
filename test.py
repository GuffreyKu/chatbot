import os
from dotenv import dotenv_values
from langchain_core.messages import HumanMessage, AIMessage

db_config = dotenv_values("config/.env")

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = db_config["OPENAI_API_KEY"]

from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4o-mini", model_provider="openai")

response = model.invoke(
  [
    HumanMessage(content="Hi! I'm Bob"),
    AIMessage(content="Hello Bob! How can I assist you today?"),
    HumanMessage(content="What's my name?"),
  ]
)


print(response)
