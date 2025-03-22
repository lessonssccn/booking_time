from dao.day_dao import DayDao 
from database.models import Day
from dto.day_models import DayLock, CreateDay
from dto.models import DayDTO
import datetime
from typing import List
from database.base import get_session, get_session_with_commit

class DayRepository:
    def __init__(self):
        self.day_dao = DayDao()

    async def get_day_by_date(self, date:datetime.date) -> DayDTO:
        async with get_session() as session:
            day = await self.day_dao.find_one(session, Day.date == date)
            if day:
                return DayDTO.model_validate(day)
            return None
    
    async def update_lock(self, day_id:int, lock:bool) -> bool:
        async with get_session_with_commit() as session:
            try:
                update_row = await self.day_dao.update(session, Day.id == day_id, DayLock(lock=lock).model_dump(exclude_unset=True))
                return update_row!=0
            except:
                return False
    
    async def add_lock_day(self, date:datetime.date) -> DayDTO:
        async with get_session_with_commit() as session:
            try:
                day = await self.day_dao.add(session, CreateDay(date=date, lock=True).model_dump(exclude_unset=True))
                if day == None:
                    return None
                return DayDTO.model_validate(day)
            except:
                return None

    
    async def get_list_lock_days(self, min_date:datetime.date, max_date:datetime.date)->List[DayDTO]:
        async with get_session() as session:
            list_day = await self.day_dao.find_all(session, [Day.date>=min_date, Day.date<=max_date, Day.lock==True])
            return list(map(lambda day: DayDTO.model_validate(day), list_day))

        