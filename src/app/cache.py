from os import getenv

from redis.asyncio import Redis

REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(getenv("REDIS_PORT", 6379))
REDIS_DB = int(getenv("REDIS_DB", 0))


cache_engine: Redis = Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
)
