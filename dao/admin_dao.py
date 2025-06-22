from dao.base_dao import BaseDAO
from database.models import Admin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from database.models import Admin,User 


class AdminDao(BaseDAO[Admin]):
    model = Admin


    async def get_one_admin(self, session:AsyncSession, filters: list) -> Admin:   
        stmt = (
            select(Admin)
            .join(User, Admin.user_id == User.id)
            .options(joinedload(Admin.user))
        )
        if filters:
            stmt = stmt.where(*filters)
        result = await session.execute(stmt)
        return result.scalars().first()