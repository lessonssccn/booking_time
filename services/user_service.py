from repositories.user_repository import UserRepository
from dto.models import UserDTO
from dto.tg_models import CreateUserTG, UpdateUser
from services.notifications_service import NotificationService
from settings.settings import settings
from utils.utils import get_user_info_as_txt
from services.const_text import USER_INFO
from dto.user_models import UserPage
from settings.settings import settings
from services.utils import get_limit_and_offset
import math

class UserService:
    def __init__(self, user_repo:UserRepository, notification_service :NotificationService):
        self.user_repo = user_repo
        self.notification_service = notification_service
        self.page_size = settings.page_size

    async def get_or_create_user(self, tg_id:int, username:str|None=None, first_name:str|None=None, last_name:str|None=None)->UserDTO:
        user = await self.user_repo.find_user_by_tg_id(tg_id)
        if not user:
            user = await self.user_repo.add_tg_user(CreateUserTG(tg_id=tg_id, username=username, first_name=first_name, last_name=last_name))
            if settings.notification_create_new_user:
                await self.notification_service.send_notification_to_channel(get_user_info_as_txt(user, USER_INFO))
        return user
    
    async def get_user_by_id(self, user_id:int)->UserDTO:
        return await self.user_repo.get_user_by_id(user_id)
    

    async def get_user_by_tg_id(self, tg_id:int)->UserDTO:
        return await self.user_repo.get_user_by_tg_id(tg_id)
    
    async def get_list_user(self, page:int)->UserPage:
        limit, offset = get_limit_and_offset(self.page_size, page)
        list_user = await self.user_repo.get_list_user(limit, offset)
        return UserPage(items=list_user.list_items, total=list_user.total_count, page=page, total_page=math.ceil(list_user.total_count/self.page_size))
         
    async def update_user_reminde_inactive(self, tg_id:int, reminde:int) -> UserDTO:
        return await self.user_repo.update_user_by_tg_id(tg_id, UpdateUser(remind_inactive=reminde))
    
    async def update_user_reminde_before(self, tg_id:int, before:int) -> UserDTO:
        user = await self.user_repo.get_user_by_tg_id(tg_id)
        reminder_minutes_before = user.reminder_minutes_before
        
        if before in reminder_minutes_before:
            reminder_minutes_before.remove(before)
        else:
            reminder_minutes_before.append(before)
        
        return await self.user_repo.update_user_by_tg_id(tg_id, UpdateUser(reminder_minutes_before=reminder_minutes_before))