import os
import json
import redis.asyncio as redis

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def auction_channel(listing_id: int) -> str:
    return f"auction:{listing_id}"

async def publish_bid(listing_id: int, message: dict):
    await redis_client.publish(auction_channel(listing_id), json.dumps(message))