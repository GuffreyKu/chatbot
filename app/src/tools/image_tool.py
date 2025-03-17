from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from ..graph_src import image_prompt
from ..utils import convert_to_base64


@tool(parse_docstring=True)
def image_model(image_path:str, question:str):
    """
    This tool processes an image and answers questions using a vision-language model.
    
    Args:
        image_path: The path to the image file. Example:
                    "path/to/image.jpg"
        question: The user's question about the image. Example:
                  "What is in the image?"
    
    Returns:
        str: The generated response from the model.
    """
    if not image_path or not question:
        raise ValueError("Both 'image_path' and 'question' must be provided.")

    image_base64 = convert_to_base64(image_path)
    llm = ChatOllama(model="llama3.2-vision:11b")

    chain = image_prompt | llm 

    result = chain.invoke({"text": question, "image": image_base64})
    return result.content