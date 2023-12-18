# In the name of GOD

import redis

from config import settings

databases = {}
collections = {}


async def sess_db():
    redis_db = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=settings.REDIS_DATABASE, password=settings.REDIS_PASSWORD or None)
    return redis_db
