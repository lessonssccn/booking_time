import datetime
from repositories.booking_repository import BookingRepository
from repositories.user_repository import UserRepository
from repositories.timeslot_repository import TimeslotRepository
from repositories.day_repository import DayRepository
from services.booking_reminder_service import BookingReminderService
from services.notifications_service import NotificationService
from dto.booking_models import BookingPage
from dto.models import BookingDTO, UserDTO
from utils.booking_status import get_locked_status, get_actual_status, get_list_status_by_type, get_canceled_status, can_update_status, get_admin_confirm_status, get_admin_reject_status, get_active_user_status
from errors.errors import *
from services.utils import get_limit_and_offset, get_actual_date_range
import math
from typing import List
from settings.settings import settings
from utils.utils import get_msg_for_booking
from tg.keyboards.keyboards import short_admin_booking_keyboard
from services.const_text import *

class BookingService:
    def __init__(self, booking_repo:BookingRepository, timeslot_repo:TimeslotRepository, user_repo:UserRepository, day_repo:DayRepository, reminder: BookingReminderService, notification: NotificationService):
        self.booking_repo = booking_repo
        self.timeslot_repo = timeslot_repo
        self.user_repo = user_repo
        self.day_repo = day_repo
        self.reminder = reminder
        self.notification = notification
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

    async def get_list_booking_prevday(self, booking_type:str, page:int) -> BookingPage:
        today = datetime.datetime.now().date()
        yesterday = today - datetime.timedelta(days=1) 
        return await self.get_list_booking_by_date(yesterday, booking_type, page)

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

        notification_msg = get_msg_for_booking(booking, SUCCESS_BOOKING_MSG)
        await self.notification.send_notification_to_channel(notification_msg)
        await self.notification.send_message_to_admin(notification_msg, short_admin_booking_keyboard(booking.id))

        return booking
    
    async def cancel_booking(self, booking_id:int, tg_id:int|None=None, is_admin:bool=False)->BookingDTO:
        if tg_id!=None and not is_admin:
            user = await self.user_repo.get_user_by_tg_id(tg_id)
            result = await self.booking_repo.cancel_booking(booking_id, user.id, get_canceled_status(is_admin))
        else:
            result = await self.booking_repo.cancel_booking(booking_id, None, get_canceled_status(is_admin))

        if result:
            await self.reminder.remove_booking(await self.get_booking_by_id(booking_id))
            await self.notification.send_notification_to_channel(get_msg_for_booking(result, SUCCESS_UNBOOKING_ADMIN_MSG if is_admin else SUCCESS_UNBOOKING_MSG ))
            if is_admin:
                await self.notification.send_message_to_one_user(result.user, get_msg_for_booking(result, SUCCESS_UNBOOKING_ADMIN_MSG_FOR_USER))
            
        return result

    async def cancel_bookings_day(self, date:datetime.date) -> List[BookingDTO]: 
        list_booking = await self.booking_repo.get_list_booking(date, get_actual_status())
        result = []
        for booking in list_booking.list_items:
            result.append(await self.cancel_booking(booking.id, None, True))
        return result
    
    async def update_status_booking(self, booking_id:int, new_status:str) -> BookingDTO:
        booking = await self.booking_repo.get_booking_by_id(booking_id)
        if not (booking and can_update_status(booking.status)):
            raise BookingError(error_code=ErrorCode.ERROR_ADMIN_MATCH_BOOKING, booking_id = booking_id, new_status = new_status)

        result = await self.booking_repo.update_staust_booking(booking_id, new_status)
        if not result:
            raise BookingError(error_code=ErrorCode.ERROR_ADMIN_UPDATE_BOOKING, booking_id = booking_id, new_status = new_status) 
     
        return await self.booking_repo.get_booking_by_id(booking_id)
    
    async def confirm_booking(self, booking_id:int) -> BookingDTO:
        booking = await self.update_status_booking(booking_id, get_admin_confirm_status())
        
        await self.reminder.add_booking(booking)

        await self.notification.send_notification_to_channel(get_msg_for_booking(booking, SUCCESS_CONFIRM_BOOKING_MSG))
        await self.notification.send_message_to_one_user(booking.user, get_msg_for_booking(booking, SUCCESS_CONFIRM_BOOKING_MSG_FOR_USER))

        return booking

    
    async def reject_booking(self, booking_id:int) -> bool:
        booking = await self.update_status_booking(booking_id, get_admin_reject_status())

        await self.notification.send_notification_to_channel(get_msg_for_booking(booking, SUCCESS_REJECT_BOOKING_MSG))
        await self.notification.send_message_to_one_user(booking.user, get_msg_for_booking(booking, SUCCESS_REJECT_BOOKING_MSG_FOR_USER))

        return booking

    async def get_inactive_users_missing_future_bookings(self)->List[UserDTO]:
        now = datetime.datetime.now()
        future = (now + datetime.timedelta(days=settings.day_before_future_booking)).date()
        before = (now - datetime.timedelta(days=settings.day_after_last_active)).date()
        yesterday = ((now - datetime.timedelta(days=1)).date()) 

        return await self.booking_repo.find_reminde_users_with_appointments_in_period_a_but_not_in_b(before, yesterday, get_active_user_status(), now.date(), future, get_actual_status())