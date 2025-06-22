from cache.cache import Cache
from dto.models import AdminDTO
from dao.admin_dao import AdminDao
from dto.admin_models import CreateAdmin
from database.models import Admin
from database.base import get_session, get_session_with_commit
from errors.errors import *

class AdminRepository:
    def __init__(self, cache:Cache):
        self.cache = cache
        self.admin_dao = AdminDao()

    async def add_admin(self, user_id:int, bot_id:int)->AdminDTO:
        async with get_session_with_commit() as session:
            admin = await self.admin_dao.add(session=session, values=CreateAdmin(user_id=user_id, bot_id=bot_id).model_dump(exclude_unset=True))
            if not admin:
                raise BookingError(error_code=ErrorCode.ERROR_CREATE_BOOKING, bot_id = bot_id, user_id = user_id)
            
            admin = await self.admin_dao.get_one_admin(session, [Admin.id == admin.id])
            if not admin:
                raise BookingError(error_code=ErrorCode.ADMIN_NOT_FOUND, bot_id = bot_id, user_id = user_id)
            
            admin_dto =  AdminDTO.model_validate(admin)

            await self.cache.put(bot_id, admin_dto)

            return admin_dto
            
    async def get_admin(self, bot_id:int)->AdminDTO:
        admin_dto = await self.find_admin(bot_id)
        if not admin_dto:
            raise BookingError(error_code=ErrorCode.ADMIN_NOT_FOUND, bot_id = bot_id)
        return admin_dto


    async def find_admin(self, bot_id:int)->AdminDTO:
        admin_dto = await self.cache.get(bot_id)
        if admin_dto:
            return admin_dto
        
        async with get_session() as session:
            admin = await self.admin_dao.get_one_admin(session, [Admin.bot_id == bot_id])
            if not admin:
                return None
            admin_dto =  AdminDTO.model_validate(admin)
            await self.cache.put(bot_id, admin_dto)
            return admin_dto
        

    async def remove_admin(self, user_id:int, bot_id:int)->AdminDTO:
        async with get_session_with_commit() as session:
            filters = [Admin.bot_id == bot_id, Admin.user_id == user_id]

            admin = await self.admin_dao.get_one_admin(session=session, filters=filters)
            if not admin:
                raise BookingError(error_code=ErrorCode.ADMIN_NOT_FOUND, bot_id = bot_id, user_id=user_id)

            result = await self.admin_dao.delete(session=session, filters=filters)
            if result != 1:
                raise BookingError(ErrorCode.ERROR_DELETE_ADMIN, user_id = user_id, bot_id = bot_id)
            
            await self.cache.remove(bot_id)
            
            return  AdminDTO.model_validate(admin)
    