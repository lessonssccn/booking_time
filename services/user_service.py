from repositories.user_repository import UserRepository
from dto.models import UserDTO
from dto.tg_models import CreateUserTG

class UserService:
    def __init__(self, user_repo:UserRepository):
        self.user_repo = user_repo

    async def get_or_create_user(self, tg_id:int, username:str|None=None, first_name:str|None=None, last_name:str|None=None)->UserDTO:
        user = await self.user_repo.find_user_by_tg_id(tg_id)
        if not user:
            user = await self.user_repo.add_tg_user(CreateUserTG(tg_id=tg_id, username=username, first_name=first_name, last_name=last_name))
        return user