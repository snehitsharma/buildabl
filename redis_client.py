import os
import redis.asyncio as redis

redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST") or "redis",
    port=int(os.environ.get("REDIS_PORT") or "6379"),
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)
