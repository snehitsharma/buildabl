from state import State
from models import call_model

SYSTEM_PROMPT = "You are a helpful assistant. Answer the user's query in a concise and informative manner."


def generate(state: State) -> State:
    query = state["query"]
    message = [
        ("system", SYSTEM_PROMPT),
        ("human", query),
    ]
    result = call_model(message)
    return {"response": result.content}
