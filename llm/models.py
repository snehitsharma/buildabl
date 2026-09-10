import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_model():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=os.getenv("GROQ_API_KEY"),
    )


def call_model(message):
    return get_model().invoke(message)