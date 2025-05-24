from repositories.user_repository import UserRepository
from dto.models import UserDTO
from dto.tg_models import CreateUserTG, UpdateUser

class UserService:
    def __init__(self, user_repo:UserRepository):
        self.user_repo = user_repo

    async def get_or_create_user(self, tg_id:int, username:str|None=None, first_name:str|None=None, last_name:str|None=None)->UserDTO:
        user = await self.user_repo.find_user_by_tg_id(tg_id)
        if not user:
            user = await self.user_repo.add_tg_user(CreateUserTG(tg_id=tg_id, username=username, first_name=first_name, last_name=last_name))
        return user
    
    async def get_user_by_tg_id(self, tg_id:int)->UserDTO:
        return await self.user_repo.get_user_by_tg_id(tg_id)
    
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