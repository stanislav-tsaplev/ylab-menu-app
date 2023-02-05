from os import environ as env

from redis.asyncio import Redis

REDIS_HOST = env.get("REDIS_HOST", "localhost")
REDIS_PORT = int(env.get("REDIS_PORT", 6379))
REDIS_DB = int(env.get("REDIS_DB", 0))

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"


cache_engine: Redis = Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
)
