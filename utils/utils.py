import datetime
import os

def datetime_to_str(date:datetime.datetime):
    return datetime.datetime.strftime(date, "%Y-%m-%d %H:%M")

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
    return tg_id == int(os.getenv("ADMIN_ID"))

def get_channel_id():
    return os.getenv("TELEGRAM_CHANNEL_ID")

def get_admin_id():
    return os.getenv("ADMIN_ID")

