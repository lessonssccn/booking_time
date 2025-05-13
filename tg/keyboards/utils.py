from tg.keyboards.kb_calendar import DateAttribute, MarkerPair
from dto.models import DayDTO, TimeSlotDTO
from typing import List, Tuple
from tg.keyboards.kb_text import *
from tg.states.states import State
from utils.utils import get_monday, get_sunday, get_list_date
import datetime

def lock_day_to_date_attribute(day:DayDTO, is_admin:False):
    if is_admin:
        return DateAttribute(date=day.date, marker_pair=MarkerPair(left_symbol="❌"))
    else:
        return DateAttribute(date=day.date, symbol="❌", is_disabled = True, callback_data=str(State.IGNORE))

def timeslot_to_date_attribute(slot:TimeSlotDTO):
    return DateAttribute(date=slot.date, marker_pair=MarkerPair(left_symbol="🚩"))

def make_list_date_attribute(list_lock_day:List[DayDTO], list_slot:List[TimeSlotDTO], is_admin=False):
    set_use_day = set(map(lambda item: item.date, list_lock_day))
    list_attr = list(map(lambda day: lock_day_to_date_attribute(day, is_admin), list_lock_day))
    for slot in list_slot:
        if slot.date not in set_use_day and ((not slot.hide and not slot.lock) or is_admin):
            set_use_day.add(slot.date)
            list_attr.append(timeslot_to_date_attribute(slot))
    return list_attr

def make_list_date_attribute_date_range(date_start:datetime.date, date_end:datetime.date, set_date:datetime.date)->List[DateAttribute]:
    result = []
    
    now = datetime.datetime.now().date()
    last_week = now - datetime.timedelta(days=7)
    next_week = now + datetime.timedelta(days=7)

    start_cur_week = get_monday(now)
    end_cur_week = get_sunday(now)

    start_last_week = get_monday(last_week)
    end_last_week = get_sunday(last_week)

    start_next_week = get_monday(next_week)
    end_next_week = get_sunday(next_week)
    

    for current_date in get_list_date(date_start, date_end):

        symbol = "🟩"
        if set_date == current_date:
            symbol = "🟥"
        elif current_date>=start_cur_week and current_date<=end_cur_week:
            symbol = "🟨"
        elif current_date>=start_last_week and current_date<=end_last_week:
            symbol = "🟧"
        elif current_date>=start_next_week and current_date<=end_next_week:
            symbol = "🟪"

        result.append(DateAttribute(current_date, marker_pair=MarkerPair(left_symbol=symbol)))
    
    return result

def calc_prev_next_page(page:int, max_page:int)->Tuple[int,int]:
    next_page = page + 1
    prev_page = None
    if page > 0:
        prev_page = page - 1
    if next_page >= max_page:
        next_page = None
    return (prev_page, next_page)

