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

def create_list_booking_btn(state:State, text:str, booking_type:str, page:int=0, date:datetime.date = None):
    params = Params(state=state, booking_type = booking_type, page=page, date=date)
    return InlineKeyboardButton(text, callback_data=str(params))

def get_user_start_buttons():
    return InlineKeyboardMarkup([[create_book_btn()],[create_my_bookings()],[create_settings_btn()]])

def create_booking_kb_admin_reminder():
    kb = [
        [create_bookings_list(State.ADMIN_PREV_DAY_BOOKING, BOOKING_PREV_DATE)],
        [create_bookings_list(State.ADMIN_CUR_DAY_BOOKING, BOOKING_CUR_DATE)],
        [create_bookings_list(State.ADMIN_NEXT_DAY_BOOKING, BOOKING_NEXT_DATE)],
        [create_start_menu_btn()]
    ]
    return InlineKeyboardMarkup(kb)

def create_btn_show_calendar(text, state:State):
    date = datetime.datetime.now()
    return InlineKeyboardButton(text, callback_data=str(Params(state=state, year=date.year, month=date.month)))

def create_btn_copy_schedule(text, state:State):
    return InlineKeyboardButton(text, callback_data=str(Params(state=state)))

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
        [create_btn_show_calendar(BOOOKING_OTHER_DATE, State.ADMIN_SELECT_OTHER_DAY_BOOKING),
         create_bookings_list(State.ADMIN_ALL_LIST_BOOKING, BOOOKING_ALL_DATE)],

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

def create_btn_confirm_booking(booking_id, show_kb=0):
    return InlineKeyboardButton(CONFIRM_BOOKING_ADMIN, callback_data = str(Params(state=State.ADMIN_CONFIRM_BOOKING , booking_id=booking_id, kb=show_kb)))

def create_btn_reject_booking(booking_id, show_kb=0):
    return InlineKeyboardButton(REJECT_BOOKING_ADMIN, callback_data = str(Params(state=State.ADMIN_REJECT_BOOKING , booking_id=booking_id, kb=show_kb)))

def create_btn_cancel_booking(booking_id, show_kb=0):
    return InlineKeyboardButton(CANCEL, callback_data = str(Params(state=State.ADMIN_CANCEL_BOOKING , booking_id=booking_id, kb=show_kb)))

def create_btn_delay_booking(booking_id, show_kb=0):
    return InlineKeyboardButton(DELAY_BOOKING_ADMIN, callback_data = str(Params(state=State.ADMIN_MAIN_MENU , booking_id=booking_id, kb=show_kb)))

def create_btn_user_noshow_booking(booking_id, show_kb=0):
    return InlineKeyboardButton(USER_NOSHOW, callback_data = str(Params(state=State.ADMIN_SET_BOOKING_STATUS_USER_NOSHOW , booking_id=booking_id, kb=show_kb)))

def create_btn_provider_noshow_booking(booking_id, show_kb=0):
    return InlineKeyboardButton(PROVIDER_NOSHOW, callback_data = str(Params(state=State.ADMIN_SET_BOOKING_STATUS_PROVIDER_NOSHOW , booking_id=booking_id, kb=show_kb)))

def create_btn_completed_booking(booking_id, show_kb=0):
    return InlineKeyboardButton(COMPLETED_BOOKING, callback_data = str(Params(state=State.ADMIN_SET_BOOKING_STATUS_COMPLETED , booking_id=booking_id, kb=show_kb)))

def create_btn_completed_unpaid_booking(booking_id, show_kb=0):
    return InlineKeyboardButton(COMPLETED_UNPAID_BOOKING, callback_data = str(Params(state=State.ADMIN_SET_BOOKING_STATUS_COMPLETED_UNPAID , booking_id=booking_id, kb=show_kb)))

def create_btn_sys_error_booking(booking_id, show_kb=0):
    return InlineKeyboardButton(SYS_ERROR_BOOKING, callback_data = str(Params(state=State.ADMIN_SET_BOOKING_STATUS_SYS_ERROR , booking_id=booking_id, kb=show_kb)))

def short_admin_booking_keyboard(booking_id, show_kb=0):
    kb = [ [btn(booking_id, show_kb)] for btn in [create_btn_confirm_booking, create_btn_reject_booking, create_btn_delay_booking] ]
    return InlineKeyboardMarkup(kb)

