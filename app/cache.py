<<<<<<< HEAD
from dotenv import load_dotenv
load_dotenv()
from fastapi.encoders import jsonable_encoder
import json
import os
import redis.asyncio as redis
import json

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise RuntimeError("REDIS_URL is not set in environment variables.")

redis_client = redis.Redis = None  

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client

async def cache_subscription(subscription: dict):
    r = await get_redis()
    safe_subscription = jsonable_encoder(subscription)
    await r.set(f"subscription:{subscription['id']}", json.dumps(safe_subscription), ex=3600)

async def get_cached_subscription(subscription_id: int):
=======
import aioredis
import json
from app.config import REDIS_URL

redis = None

async def get_redis():
    global redis
    if not redis:
        redis = await aioredis.from_url(REDIS_URL)
    return redis

async def cache_subscription(subscription: dict):
    r = await get_redis()
    await r.set(f"subscription:{subscription['id']}", json.dumps(subscription), ex=3600)  # 1 hour TTL

async def get_cached_subscription(subscription_id: str):
>>>>>>> 65cd0d2 (Initial Commit)
    r = await get_redis()
    data = await r.get(f"subscription:{subscription_id}")
    if data:
        return json.loads(data)
    return None

async def invalidate_subscription_cache(subscription_id: str):
    r = await get_redis()
    await r.delete(f"subscription:{subscription_id}")
<<<<<<< HEAD
   
=======
>>>>>>> 65cd0d2 (Initial Commit)
