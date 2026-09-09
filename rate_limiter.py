# rate_limiter.py
from fastapi import Request, HTTPException
from redis_client import redis_client

async def rate_limit(request: Request, limit: int = 5, window: int = 60):
    ip = request.client.host
    key = f"ratelimit:ip:{ip}"
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, window)
    if count > limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again shortly.")