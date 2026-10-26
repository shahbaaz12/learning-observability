from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

repo_root = Path(__file__).resolve().parents[2]
load_dotenv(repo_root / ".env", override=True)


def get_model():
    return ChatGroq(model="openai/gpt-oss-20b")
