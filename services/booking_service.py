import datetime
from repositories.booking_repository import BookingRepository
from repositories.user_repository import UserRepository
from repositories.timeslot_repository import TimeslotRepository
from repositories.day_repository import DayRepository
from dto.booking_models import BookingPage
from dto.models import BookingDTO
from utils.booking_status import get_locked_status, get_actual_status, get_list_status_by_type, get_canceled_status, can_update_status, get_admin_confirm_status, get_admin_reject_status
from errors.errors import *
from services.utils import get_limit_and_offset, get_actual_date_range
import math
from typing import List

class BookingService:
    def __init__(self, booking_repo:BookingRepository, timeslot_repo:TimeslotRepository, user_repo:UserRepository, day_repo:DayRepository):
        self.booking_repo = booking_repo
        self.timeslot_repo = timeslot_repo
        self.user_repo = user_repo
        self.day_repo = day_repo
        self.page_size = 10
        self.days = 30


    async def get_booking_by_id(self, booking_id:int) -> BookingDTO:
        return await self.booking_repo.get_booking_by_id(booking_id)

    async def get_booking(self, booking_id:int, tg_id:int) -> BookingDTO:
        user = await self.user_repo.get_user_by_tg_id(tg_id)
        return await self.booking_repo.get_booking(booking_id, user.id)
    
    async def get_list_booking_by_date(self, date:datetime.date, booking_type:str, page:int) -> BookingPage:
        list_status = get_list_status_by_type(booking_type)
        limit, offset = get_limit_and_offset(self.page_size, page)
        list_booking = await self.booking_repo.get_list_booking(date, list_status, limit, offset)
        return BookingPage(items=list_booking.list_items, total=list_booking.total_count, page=page, total_page=math.ceil(list_booking.total_count/self.page_size))


    async def get_list_booking_curday(self, booking_type:str, page:int) -> BookingPage:
        today = datetime.datetime.now().date()
        return await self.get_list_booking_by_date(today, booking_type, page)
    
    async def get_list_booking_nextday(self, booking_type:str, page:int) -> BookingPage:
        today = datetime.datetime.now().date()
        tomorrow = today + datetime.timedelta(days=1) 
        return await self.get_list_booking_by_date(tomorrow, booking_type, page)

    async def get_all_actual_booking(self, booking_type:str, page:int) -> BookingPage:
        list_status = get_list_status_by_type(booking_type)
        limit, offset = get_limit_and_offset(self.page_size, page)
        min_date,max_date = get_actual_date_range(self.days)
        list_booking = await self.booking_repo.get_all_booking_by_date_range(list_status, min_date, max_date, limit, offset)
        return BookingPage(items=list_booking.list_items, total=list_booking.total_count, page=page, total_page=math.ceil(list_booking.total_count/self.page_size))

    async def get_list_actual_booking(self, tg_id:int, booking_type:str, page:int) -> BookingPage:
        user = await self.user_repo.get_user_by_tg_id(tg_id)
        list_status = get_list_status_by_type(booking_type)
        limit, offset = get_limit_and_offset(self.page_size, page)
        min_date,max_date = get_actual_date_range(self.days)
        list_booking = await self.booking_repo.get_list_booking_for_user_by_date_range(user.id, list_status, min_date, max_date, limit, offset)
        return BookingPage(items=list_booking.list_items, total=list_booking.total_count, page=page, total_page=math.ceil(list_booking.total_count/self.page_size))


    async def booking(self, timslot_id:int, tg_id:int) -> BookingDTO:
        if await self.booking_repo.exsist_booking(timslot_id, get_locked_status()):
            raise BookingError(error_code=ErrorCode.TIMESLOT_OCCUPIED, timslot_id=timslot_id)

        user = await self.user_repo.get_user_by_tg_id(tg_id)
        
        if await self.booking_repo.exsist_booking_for_user(user.id, timslot_id, get_actual_status()):
            raise BookingError(error_code=ErrorCode.TIMESLOT_OCCUPIED_CURRENT_USER, user_id = user.id, tg_id = tg_id, timslot_id = timslot_id)
        
        booking = await self.booking_repo.add_new_booking(timslot_id, user.id)
        return booking
    
    async def cancel_booking(self, booking_id:int, tg_id:int|None=None, is_admin:bool=False)->BookingDTO:
        if tg_id!=None and not is_admin:
            user = await self.user_repo.get_user_by_tg_id(tg_id)
            return await self.booking_repo.cancel_booking(booking_id, user.id, get_canceled_status(is_admin))
        else:
            return await self.booking_repo.cancel_booking(booking_id, None, get_canceled_status(is_admin))

    async def cancel_bookings_day(self, date:datetime.date) -> List[BookingDTO]: 
        list_booking = await self.booking_repo.get_list_booking(date, get_actual_status())
        result = []
        for booking in list_booking.list_items:
            result.append(await self.cancel_booking(booking.id, None, True))
        return result
    
    async def update_status_booking(self, booking_id:int, new_status:str) -> bool:
        booking = await self.booking_repo.get_booking_by_id(booking_id)
        if not can_update_status(booking.status):
            raise MatchBookingError(booking_id=booking_id)
        return await self.booking_repo.update_staust_booking(booking_id, new_status)
    
    async def confirm_booking(self, booking_id:int) -> bool:
        return await self.update_status_booking(booking_id, get_admin_confirm_status())
    
    async def reject_booking(self, booking_id:int) -> bool:
        return await self.update_status_booking(booking_id, get_admin_reject_status())

    
    