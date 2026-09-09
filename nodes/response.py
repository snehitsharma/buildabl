from state import State

def response(state: State) -> State:
    final = state["response"]
    return {"response": final}
