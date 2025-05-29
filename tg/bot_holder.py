from telegram.ext import Application
from typing import Dict, List
import asyncio

class BotAppHolder:
    _apps:Dict[int, Application] = {}
    _lock = asyncio.Lock()

    @classmethod
    async def add_app(cls, app: Application) -> None:
        """Устанавливает экземпляр бота"""
        async with cls._lock:
            cls._apps[app.bot.id] = app

    @classmethod
    async def get_app(cls, bot_id:int) -> Application:
        """Возвращает экземпляр бота по ид или None"""
        async with cls._lock:
            return cls._apps.get(bot_id, None)
    
    @classmethod
    async def get_list_app(cls)->List[Application]:
        """Возвращает список всех экземпляров бота"""
        async with cls._lock:
            return list(cls._apps.values())