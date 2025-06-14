import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from tg.keyboards.kb_calendar import Calendar
from tg.keyboards.kb_time import TimeKeyboard
from utils.utils import is_admin, datetime_to_str, time_to_str
from tg.keyboards.utils import make_list_date_attribute, calc_prev_next_page, make_list_date_attribute_date_range
from utils.booking_status import get_status_booking_icon, get_disable_status, ACTUAL_BOOKING, ALL_BOOKING
from dto.timeslot_models import ActualTimeslots
from dto.models import TimeSlotDTO, UserDTO
from dto.booking_models import BookingPage
from dto.user_models import UserPage
from typing import List
from tg.keyboards.kb_text import *
from tg.states.states import State
from tg.callback_params import Params
from settings.settings import settings

def create_back_btn(state:State):
    params = Params(state=state)
    return InlineKeyboardButton(BACK, callback_data=str(params))

def create_book_btn():
    return create_btn_show_calendar(SIGN_UP, State.USER_SHOW_CALENDAR)

def create_start_menu_btn():
    return InlineKeyboardButton(START_MENU, callback_data=str(Params(state=State.USER_SHOW_START_MENU)))


def create_settings_kb():
    kb = [
            [InlineKeyboardButton(REMIND_SETTINGS, callback_data=str(Params(state=State.USER_SHOW_REMINDE_SETTINGS)))],
            [create_start_menu_btn()]
        ]
    return InlineKeyboardMarkup(kb)

def create_reminde_settings_kb(user:UserDTO):
    kb = []
    for item in sorted(settings.reminder_minutes_before):
        text = f"{ICON_ON if item in user.reminder_minutes_before else ICON_OFF} {REMIND_BEFOR.format(offset = item)}"
        kb.append([InlineKeyboardButton(text, callback_data=str(Params(state=State.USER_TOGGLE_REMINDE_BEFORE, data=item)))])


    inaction_text = f"{ICON_ON if user.remind_inactive else ICON_OFF} {REMIND_INACTIVE}"
    kb.append([InlineKeyboardButton(inaction_text, callback_data=str(Params(state=State.USER_TOGGLE_REMINDE_INACTIVE, data=(not user.remind_inactive))))])
    kb.append([InlineKeyboardButton(BACK, callback_data=str(Params(state=State.USER_SHOW_SETTINGS)))])
    
    return InlineKeyboardMarkup(kb)

def create_settings_btn():
    return InlineKeyboardButton(SETTINGS, callback_data=str(Params(state=State.USER_SHOW_SETTINGS)))

def create_bookings_list(state:State, text:str, booking_type:str=ACTUAL_BOOKING, page:int=0):
    params = Params(state=state, booking_type = booking_type, page=page)
    return InlineKeyboardButton(text, callback_data=str(params))

def create_my_bookings(text:str|None = None, booking_type:str=ACTUAL_BOOKING, page:int=0):
    return create_list_booking_btn(State.USER_SHOW_LIST_MY_BOOKING, MY_BOOKING if text is None else text, booking_type, page)

def create_list_booking_btn(state:State, text:str, booking_type:str, page:int=0, date:datetime.date = None, nav_state_callback=None):
    if nav_state_callback == None:
        params = Params(state=state, booking_type = booking_type, page=page, date=date)
    else:
        params = nav_state_callback(page)
    return InlineKeyboardButton(text, callback_data=str(params))

def get_user_start_buttons():
    return InlineKeyboardMarkup([[create_book_btn()],[create_my_bookings()],[create_settings_btn()]])

def create_booking_kb_admin_reminder():
    kb = [
        [create_bookings_list(State.ADMIN_UNPAID_BOOKING, BOOKING_UNPAID_ALL)],
        [create_bookings_list(State.ADMIN_PREV_DAY_BOOKING, BOOKING_PREV_DATE)],
        [create_bookings_list(State.ADMIN_CUR_DAY_BOOKING, BOOKING_CUR_DATE)],
        [create_bookings_list(State.ADMIN_NEXT_DAY_BOOKING, BOOKING_NEXT_DATE)],
        [create_start_menu_btn()],
    ]
    return InlineKeyboardMarkup(kb)

def create_btn_show_calendar(text, state:State, date:datetime.datetime=None):
    if date is None:
        date = datetime.datetime.now()
    return InlineKeyboardButton(text, callback_data=str(Params(state=state, year=date.year, month=date.month)))

def create_btn_copy_schedule(text, state:State):
    return InlineKeyboardButton(text, callback_data=str(Params(state=state)))

def create_btn_show_list_user(state:State, text:str, page:int=0):
    return InlineKeyboardButton(text, callback_data=str(Params(state=state, page=page)))

