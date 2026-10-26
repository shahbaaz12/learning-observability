from langchain_groq import ChatGroq


MODEL_NAME = "openai/gpt-oss-20b"


def load_llm():
    return ChatGroq(
        model=MODEL_NAME,
        temperature=0,
    )
