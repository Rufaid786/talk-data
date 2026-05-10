from langchain_google_genai import ChatGoogleGenerativeAI

def create_model(api_key):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0,
    )