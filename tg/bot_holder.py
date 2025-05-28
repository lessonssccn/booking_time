from telegram.ext import Application
from typing import Dict, List

class BotAppHolder:
    _apps:Dict[int, Application] = {}

    @classmethod
    def add_app(cls, app: Application) -> None:
        """Устанавливает экземпляр бота."""
        cls._apps[app.bot.id] = app

    @classmethod
    def get_app(cls, bot_id:int) -> Application:
        """Возвращает экземпляр бота по ид или None"""
        return cls._apps.get(bot_id,None)
    
    @classmethod
    def get_list_app(cls)->List[Application]:
        return list(cls._apps.values())