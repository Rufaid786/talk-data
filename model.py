from langchain_groq import ChatGroq

def create_model(api_key):
    return ChatGroq(
        model="openai/gpt-oss-120b", 
        api_key=api_key,
        temperature=0,
        max_retries=5)