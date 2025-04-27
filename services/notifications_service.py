from telegram.ext import Application 
from telegram.constants import ParseMode

class NotificationService:
    def __init__(self, app:Application):
        self.app = app
    
    async def send_message(self, chat_id: int, text: str, reply_markup=None, parse_mode = None) -> None:
        """Отправляет сообщение в указанный чат."""
        await self.app.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode = parse_mode)