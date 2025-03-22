from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import datetime
from dao.timeslot_dao import TimeslotDao 
from dto.models import TimeSlotDTO
from database.models import TimeSlot
from dto.timeslot_models import CreateTimeslot, UpdateTimeslot
from database.base import get_session, get_session_with_commit
from errors.errors import *


class TimeslotRepository:
    def __init__(self):
        self.timeslot_dao = TimeslotDao()

    async def add_timeslot(self, date:datetime.date, time:datetime.time)->TimeSlotDTO:
        async with get_session_with_commit() as session:
            try:
                slot = await self.timeslot_dao.add(session, CreateTimeslot(date=date, time=time).model_dump(exclude_unset=True))
                return TimeSlotDTO.model_validate(slot)
            except:
                raise BookingError(ErrorCode.ERROR_CREATE_TIMESLOT, date=date, time=time)
            
    async def get_timeslot_by_id(self, timeslot_id)->TimeSlotDTO:
        async with get_session() as session:
            slot = await self.timeslot_dao.find_one(session, TimeSlot.id == timeslot_id)
            if slot:
                return TimeSlotDTO.model_validate(slot)
            raise BookingError(ErrorCode.TIMESLOT_NOT_FOUND, timeslot_id = timeslot_id)
        

    async def exist_timeslot(self, date:datetime.date, time:datetime.time) -> bool:
        async with get_session() as session:
            count = await self.timeslot_dao.count(session,[TimeSlot.date == date, TimeSlot.time == time])
            return count>0
    
    async def get_timeslot(self, date:datetime.date, time:datetime.time)->TimeSlotDTO:
        async with get_session() as session:
            slot = await self.timeslot_dao.find_one(session, [TimeSlot.date == date, TimeSlot.time == time])
            if slot:
                return TimeSlotDTO.model_validate(slot) 
            raise BookingError(ErrorCode.TIMESLOT_NOT_FOUND, date=date, time=time)
    
    async def get_list_by_date_range(self, min_date:datetime.date, max_date:datetime.date)->List[TimeSlotDTO]:
        async with get_session() as session:
            list_slot = await self.timeslot_dao.find_all(session, [TimeSlot.date >= min_date, TimeSlot.date <= max_date])
            return list(map(lambda slot: TimeSlotDTO.model_validate(slot), list_slot))
    
    async def update_timeslot(self, id:int, update_data: UpdateTimeslot)->bool:
        async with get_session_with_commit() as session:
            try:
                return await self.timeslot_dao.update(session,TimeSlot.id == id, update_data.model_dump(exclude_unset=True))
            except:
                return False
    
    async def get_list_timeslot_for_date_exlude(self, date:datetime.date, exclude_ids:List[int])->List[TimeSlotDTO]:
        async with get_session() as session:
            list_slot = await self.timeslot_dao.find_all(session, [TimeSlot.date == date, TimeSlot.id.not_in(exclude_ids), TimeSlot.hide==False])
            return list(map(lambda slot: TimeSlotDTO.model_validate(slot), list_slot))
        
    async def get_list_timeslot_by_date(self, date:datetime.date)->List[TimeSlotDTO]:
        async with get_session() as session:
            list_slot =  await self.timeslot_dao.find_all(session, TimeSlot.date == date)
            return list(map(lambda slot: TimeSlotDTO.model_validate(slot), list_slot))

    async def remove_timeslot(self, slot_id:int) -> TimeSlotDTO:
        async with get_session_with_commit() as session:
            filters = [TimeSlot.id == slot_id]

            slot = await self.timeslot_dao.find_one(session, filters)
            if not slot:
                raise BookingError(ErrorCode.TIMESLOT_NOT_FOUND, slot_id = slot_id)
            
            count = await self.timeslot_dao.delete(session, filters)
            if count != 1:
                raise BookingError(ErrorCode.ERROR_DELETE_TIMESLOT, slot_id = slot_id)
            
            return  TimeSlotDTO.model_validate(slot)
