import os
import json
import hashlib
import redis.asyncio as redis

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
CACHE_TTL_SECONDS = 60

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def build_cache_key(**params) -> str:
    raw = json.dumps(params, sort_keys=True, default=str)
    digest = hashlib.md5(raw.encode()).hexdigest()
    return f"listings:list:{digest}"

async def get_cached(key: str) -> dict | None:
    raw = await redis_client.get(key)
    return json.loads(raw) if raw else None

async def set_cached(key: str, value: dict, ttl: int = CACHE_TTL_SECONDS):
    await redis_client.set(key, json.dumps(value, default=str), ex=ttl)

async def invalidate_listings_cache():
    keys = await redis_client.keys("listings:list:*")
    if keys:
        await redis_client.delete(*keys)