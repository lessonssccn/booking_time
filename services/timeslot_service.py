import datetime
from repositories.timeslot_repository import TimeslotRepository
from repositories.user_repository import UserRepository
from repositories.day_repository import DayRepository
from repositories.booking_repository import BookingRepository
from datetime import date, time
from dto.timeslot_models import ActualTimeslots
from dto.models import TimeSlotDTO
from typing import List, Tuple
from utils.booking_status import get_locked_status
from services.utils import get_actual_date_range
from utils.utils import get_list_date
from errors.errors import *
from dto.timeslot_models import UpdateTimeslot
from settings.settings import settings
from services.notifications_service import NotificationService
from utils.utils import get_msg_for_copy_slot, get_msg_for_slot
from services.const_text import *

class TimeslotService:
    def __init__(self, timeslot_repo:TimeslotRepository, day_repo:DayRepository, booking_repo:BookingRepository, user_repo:UserRepository, notification:NotificationService):
        self.timeslot_repo = timeslot_repo
        self.day_repo = day_repo
        self.booking_repo = booking_repo
        self.user_repo = user_repo
        self.days = settings.open_windows
        self.notification = notification

    async def get_timeslot_by_id(self, timeslot_id:int) -> TimeSlotDTO:
        return await self.timeslot_repo.get_timeslot_by_id(timeslot_id)
        
    async def get_list_timeslot_date_range(self, min_date:date, max_date:date)->List[TimeSlotDTO]:
        return await self.timeslot_repo.get_list_by_date_range(min_date, max_date)
    
    async def get_list_timeslot_by_date(self, date:date) -> List[TimeSlotDTO]:
        return await self.timeslot_repo.get_list_timeslot_by_date(date)
    
    async def get_list_timeslot_for_tg_user(self, date:date, tg_id:int) -> List[TimeSlotDTO]:
        user = await self.user_repo.get_user_by_tg_id(tg_id)
        list_booking = await self.booking_repo.get_list_booking_for_user(date, user.id, get_locked_status())
        return await self.timeslot_repo.get_list_timeslot_for_date_exlude(date, list(map(lambda booking: booking.time_slot_id, list_booking)))
    
    async def get_actual_timeslots(self) -> ActualTimeslots:
        min_date, max_date = get_actual_date_range(self.days)
        return ActualTimeslots(
            min_date = min_date,
            max_date = max_date,
            list_timeslot = await self.get_list_timeslot_date_range(min_date, max_date),
            list_locked_day= await self.day_repo.get_list_lock_days(min_date, max_date)
        )

    async def add_timeslot(self, date:datetime.date, time:datetime.time) -> TimeSlotDTO:
        if await self.timeslot_repo.exist_timeslot(date, time):
            raise BookingError(ErrorCode.TIMESLOT_EXIST, date=date, time=time)
        
        slot = await self.timeslot_repo.add_timeslot(date, time)

        await self.notification.send_notification_to_channel(get_msg_for_slot(slot, SUCCESS_TIMESLOT_CREATED)) 

        return slot
    
    async def remove_timeslot(self, slot_id:int) -> TimeSlotDTO:
        slot =  await self.timeslot_repo.remove_timeslot(slot_id)

        await self.notification.send_notification_to_channel(get_msg_for_slot(slot, SUCCESS_TIMESLOT_REMOVED)) 

        return slot
    
    async def lock_timeslot(self, slot_id:int) -> TimeSlotDTO:
        slot = await self.timeslot_repo.get_timeslot_by_id(slot_id)
        slot.lock = not slot.lock
        update_data = UpdateTimeslot(lock = slot.lock)
        if not await self.timeslot_repo.update_timeslot(slot_id, update_data):
            raise BookingError(ErrorCode.ERROR_UPDATE_TIMESLOT, timeslot_id = slot_id, **update_data.model_dump(exclude_unset=True))
        
        await self.notification.send_notification_to_channel(get_msg_for_slot(slot, SUCCESS_TIMESLOT_LOCKED if slot.lock else SUCCESS_TIMESLOT_UNLOCKED)) 
        
        return slot
    
    async def hide_timeslot(self, slot_id:int) -> TimeSlotDTO:
        slot = await self.timeslot_repo.get_timeslot_by_id(slot_id)
        slot.hide = not slot.hide
        update_data = UpdateTimeslot(hide = slot.hide)
        if not await self.timeslot_repo.update_timeslot(slot_id, update_data):
            raise BookingError(ErrorCode.ERROR_UPDATE_TIMESLOT, timeslot_id = slot_id, **update_data.model_dump(exclude_unset=True))
        
        await self.notification.send_notification_to_channel(get_msg_for_slot(slot, SUCCESS_TIMESLOT_HIDDEN if slot.hide else SUCCESS_TIMESLOT_SHOW)) 
       
        return slot
    
    def copy_slots(self, list_slot:List[TimeSlotDTO], list_date:List[datetime.date]) -> List[Tuple[datetime.date, datetime.time]]:
        list_new_slot = []
        date_dict = dict(zip(map(lambda d: d.weekday(), list_date),list_date))

        for slot in list_slot:
            weekday = slot.date.weekday()
            date = date_dict.get(weekday, None)
            if date:
                list_new_slot.append((date, slot.time))

        return list_new_slot

    async def copy_range(self, date_src_start:datetime.date, date_src_end:datetime.date, date_des_start:datetime.date, date_des_end:datetime.date) -> int:
        list_slot = await self.get_list_timeslot_date_range(date_src_start, date_src_end)
        list_new_slot = self.copy_slots(list_slot, get_list_date(date_des_start, date_des_end))
        count = await self.timeslot_repo.try_add_list_timeslot(list_new_slot)

        await self.notification.send_notification_to_channel(get_msg_for_copy_slot(date_src_start,date_src_end,date_des_start,date_des_end, COPY_SCHEDULE_RESULT, count))

        return count