def get_admin_start_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(SLOT_ACTIONS, callback_data=str(State.IGNORE))],
        [create_btn_show_calendar(ADD_SLOT, State.ADMIN_ADD_TIMESLOT_SELECT_DATE), 
         create_btn_show_calendar(REMOVE_SLOT, State.ADMIN_REMOVE_TIMESLOT_SELECT_DATE)],
        [create_btn_show_calendar(LOCK, State.ADMIN_LOCK_TIMESLOT_SELECT_DATE), 
         create_btn_show_calendar(HIDE, State.ADMIN_HIDE_TIMESLOT_SELECT_DATE)],

        [InlineKeyboardButton(SCHEDULE_ACTIONS, callback_data=str(State.IGNORE))],
        [create_btn_show_calendar(LOCK_DAY, State.ADMIN_LOCK_DAY_SELECT_DATE), 
         create_btn_show_calendar(UNBOOKING, State.ADMIN_UNBOOKING_DAY_SELECT_DATE)],
        [create_btn_copy_schedule(COPY_SCHEDULE, State.ADMIN_COPY_SCHEDULE_SELECT_DAY_ON_SRC_WEEK)],

        [InlineKeyboardButton(BOOKING_ACTIONS, callback_data=str(State.IGNORE))],
        [create_bookings_list(State.ADMIN_CUR_DAY_BOOKING, BOOKING_CUR_DATE), 
         create_bookings_list(State.ADMIN_NEXT_DAY_BOOKING, BOOKING_NEXT_DATE),
         create_bookings_list(State.ADMIN_PREV_DAY_BOOKING, BOOKING_PREV_DATE),],
        [create_bookings_list(State.ADMIN_UNPAID_BOOKING, BOOKING_UNPAID_ALL),
         create_btn_show_calendar(BOOKING_OTHER_DATE, State.ADMIN_SELECT_OTHER_DAY_BOOKING),
         create_bookings_list(State.ADMIN_ALL_LIST_BOOKING, BOOKING_ALL_DATE)],
        [create_btn_show_list_user(State.ADMIN_SELECT_USER_LIST_BOOKING, BOOKING_BY_USER)],

        [InlineKeyboardButton(USER_ACTION, callback_data=str(State.IGNORE))],
        [create_book_btn()],
        [create_my_bookings()], 
        [create_settings_btn()],
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

def create_manage_booking_btn(text:str, state:State, booking_id, show_kb=0):
    return InlineKeyboardButton(text, callback_data = str(Params(state=state, booking_id=booking_id, kb=show_kb)))

def short_admin_booking_keyboard(booking_id, show_kb=0):
    list_btn = [
                (CONFIRM_BOOKING_ADMIN, State.ADMIN_CONFIRM_BOOKING),
                (REJECT_BOOKING_ADMIN, State.ADMIN_REJECT_BOOKING),
                (DELAY_BOOKING_ADMIN, State.ADMIN_MAIN_MENU),
        ]
    kb = [ [create_manage_booking_btn(btn[0],btn[1], booking_id, show_kb)] for btn in list_btn ]
    return InlineKeyboardMarkup(kb)

def full_admin_booking_keyboard(booking_id, is_new, show_kb=1):
    if is_new:
        list_btn = [
                (CONFIRM_BOOKING_ADMIN, State.ADMIN_CONFIRM_BOOKING),
                (REJECT_BOOKING_ADMIN, State.ADMIN_REJECT_BOOKING),
                (DELAY_BOOKING_ADMIN, State.ADMIN_MAIN_MENU),
            ]
    else:
        list_btn = [
            (COMPLETED_BOOKING, State.ADMIN_SET_BOOKING_STATUS_COMPLETED),
            (COMPLETED_UNPAID_BOOKING, State.ADMIN_SET_BOOKING_STATUS_COMPLETED_UNPAID),
            (USER_NOSHOW, State.ADMIN_SET_BOOKING_STATUS_USER_NOSHOW),
            (PROVIDER_NOSHOW, State.ADMIN_SET_BOOKING_STATUS_PROVIDER_NOSHOW),
            (CANCEL, State.ADMIN_CANCEL_BOOKING),
            (NETWORK_ERROR_BOOKING, State.ADMIN_SET_BOOKING_STATUS_NETWORK_ERROR),
            (SYS_ERROR_BOOKING, State.ADMIN_SET_BOOKING_STATUS_SYS_ERROR),
        ]

    kb = [ [create_manage_booking_btn(btn[0],btn[1], booking_id, show_kb)] for btn in list_btn ]

    if show_kb!=0:
        kb.append([create_start_menu_btn()])

    return InlineKeyboardMarkup(kb)

def create_empty_btn():
    return InlineKeyboardButton(EMPTY_BTN, callback_data=str(State.IGNORE))

