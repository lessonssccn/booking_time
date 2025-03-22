import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from tg.keyboards.kb_calendar import Calendar
from tg.keyboards.kb_time import TimeKeyboard
from utils.utils import is_admin, datetime_to_str, time_to_str
from tg.keyboards.utils import make_list_date_attribute, calc_prev_next_page
from utils.booking_status import get_status_booking_icon, get_disable_status, ACTUAL_BOOKING, ALL_BOOKING
from dto.timeslot_models import ActualTimeslots
from dto.models import TimeSlotDTO
from dto.booking_models import BookingPage
from typing import List
from tg.keyboards.kb_text import *
from tg.states.states import State
from tg.callback_params import Params

def create_back_btn(state:State):
    params = Params(state=state)
    return InlineKeyboardButton(BACK, callback_data=str(params))

def create_book_btn():
    return create_btn_show_calendar(SIGN_UP, State.USER_SHOW_CALENDAR)

def create_bookings_list(state:State, text:str, booking_type:str=ACTUAL_BOOKING, page:int=0):
    params = Params(state=state, booking_type = booking_type, page=page)
    return InlineKeyboardButton(text, callback_data=str(params))

def create_my_bookings(text:str|None = None, booking_type:str=ACTUAL_BOOKING, page:int=0):
    return create_list_booking_btn(State.USER_SHOW_LIST_MY_BOOKING, MY_BOOKING if text is None else text, booking_type, page)

def create_list_booking_btn(state:State, text:str, booking_type:str, page:int=0):
    params = Params(state=state, booking_type = booking_type, page=page)
    return InlineKeyboardButton(text, callback_data=str(params))

def get_user_start_buttons():
    return InlineKeyboardMarkup([[create_book_btn()],[create_my_bookings()],])

def create_btn_show_calendar(text, state:State):
    now = datetime.datetime.now()
    return InlineKeyboardButton(text, callback_data=str(Params(state=state, year=now.year, month=now.month)))

def get_admin_start_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(SLOT_ACTIONS, callback_data=str(State.IGNORE))],
        [create_btn_show_calendar(ADD_SLOT, State.ADMIN_ADD_TIMESLOT_SELECT_DATE), 
         create_btn_show_calendar(REMOVE_SLOT, State.ADMIN_REMOVE_TIMESLOT_SELECT_DATE)],
        [create_btn_show_calendar(LOCK, State.ADMIN_LOCK_TIMESLOT_SELECT_DATE), 
         create_btn_show_calendar(HIDE, State.ADMIN_HIDE_TIMESLOT_SELECT_DATE)],
        [InlineKeyboardButton(DAY_ACTIONS, callback_data=str(State.IGNORE))],
        [create_btn_show_calendar(LOCK_DAY, State.ADMIN_LOCK_DAY_SELECT_DATE), 
         create_btn_show_calendar(UNBOOKING, State.ADMIN_UNBOOKING_DAY_SELECT_DATE)],
        [InlineKeyboardButton(BOOKING_ACTIONS, callback_data=str(State.IGNORE))],
        [create_bookings_list(State.ADMIN_CUR_DAY_BOOKING, BOOKING_CUR_DATE), 
         create_bookings_list(State.ADMIN_ALL_LIST_BOOKING, BOOOKING_ALL_DATE)],
        [InlineKeyboardButton(USER_ACTION, callback_data=str(State.IGNORE))],
        [create_book_btn(),create_my_bookings()],
    ])

def create_start_keyboard(user_id):
    if is_admin(user_id):
        return get_admin_start_buttons()
    else:
        return get_user_start_buttons()


def get_callback_booking_details(booking_id:int, status:str, state:State, ignore_status:bool):
    if not ignore_status and status in get_disable_status():
        return str(State.IGNORE)
    return str(Params(state=state, booking_id=booking_id))

def create_booking_btn(booking_id:int, status:str, date:datetime.date, state:State, ignore_status:bool):
    icon = get_status_booking_icon(status)
    return InlineKeyboardButton(f"{icon} {datetime_to_str(date)}", callback_data=get_callback_booking_details(booking_id, status, state, ignore_status))

def confirm_admin_booking_keyboard(booking_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(CONFIRM_BOOKING_ADMIN, callback_data = str(Params(state=State.ADMIN_CONFIRM_BOOKING , booking_id=booking_id)))],
        [InlineKeyboardButton(REJECT_BOOKING_ADMIN, callback_data = str(Params(state=State.ADMIN_REJECT_BOOKING , booking_id=booking_id)))],
        [InlineKeyboardButton(CANCEL, callback_data = str(Params(state=State.ADMIN_CANCEL_BOOKING , booking_id=booking_id)))],
        [InlineKeyboardButton(DELAY_BOOKING_ADMIN, callback_data = str(Params(state=State.ADMIN_MAIN_MENU , booking_id=booking_id)))],
    ])

def create_empty_btn():
    return InlineKeyboardButton(EMPTY_BTN, callback_data=str(State.IGNORE))

