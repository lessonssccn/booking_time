from dao.base_dao import BaseDAO
from database.models import Booking, User, TimeSlot
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from sqlalchemy import select

class BookingDao(BaseDAO[Booking]):
    model = Booking

    async def get_one_booking(self, session:AsyncSession, filters: list) -> Booking:   
        stmt = (
            select(Booking)
            .join(User, Booking.user_id == User.id)
            .join(TimeSlot, Booking.time_slot_id == TimeSlot.id)
            .options(joinedload(Booking.time_slot))
            .options(joinedload(Booking.user))
        )
        if filters:
            stmt = stmt.where(*filters)
        result = await session.execute(stmt)
        return result.scalars().first()
        
    
    async def get_count_booking(self, session:AsyncSession, filters: list)->int:
        stmt_total = (select(func.count(Booking.id))
                .join(User, Booking.user_id == User.id)
                .join(TimeSlot, Booking.time_slot_id == TimeSlot.id)
                .where(*filters))
        total_result = await session.execute(stmt_total)
        return total_result.scalar()
    
    async def get_list_booking(self, session:AsyncSession, filters: list, limit:int|None=None, offset:int|None=None) -> List[Booking]:
        stmt = (select(Booking)
            .join(User, Booking.user_id == User.id)
            .join(TimeSlot, Booking.time_slot_id == TimeSlot.id)
            .options(joinedload(Booking.time_slot))
            .options(joinedload(Booking.user))
            .where(*filters)
            .order_by(Booking.date))
        if limit!=None:
            stmt = stmt.limit(limit)
        if offset!=None:
            stmt = stmt.offset(offset)
        
        result = await session.execute(stmt)
        return result.scalars().all() 
        
