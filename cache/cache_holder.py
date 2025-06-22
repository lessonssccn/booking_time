from cache.cache import Cache
import asyncio


class CacheHolder:
    _admin_cache:Cache = None
    _channel_cache:Cache = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_admin_cache(cls):
        async with cls._lock:
            if not cls._admin_cache:
                cls._admin_cache = Cache()
            return cls._admin_cache
    

    @classmethod
    async def get_channel_cache(cls):
        async with cls._lock:
            if not cls._channel_cache:
                cls._channel_cache = Cache()
            return cls._channel_cache