def create_user_btn(user:UserDTO, next_state:State):
    text = USER_BTN_TEXT.format(first_name = user.first_name, username = user.username)
    return InlineKeyboardButton(text, callback_data=str(Params(state=next_state, user_id=user.id)))

def create_user_list_buttons(users:UserPage, next_state:State, prev_state:State, nav_state:State):
    page = users.page
    prev_page, next_page = calc_prev_next_page(page, users.total_page)

    list_btn = [[create_user_btn(user, next_state)] for user in users.items]

    if prev_page!=None or next_page!=None:
        list_btn.append([
            create_btn_show_list_user(nav_state, PREV_BTN, prev_page) if prev_page!=None else create_empty_btn(),
            InlineKeyboardButton(f"{page+1}", callback_data=str(State.IGNORE)),
            create_btn_show_list_user(nav_state, NEXT_BTN, next_page) if next_page!=None else create_empty_btn(),
            ])
    
    list_btn.append([create_back_btn(prev_state)])

    return InlineKeyboardMarkup(list_btn)


def create_booking_list_buttons(bookings:BookingPage, booking_type:str=ACTUAL_BOOKING, next_state:State = State.USER_BOOKING_DETAILS, nav_state:State = State.USER_SHOW_LIST_MY_BOOKING, create_back_btn = create_book_btn, ignore_status:bool=False, date:datetime.date=None, type_switcher=True, nav_state_callbak=None):
    page = bookings.page
    prev_page, next_page = calc_prev_next_page(page, bookings.total_page)
    
    list_btn = [[create_booking_btn(booking.id, booking.status, booking.date, next_state, ignore_status)] for booking in bookings.items]

    if prev_page!=None or next_page!=None:
        list_btn.append([
            create_list_booking_btn(nav_state, PREV_BTN, booking_type,  prev_page, date, nav_state_callback=nav_state_callbak) if prev_page!=None else create_empty_btn(),
            InlineKeyboardButton(f"{page+1}", callback_data=str(State.IGNORE)),
            create_list_booking_btn(nav_state, NEXT_BTN, booking_type,  next_page, date, nav_state_callback=nav_state_callbak) if next_page!=None else create_empty_btn(),
            ])
    
    
    if type_switcher and booking_type is not None:
        btn_switch_type = create_list_booking_btn(nav_state, SHOW_ALL, ALL_BOOKING, 0, date, nav_state_callback=nav_state_callbak) if booking_type == ACTUAL_BOOKING else create_list_booking_btn(nav_state, SHOW_ACTUAL, ACTUAL_BOOKING, 0, date, nav_state_callback=nav_state_callbak)
        btn_refresh = create_list_booking_btn(nav_state, REFRESH_BTN, booking_type, 0, date, nav_state_callback=nav_state_callbak)
        list_btn.append([btn_refresh, btn_switch_type])
    else:
        btn_refresh = create_list_booking_btn(nav_state, REFRESH_BTN, booking_type, 0, date, nav_state_callback=nav_state_callbak)
        list_btn.append([btn_refresh])

    list_btn.append([create_start_menu_btn()])
    # list_btn.append([create_back_btn()])


    return InlineKeyboardMarkup(list_btn)


def create_calendar_buttons(actual_slots:ActualTimeslots, year:int=None, month:int=None, next_state:State = State.USER_SHOW_TIMESLOTS, nav_state:State = State.USER_SHOW_CALENDAR, is_admin:bool=False, cur_state:State=None):
    additional_btns = []
    additional_btns.append(create_start_menu_btn())

    min_date = actual_slots.min_date

    if cur_state == State.ADMIN_SELECT_OTHER_DAY_BOOKING:
        min_date = min_date - datetime.timedelta(days=settings.admin_select_other_day_booking_day_before)

    cal = Calendar(min_date, 
                   actual_slots.max_date, 
                   callback_data_default_prefix = lambda date: f"state={next_state}&date={date}",
                   callback_data_next = lambda year_next, month_next : f"state={nav_state}&year={year_next}&month={month_next}",
                   callback_data_prev = lambda year_prev, month_prev : f"state={nav_state}&year={year_prev}&month={month_prev}",
                   date_attributes=make_list_date_attribute(actual_slots.list_locked_day, actual_slots.list_timeslot, is_admin), 
                   additional_btns = additional_btns)
    
    if year is None:
        year = actual_slots.min_date.year

    if month is None:
        month = actual_slots.min_date.month

    return cal.create_calendar_buttons(year, month)

