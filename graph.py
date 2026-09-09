from langgraph.graph import StateGraph, START, END
from state import State
from nodes.generate import generate
from nodes.response import response


builder = StateGraph(State)

builder.add_node("generate", generate)
builder.add_node("response", response)

builder.add_edge(START, "generate")
builder.add_edge("generate", "response")
builder.add_edge("response", END)

graph = builder.compile()
