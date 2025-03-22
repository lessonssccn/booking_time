from typing import Tuple
import datetime

def get_actual_date_range(days=30)->Tuple[datetime.date, datetime.date]:
        now = datetime.datetime.now()
        min_date = now.date()
        max_date = (now + datetime.timedelta(days=days)).date()
        return min_date, max_date

def get_limit_and_offset(items_per_page:int, page:int) -> Tuple[int, int]:
    limit = items_per_page
    offset = items_per_page * page
    return limit, offset