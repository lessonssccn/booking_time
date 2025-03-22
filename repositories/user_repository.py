from dao.user_dao import UserDao 
from dto.models import UserDTO
from dto.tg_models import CreateUserTG
from database.models import User
from database.base import get_session, get_session_with_commit
from errors.errors import *

class UserRepository:
    def __init__(self):
        self.user_dao = UserDao()
    
    async def get_user_by_tg_id(self, tg_id:int)->UserDTO:
        async with get_session() as session:
            user = await self.user_dao.find_one(session, User.tg_id == tg_id)
            if not user:
                raise BookingError(error_code=ErrorCode.USER_NOT_FOUND, tg_id = tg_id)
            return UserDTO.model_validate(user)
            
    async def find_user_by_tg_id(self, tg_id:int)->UserDTO:
        async with get_session() as session:
            user = await self.user_dao.find_one(session, User.tg_id == tg_id)
            if user:
                return UserDTO.model_validate(user)
    
    async def add_tg_user(self, new_user:CreateUserTG) -> UserDTO:
        async with get_session_with_commit() as session:
            try:
                user = await self.user_dao.add(session, new_user.model_dump(exclude_unset=True))
                if user:
                    return UserDTO.model_validate(user)
            except:
                return None
