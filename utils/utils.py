import datetime
from settings.settings import settings
from typing import List
from dto.models import UserDTO, BookingDTO, TimeSlotDTO, DayDTO

def get_list_date(date_start:datetime.date, date_end:datetime.date)->List[datetime.date]:
    result = []
    delta = (date_end - date_start).days
    for i in range(delta + 1):
        current_date = date_start + datetime.timedelta(days=i)
        result.append(current_date)
    return result

def get_monday(date:datetime.date):
    monday = date - datetime.timedelta(days=date.weekday())
    return monday
    
def get_sunday(date:datetime.date):
    date = datetime.datetime(date.year, date.month, date.day)
    current_weekday = date.weekday()
    days_until_sunday = 6 - current_weekday
    return (date + datetime.timedelta(days=days_until_sunday)).date()

def date_to_str(date:datetime.date):
    return datetime.datetime.strftime(date, "%a, %d %B %Y")

def datetime_to_str(date:datetime.datetime):    
    return datetime.datetime.strftime(date, "%a %H:%M (%d %B %Y)")

def datetime_to_str_with_second(date:datetime.datetime):
    return datetime.datetime.strftime(date, "%a %H:%M:%S (%d %B %Y)")

def time_to_str(time:datetime.time):
    return time.strftime("%H:%M")

def time_to_str_with_second(time:datetime.time):
    return time.strftime("%H:%M:%S")

def conver_str_to_date(date:str):
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()

def conver_str_to_time(time:str):
    return datetime.datetime.strptime(time, "%H:%M:%S").time()

def is_admin(tg_id:int):
    return tg_id == settings.admin_id

def get_channel_id():
    return settings.telegram_channel_id

def get_admin_id():
    return settings.admin_id

def get_user_info_as_txt(user:UserDTO, tmpl:str)->str:
    date = datetime_to_str(user.created_at)
    return tmpl.format(name = user.first_name, username = user.username, tg_id = user.tg_id, user_id = user.id, date = date)

def get_msg_for_booking(booking: BookingDTO, tmpl:str):
    date = datetime_to_str(booking.date)
    return tmpl.format(date = date, name = booking.user.first_name, username = booking.user.username, tg_id = booking.user.tg_id, user_id = booking.user.id)

def get_msg_for_slot(slot:TimeSlotDTO, tmpl:str):
    date = date_to_str(slot.date)
    time = time_to_str(slot.time)
    return tmpl.format(date=date, time=time)

def get_msg_for_copy_slot(date_src_start:datetime.date, date_src_end:datetime.date, date_des_start:datetime.date, date_des_end:datetime.date, tmpl:str, count:int|None = None):
    date_src_start = date_to_str(date_src_start)
    date_src_end = date_to_str(date_src_end)
    date_des_start = date_to_str(date_des_start)
    date_des_end = date_to_str(date_des_end)
    return tmpl.format(date_src_start = date_src_start, date_src_end = date_src_end, date_des_start = date_des_start, date_des_end = date_des_end, count = count)

def get_msg_for_day(day:DayDTO, tmpl:str):
    date = date_to_str(day.date)
    return tmpl.format(date=date)