def create_booking_list_buttons(bookings:BookingPage, booking_type:str=ACTUAL_BOOKING, next_state:State = State.USER_BOOKING_DETAILS, nav_state:State = State.USER_SHOW_LIST_MY_BOOKING, create_back_btn = create_book_btn, ignore_status:bool=False):
    page = bookings.page
    prev_page, next_page = calc_prev_next_page(page, bookings.total_page)
    
    list_btn = [[create_booking_btn(booking.id, booking.status, booking.date, next_state, ignore_status)] for booking in bookings.items]

    if prev_page!=None or next_page!=None:
        list_btn.append([
            create_list_booking_btn(nav_state, PREV_BTN, booking_type,  prev_page) if prev_page!=None else create_empty_btn(),
            InlineKeyboardButton(f"{page+1}", callback_data=str(State.IGNORE)),
            create_list_booking_btn(nav_state, NEXT_BTN, booking_type,  prev_page) if next_page!=None else create_empty_btn(),
            ])
    
    
    btn_switch_type = create_list_booking_btn(nav_state, SHOW_ALL, ALL_BOOKING, 0) if booking_type == ACTUAL_BOOKING else create_list_booking_btn(nav_state, SHOW_ACTUAL, ACTUAL_BOOKING, 0)
    btn_refresh = create_list_booking_btn(nav_state, REFRESH_BTN, booking_type, 0)
    list_btn.append([btn_refresh, btn_switch_type])
    list_btn.append([create_back_btn()])

    return InlineKeyboardMarkup(list_btn)


def create_calendar_buttons(actual_slots:ActualTimeslots, year:int=None, month:int=None, selct_state:State = State.USER_SHOW_TIMESLOTS, nav_state:State = State.USER_SHOW_CALENDAR, is_admin:bool=False):
    additional_btns = []
    if not is_admin:
        additional_btns.append(create_my_bookings())

    cal = Calendar(actual_slots.min_date, 
                   actual_slots.max_date, 
                   callback_data_default_prefix=str(selct_state),
                   callback_data_next=str(nav_state),
                   callback_data_prev=str(nav_state),
                   date_attributes=make_list_date_attribute(actual_slots.list_locked_day, actual_slots.list_timeslot, is_admin), 
                   additional_btns = additional_btns)
    
    if year is None:
        year = actual_slots.min_date.year

    if month is None:
        month = actual_slots.min_date.month

    return cal.create_calendar_buttons(year, month)

def create_time_picker(date:datetime.date, time:datetime.time, default_pefix:State, confirm_prefix:State, cancel_pefix:State):
    if time is None:
        time = datetime.time(10,0,0)
    kb_time = TimeKeyboard(date, time, str(default_pefix), str(confirm_prefix), str(cancel_pefix), disable_prefix=str(State.IGNORE))
    return kb_time.create_time_buttons()

def create_timeslot_btn(slot:TimeSlotDTO, state:State, is_admin:bool):
    is_active = True
    icons = ""
    if slot.lock:
        icons += f"🔒"
        is_active = False
    if slot.capacity<=0:
        icons += f"⚠️"
    if slot.hide:
        icons += f"🕶️"
    
    text = f'{icons}{time_to_str(slot.time)}'

    if is_admin:
        is_active = True

    callback_data = str(Params(state=state, slot_id=slot.id)) if is_active else str(State.IGNORE)

    return InlineKeyboardButton(text, callback_data=callback_data)

def create_timeslots_buttons(list_timeslot:List[TimeSlotDTO], state:State, addition_btns:List[List[InlineKeyboardButton]]=[], is_admin:bool=False):
    if len(list_timeslot)>0:
        buttons = [[create_timeslot_btn(slot, state, is_admin)] for slot in list_timeslot]
    else:
        buttons = [[InlineKeyboardButton(NOT_FOUND, callback_data=str(State.IGNORE))]]

    buttons.extend(addition_btns)
    return InlineKeyboardMarkup(buttons)

def create_confirm_booking_kb(date:datetime.date, timeslot_id:int):
    buttons = [
        [InlineKeyboardButton(CONFIRM, callback_data=str(Params(state=State.USER_BOOKING, slot_id=timeslot_id)))],
        [InlineKeyboardButton(OTHER_TIME, callback_data=str(Params(state = State.USER_SHOW_TIMESLOTS, date = date)))],
        [InlineKeyboardButton(SHOW_CALENDAR, callback_data= str(Params(state = State.USER_SHOW_CALENDAR, year=date.year, month=date.month)))],
    ]
    return InlineKeyboardMarkup(buttons)   

def create_confirm_unbooking_kb(booking_id):
    buttons = [
        [InlineKeyboardButton(CONFIRM, callback_data=str(Params(state=State.USER_UNBOOKING, booking_id=booking_id)))],
        [create_book_btn()],
        [create_my_bookings()],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

def create_unbooking_keyboard(booking_id):
    buttons = [
        [InlineKeyboardButton(CANCEL, callback_data=str(Params(state=State.USER_SHOW_CONFIRM_UNBOOKING, booking_id=booking_id)))],
        [create_book_btn()],
        [create_my_bookings()]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

def create_confirm_keyboard(callback_data_confirm:str, callback_data_cancel:str):
    buttons = [
        [InlineKeyboardButton(CONFIRM, callback_data=callback_data_confirm)],
        [InlineKeyboardButton(CANCEL, callback_data=callback_data_cancel)]
    ]
    return InlineKeyboardMarkup(buttons)