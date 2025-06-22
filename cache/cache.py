import asyncio

class Cache:
    def __init__(self):
        self._data = {}
        self._lock = asyncio.Lock()

    async def put(self, key,value)->bool:
        async with self._lock:
            self._data[key]= value
            return True
    
    async def remove(self, key)->bool:
        async with self._lock:
            if key in self._data:
                del self._data[key]
                return True
            else:
                return False
            
    async def get(self, key):
        async with self._lock:
            return self._data.get(key)
    
    async def clear(self)->bool:
        async with self._lock:
            self._data.clear()
            return True