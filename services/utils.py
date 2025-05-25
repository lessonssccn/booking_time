from typing import Tuple
import datetime
from dto.models import UserDTO
from dto.models import BookingDTO
from dto.models import TimeSlotDTO
from dto.models import DayDTO
from services.const_text import *
from utils.utils import *

def get_actual_date_range(days=30)->Tuple[datetime.date, datetime.date]:
        now = datetime.datetime.now()
        min_date = now.date()
        max_date = (now + datetime.timedelta(days=days)).date()
        return min_date, max_date

def get_limit_and_offset(items_per_page:int, page:int) -> Tuple[int, int]:
    limit = items_per_page
    offset = items_per_page * page
    return limit, offset

def get_user_info_as_txt(user:UserDTO)->str:
    date = datetime_to_str(user.created_at)
    return USER_INFO.format(name = user.first_name, username = user.username, tg_id = user.tg_id, user_id = user.id, date = date)

def get_success_msg_for_booking(booking: BookingDTO, action:str):
    date = datetime_to_str(booking.date)
    return action.format(date = date, name = booking.user.first_name, username = booking.user.username)

def get_success_msg_for_slot(slot:TimeSlotDTO, action:str):
    date = date_to_str(slot.date)
    time = time_to_str(slot.time)
    return action.format(date=date, time=time)

def get_copy_slot_result(date_src_start:datetime.date, date_src_end:datetime.date, date_des_start:datetime.date, date_des_end:datetime.date, count:int):
    date_src_start = date_to_str(date_src_start)
    date_src_end = date_to_str(date_src_end)
    date_des_start = date_to_str(date_des_start)
    date_des_end = date_to_str(date_des_end)
    return COPY_SCHEDULE_RESULT.format(date_src_start = date_src_start, date_src_end = date_src_end, date_des_start = date_des_start, date_des_end = date_des_end, count = count)

def get_success_msg_for_day(day:DayDTO, action:str):
    date = date_to_str(day.date)
    return action.format(date=date)