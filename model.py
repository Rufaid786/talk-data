from langchain_groq import ChatGroq

def create_model(api_key):
     return ChatGroq(
        model="qwen/qwen3-32b", 
        api_key=api_key,
        temperature=0,
    )