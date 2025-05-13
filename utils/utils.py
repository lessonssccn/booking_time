import datetime
from settings.settings import settings
from typing import List

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
    return datetime.datetime.strftime(date, "%a (%d %B %Y)")

def datetime_to_str(date:datetime.datetime):
    
    return datetime.datetime.strftime(date, "%a %H:%M (%d %B %Y)")
    # return datetime.datetime.strftime(date, "%Y-%m-%d %H:%M")

def datetime_to_str_with_second(date:datetime.datetime):
    return datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")

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

