from dotenv import load_dotenv
load_dotenv()
import os
import json
from fastapi.encoders import jsonable_encoder
import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise RuntimeError("REDIS_URL is not set in environment variables.")

redis_client = None  # Global singleton

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client

async def cache_subscription(subscription: dict):
    r = await get_redis()
    safe_subscription = jsonable_encoder(subscription)
    await r.set(f"subscription:{subscription['id']}", json.dumps(safe_subscription), ex=3600)  # 1 hour TTL

async def get_cached_subscription(subscription_id: int):
    r = await get_redis()
    data = await r.get(f"subscription:{subscription_id}")
    if data:
        return json.loads(data)
    return None
