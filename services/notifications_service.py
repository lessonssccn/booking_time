from telegram.ext import Application 
from telegram.constants import ParseMode
from dto.models import UserDTO
from typing import List
from settings.settings import settings
from services.const_text import POSTFIX_NOTIFICATION_CHANNAL

class NotificationService:
    def __init__(self, app:Application):
        self.app = app
    
    async def send_message(self, chat_id: int, text: str, reply_markup=None, parse_mode = None) -> None:
        """Отправляет сообщение в указанный чат."""
        try:
            await self.app.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode = parse_mode)
        except Exception as e:
            try:
                error_msg = f"Notification error\nchat_id = {chat_id}\nerror = {e}"
                self.app.bot.send_message(chat_id = settings.admin_id, text=error_msg)
            except:
                print(f"Error send notification")

    async def send_message_to_users(self, list_user:List[UserDTO], text: str, reply_markup=None, parse_mode = None) -> None:
        for user in list_user:
            await self.send_message(user.tg_id, text, reply_markup=reply_markup, parse_mode=parse_mode)

    async def send_notification_to_channel(self, msg, tg_user = None) -> None:
        if tg_user:
            msg = POSTFIX_NOTIFICATION_CHANNAL.format(msg=msg, first_name = tg_user.first_name, username = tg_user.username)
        await self.send_message(settings.telegram_channel_id, msg)

    async def send_message_to_admin(self, msg, reply_markup=None) -> None:
        await self.send_message(settings.admin_id, msg, reply_markup)