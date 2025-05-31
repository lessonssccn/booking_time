from telegram.ext import Application 
from dto.models import UserDTO
from typing import List, Tuple
from settings.settings import settings
from services.const_text import POSTFIX_NOTIFICATION_CHANNAL

class NotificationService:
    def __init__(self, app:Application):
        self.app = app
    
    async def send_message(self, chat_id: int, text: str, reply_markup=None, parse_mode = None) -> bool:
        """Отправляет сообщение в указанный чат."""
        try:
            await self.app.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode = parse_mode)
            return True
        except Exception as e:
            try:
                error_msg = f"Notification error\nchat_id = {chat_id}\nerror = {e}"
                self.app.bot.send_message(chat_id = settings.admin_id, text=error_msg)
            except:
                print(f"Error send notification")
            return False

    async def send_message_to_users(self, list_user:List[UserDTO], text: str, reply_markup=None, parse_mode = None) -> List[Tuple[UserDTO, bool]]:
        list_result = []
        for user in list_user:
            result = await self.send_message(user.tg_id, text, reply_markup=reply_markup, parse_mode=parse_mode)
            list_result.append((user, result))
        return list_result

    async def send_message_to_one_user(self, user: UserDTO, text: str, reply_markup=None, parse_mode = None) -> bool:
        return await self.send_message(user.tg_id, text, reply_markup=reply_markup, parse_mode=parse_mode)

    async def send_notification_to_channel(self, msg, tg_user = None) -> bool:
        if tg_user:
            msg = POSTFIX_NOTIFICATION_CHANNAL.format(msg=msg, first_name = tg_user.first_name, username = tg_user.username)
        return await self.send_message(settings.telegram_channel_id, msg)

    async def send_message_to_admin(self, msg, reply_markup=None) -> bool:
        return await self.send_message(settings.admin_id, msg, reply_markup)