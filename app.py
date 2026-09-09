from fastapi import FastAPI, Depends
from pydantic import BaseModel

from graph import graph
from rate_limiter import rate_limit
from cache import get_cached_response, set_cached_response

app = FastAPI(title="Buildable Chatbot")


class QueryRequest(BaseModel):
    query: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat", dependencies=[Depends(rate_limit)])
async def chat(payload: QueryRequest):
    if cached := await get_cached_response(payload.query):
        return cached

    result = graph.invoke({"query": payload.query})
    response = {"response": result["response"]}
    await set_cached_response(payload.query, response)
    return response