def create_calendar_range_buttons(year:int, month:int, next_state:State, nav_state:State, day_before:int, day_after:int, first_date:datetime.date=None, user_id:int=None):

    new = datetime.datetime.now()
    date_start = first_date if first_date else (new - datetime.timedelta(days=day_before)).date()
    date_end = (new + datetime.timedelta(days=day_after)).date()

    if first_date==None:
        callback = lambda date: str(Params(state=next_state, date=date, user_id=user_id)) 
    else:
        callback = lambda date: str(Params(state=next_state, date=first_date, date2=date, user_id=user_id))
       
    cal = Calendar(date_start, 
                   date_end, 
                   callback_data_default_prefix = callback,
                   callback_data_next = lambda year_next, month_next : str(Params(state=nav_state, year=year_next, month=month_next, date=first_date, user_id=user_id)),
                   callback_data_prev = lambda year_prev, month_prev : str(Params(state=nav_state, year=year_prev, month=month_prev, date=first_date, user_id=user_id)),
                   date_attributes = make_list_date_attribute_date_range(date_start, date_end, first_date), 
                   additional_btns = [create_start_menu_btn()])
    
    if year is None:
        year = new.year

    if month is None:
        month = new.month

    if first_date:
        if year is None or month is None or datetime.date(year=first_date.year, month=first_date.month, day=1) > datetime.date(year=year, month=month, day=1):
            year = first_date.year
            month = first_date.month
        
    return cal.create_calendar_buttons(year, month)

def create_time_picker(date:datetime.date, time:datetime.time, default_pefix:State, confirm_prefix:State, cancel_pefix:State):
    if time is None:
        time = settings.add_slot_start_time
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

def user_confirm_booking_btn(timeslot_id:int):
    return InlineKeyboardButton(CONFIRM, callback_data=str(Params(state=State.USER_BOOKING, slot_id=timeslot_id)))

def user_watch_booking_btn(timeslot_id:int):
    return InlineKeyboardButton(WATCH_DOG, callback_data=str(Params(state=State.USER_WATCH_SLOT, slot_id=timeslot_id)))

def other_time_btn(date:datetime.date):
    return InlineKeyboardButton(OTHER_TIME, callback_data=str(Params(state = State.USER_SHOW_TIMESLOTS, date = date)))

def user_confirm_booking_watch_slot_btn(booking_id:int):
    return InlineKeyboardButton(CONFIRM, callback_data=str(Params(state=State.USER_BOOKING_WATCH_SLOT, booking_id=booking_id)))

def user_booking_watch_slot_keyboard(booking_id:int):
    buttons = [
        [user_confirm_booking_watch_slot_btn(booking_id)],
        [create_btn_show_calendar(SHOW_CALENDAR, State.USER_SHOW_CALENDAR)],
        [create_start_menu_btn()],
    ]
    return InlineKeyboardMarkup(buttons)   

def create_confirm_booking_kb(date:datetime.date, timeslot_id:int):
    buttons = [
        [user_confirm_booking_btn(timeslot_id)],
        [other_time_btn(date)],
        [create_btn_show_calendar(SHOW_CALENDAR, State.USER_SHOW_CALENDAR, date)],
        [create_start_menu_btn()],
    ]
    return InlineKeyboardMarkup(buttons)   

def create_watch_booking_kb(date:datetime.date, timeslot_id:int):
    buttons = [
        [user_watch_booking_btn(timeslot_id)],
        [other_time_btn(date)],
        [create_btn_show_calendar(SHOW_CALENDAR, State.USER_SHOW_CALENDAR, date)],
        [create_start_menu_btn()],
    ]
    return InlineKeyboardMarkup(buttons)   

def create_skip_booking_kb(date:datetime.date):
    buttons = [
        [other_time_btn(date)],
        [create_btn_show_calendar(SHOW_CALENDAR, State.USER_SHOW_CALENDAR, date)],
        [create_start_menu_btn()],
    ]
    return InlineKeyboardMarkup(buttons)   


def create_confirm_unbooking_kb(booking_id):
    buttons = [
        [InlineKeyboardButton(CONFIRM, callback_data=str(Params(state=State.USER_UNBOOKING, booking_id=booking_id)))],
        [create_start_menu_btn()],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

def create_confirm_unwatching_kb(booking_id):
    buttons = [
        [InlineKeyboardButton(CONFIRM, callback_data=str(Params(state=State.USER_UNWATCHING, booking_id=booking_id)))],
        [create_start_menu_btn()],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

def create_unbooking_keyboard(booking_id):
    buttons = [
        [InlineKeyboardButton(CANCEL, callback_data=str(Params(state=State.USER_SHOW_CONFIRM_UNBOOKING, booking_id=booking_id)))],
        [create_start_menu_btn()],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def create_confirm_keyboard(callback_data_confirm:str, callback_data_cancel:str):
    buttons = [
        [InlineKeyboardButton(CONFIRM, callback_data=callback_data_confirm)],
        [InlineKeyboardButton(CANCEL, callback_data=callback_data_cancel)]
    ]
    return InlineKeyboardMarkup(buttons)