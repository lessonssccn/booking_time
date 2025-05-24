from typing import Tuple
import datetime
from dto.models import UserDTO
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