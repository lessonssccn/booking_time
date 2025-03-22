from repositories.day_repository import DayRepository
from dto.models import DayDTO
from typing import List
import datetime
from errors.errors import *

class DayService:
    def __init__(self, day_repo:DayRepository):
        self.day_repo = day_repo

    async def lock_day(self, date:datetime.date)->DayDTO:
        day = await self.day_repo.get_day_by_date(date)
        if day:
            day.lock = not day.lock
            update_result = await self.day_repo.update_lock(day.id, day.lock)
            if not update_result:
                raise BookingError(error_code=ErrorCode.ERROR_UPDATE_DAY, **day.model_dump(exclude_unset=True))
        else:
            day = await self.day_repo.add_lock_day(date)
            if not day:
                raise BookingError(error_code=ErrorCode.ERROR_ADD_DAY, date = date)
        return day
    
    async def get_list_lock_days(self, min_date:datetime.date, max_date:datetime.date)->List[DayDTO]:
        return await self.day_repo.get_list_lock_days(min_date, max_date)
    