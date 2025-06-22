from repositories.admin_repository import AdminRepository
from repositories.user_repository import UserRepository
from services.notifications_service import NotificationService
from dto.models import AdminDTO
from services.const_text import SUCCESS_ADD_ADMIN, SUCCESS_REMOVE_ADMIN
from utils.utils import get_msg_admin
from errors.errors import *


class AdminService:
    def __init__(self, user_repo:UserRepository, admin_repo:AdminRepository, notification_service :NotificationService):
        self.admin_repo = admin_repo
        self.user_repo = user_repo
        self.notification_service = notification_service

    async def add_admin(self, tg_id, bot_id)->AdminDTO:
        user = await self.user_repo.get_user_by_tg_id(tg_id)
        admin = await self.admin_repo.find_admin(bot_id)
        if admin:
            raise BookingError(ErrorCode.ADMIN_ALREADY_SET, bot_id = bot_id)
        admin = await self.admin_repo.add_admin(user.id, bot_id)
        msg = get_msg_admin(admin, SUCCESS_ADD_ADMIN)
        await self.notification_service.send_notification_to_channel(msg)
        await self.notification_service.send_message_to_admin(msg)
        return admin

    
    async def remove_admin(self, tg_id, bot_id)->AdminDTO:
        user = await self.user_repo.get_user_by_tg_id(tg_id)
        admin = await self.admin_repo.remove_admin(user.id, bot_id)
        msg = get_msg_admin(admin, SUCCESS_REMOVE_ADMIN)
        await self.notification_service.send_notification_to_channel(msg)
        await self.notification_service.send_message_to_admin(msg, admin_id=admin.user.tg_id)
        return admin
    

    async def is_admin(self, tg_id, bot_id)->bool:
        user = await self.user_repo.get_user_by_tg_id(tg_id)
        admin = await self.admin_repo.find_admin(bot_id)
        if not admin:
            return False
        return admin.user_id == user.id
    

    async def find_admin(self, bot_id)->AdminDTO:
        return await self.admin_repo.find_admin(bot_id)