def full_admin_booking_keyboard(booking_id, is_new, show_kb=1):
    if is_new:
        list_btn = [create_btn_confirm_booking, create_btn_reject_booking, create_btn_delay_booking]
    else:
        list_btn = [
            create_btn_completed_booking,
            create_btn_completed_unpaid_booking,
            create_btn_user_noshow_booking,
            create_btn_provider_noshow_booking,
            create_btn_cancel_booking,
            create_btn_sys_error_booking
        ]

    kb = [ [btn(booking_id, show_kb)] for btn in list_btn ]

    if show_kb!=0:
        kb.append([create_start_menu_btn()])

    return InlineKeyboardMarkup(kb)

def create_empty_btn():
    return InlineKeyboardButton(EMPTY_BTN, callback_data=str(State.IGNORE))

def create_booking_list_buttons(bookings:BookingPage, booking_type:str=ACTUAL_BOOKING, next_state:State = State.USER_BOOKING_DETAILS, nav_state:State = State.USER_SHOW_LIST_MY_BOOKING, create_back_btn = create_book_btn, ignore_status:bool=False, date:datetime.date=None):
    page = bookings.page
    prev_page, next_page = calc_prev_next_page(page, bookings.total_page)
    
    list_btn = [[create_booking_btn(booking.id, booking.status, booking.date, next_state, ignore_status)] for booking in bookings.items]

    if prev_page!=None or next_page!=None:
        list_btn.append([
            create_list_booking_btn(nav_state, PREV_BTN, booking_type,  prev_page, date) if prev_page!=None else create_empty_btn(),
            InlineKeyboardButton(f"{page+1}", callback_data=str(State.IGNORE)),
            create_list_booking_btn(nav_state, NEXT_BTN, booking_type,  next_page, date) if next_page!=None else create_empty_btn(),
            ])
    
    
    btn_switch_type = create_list_booking_btn(nav_state, SHOW_ALL, ALL_BOOKING, 0, date) if booking_type == ACTUAL_BOOKING else create_list_booking_btn(nav_state, SHOW_ACTUAL, ACTUAL_BOOKING, 0, date)
    btn_refresh = create_list_booking_btn(nav_state, REFRESH_BTN, booking_type, 0, date)
    list_btn.append([btn_refresh, btn_switch_type])
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

def create_calendar_range_buttons(year:int, month:int, next_state:State, nav_state:State, set_date:datetime.date=None):

    new = datetime.datetime.now()
    date_start = set_date if set_date else (new - datetime.timedelta(days=settings.day_before)).date()
    date_end = (new + datetime.timedelta(days=settings.day_after)).date()

    nav_callback_set_date = ""

    if set_date==None:
        callback = lambda date: f"state={next_state}&date={date}" 
    else:
        callback = lambda date: f"state={next_state}&date={set_date}&date2={date}"
        nav_callback_set_date += f"&date={set_date}"

    cal = Calendar(date_start, 
                   date_end, 
                   callback_data_default_prefix = callback,
                   callback_data_next = lambda year_next, month_next : f"state={nav_state}&year={year_next}&month={month_next}" + nav_callback_set_date,
                   callback_data_prev = lambda year_prev, month_prev : f"state={nav_state}&year={year_prev}&month={month_prev}" + nav_callback_set_date,
                   date_attributes = make_list_date_attribute_date_range(date_start, date_end, set_date), 
                   additional_btns = [create_start_menu_btn()])
    
    if year is None:
        year = new.year

    if month is None:
        month = new.month

    if set_date:
        year = set_date.year
        month = set_date.month
        
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

def create_confirm_booking_kb(date:datetime.date, timeslot_id:int):
    buttons = [
        [InlineKeyboardButton(CONFIRM, callback_data=str(Params(state=State.USER_BOOKING, slot_id=timeslot_id)))],
        [InlineKeyboardButton(OTHER_TIME, callback_data=str(Params(state = State.USER_SHOW_TIMESLOTS, date = date)))],
        [InlineKeyboardButton(SHOW_CALENDAR, callback_data= str(Params(state = State.USER_SHOW_CALENDAR, year=date.year, month=date.month)))],
        [create_start_menu_btn()],
    ]
    return InlineKeyboardMarkup(buttons)   

def create_confirm_unbooking_kb(booking_id):
    buttons = [
        [InlineKeyboardButton(CONFIRM, callback_data=str(Params(state=State.USER_UNBOOKING, booking_id=booking_id)))],
        # [create_book_btn()],
        # [create_my_bookings()],
        [create_start_menu_btn()],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

def create_unbooking_keyboard(booking_id):
    buttons = [
        [InlineKeyboardButton(CANCEL, callback_data=str(Params(state=State.USER_SHOW_CONFIRM_UNBOOKING, booking_id=booking_id)))],
        # [create_book_btn()],
        # [create_my_bookings()],
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