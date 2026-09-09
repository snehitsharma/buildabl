# cache.py
import hashlib, json
from redis_client import redis_client   # ← imports the shared client

async def get_cached_response(query: str):
    key = f"cache:{hashlib.sha256(query.encode()).hexdigest()}"
    cached = await redis_client.get(key)          # ← the actual Redis call happens HERE
    return json.loads(cached) if cached else None

async def set_cached_response(query: str, response: dict, ttl: int = 3600):
    key = f"cache:{hashlib.sha256(query.encode()).hexdigest()}"
    await redis_client.set(key, json.dumps(response), ex=ttl)   # ← and HERE