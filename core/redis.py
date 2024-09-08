import redis.asyncio as aio_redis
from core.config import config

redis = aio_redis.from_url(url=f"redis://{config.REDIS_HOST}")
