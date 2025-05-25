import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils.utils import *
from tg.keyboards.keyboards import *
from tg.constants import *
from tg.keyboards.kb_text import *
from errors.errors import *
from services.service_factory import ServiceFactory
from tg.callback_params import Params   
from tg.states.states import State
from settings.settings import settings

ADMIN_ACTIONS_FUNC = {
    State.ADMIN_ADD_TIMESLOT_SELECT_DATE:"select_day",
    State.ADMIN_ADD_TIMESLOT_SELECT_TIME: "add_timeslot_select_time",
    State.ADMIN_ADD_TIMESLOT_CONFIRM: "add_timeslot_confirm",
    State.ADMIN_ADD_TIMESLOT_CANCEL:"action_cancel",

    State.ADMIN_REMOVE_TIMESLOT_SELECT_DATE: "select_day",
    State.ADMIN_REMOVE_TIMESLOT_SELECT_SLOT: "select_slot",
    State.ADMIN_REMOVE_TIMESLOT_CONFIRM_MSG: "remove_timeslot_confirm_msg",
    State.ADMIN_REMOVE_TIMESLOT_CONFIRM: "process_admin_remove_timeslot_confirm",
    State.ADMIN_REMOVE_TIMESLOT_CANCEL: "action_cancel",

    State.ADMIN_LOCK_TIMESLOT_SELECT_DATE: "select_day",
    State.ADMIN_LOCK_TIMESLOT_SELECT_SLOT: "select_slot",
    State.ADMIN_LOCK_TIMESLOT: "process_lock_timeslot",

    State.ADMIN_HIDE_TIMESLOT_SELECT_DATE: "select_day",
    State.ADMIN_HIDE_TIMESLOT_SELECT_SLOT: "select_slot",
    State.ADMIN_HIDE_TIMESLOT: "process_hide_timeslot",

    State.ADMIN_LOCK_DAY_SELECT_DATE: "select_day",
    State.ADMIN_LOCK_DAY: "process_lock_day",

    State.ADMIN_UNBOOKING_DAY_SELECT_DATE: "select_day",
    State.ADMIN_UNBOOKING_DAY_SHOW_CONFIRM_MSG: "show_confirm_msg_unbooking_day",
    State.ADMIN_UNBOOKING_DAY_CONFIRM: "process_unbooking_day",
    State.ADMIN_UNBOOKING_DAY_CANCEL: "action_cancel",

    State.ADMIN_COPY_SCHEDULE_SELECT_DAY_ON_SRC_WEEK: "select_range_day",
    State.ADMIN_COPY_SCHEDULE_SELECT_DAY_ON_DES_WEEK: "select_range_day",
    State.ADMIN_COPY_SCHEDULE_SHOW_CONFIRM_MSG: "show_confirm_copy_schedule",
    State.ADMIN_COPY_SCHEDULE_CONFIRM: "process_copy_schedule",
    State.ADMIN_COPY_SCHEDULE_CANCEL: "action_cancel",

    State.ADMIN_CONFIRM_BOOKING:"admin_confirm_reject_booking",
    State.ADMIN_REJECT_BOOKING:"admin_confirm_reject_booking",
    State.ADMIN_CANCEL_BOOKING:"admin_cancel_booking",

    State.ADMIN_CUR_DAY_BOOKING:"show_list_booking",
    State.ADMIN_NEXT_DAY_BOOKING:"show_list_booking",
    State.ADMIN_ALL_LIST_BOOKING:"show_list_booking",
    State.ADMIN_BOOKING_DETAILS:"show_booking_details",
    State.ADMIN_SELECT_OTHER_DAY_BOOKING:"select_day",
    State.ADMIN_OTHER_DAY_BOOKING:"show_list_booking",

    State.ADMIN_MAIN_MENU: "show_admin_main_menu",
}


ADMIN_ACTIONS_NEXT_ACTION = {
    State.ADMIN_ADD_TIMESLOT_SELECT_DATE : State.ADMIN_ADD_TIMESLOT_SELECT_TIME,
    State.ADMIN_REMOVE_TIMESLOT_SELECT_DATE : State.ADMIN_REMOVE_TIMESLOT_SELECT_SLOT,
    State.ADMIN_LOCK_TIMESLOT_SELECT_DATE : State.ADMIN_LOCK_TIMESLOT_SELECT_SLOT,
    State.ADMIN_HIDE_TIMESLOT_SELECT_DATE : State.ADMIN_HIDE_TIMESLOT_SELECT_SLOT,

    State.ADMIN_REMOVE_TIMESLOT_SELECT_SLOT: State.ADMIN_REMOVE_TIMESLOT_CONFIRM_MSG,
    State.ADMIN_LOCK_TIMESLOT_SELECT_SLOT: State.ADMIN_LOCK_TIMESLOT,
    State.ADMIN_HIDE_TIMESLOT_SELECT_SLOT: State.ADMIN_HIDE_TIMESLOT,

    State.ADMIN_LOCK_DAY_SELECT_DATE: State.ADMIN_LOCK_DAY,
    State.ADMIN_UNBOOKING_DAY_SELECT_DATE: State.ADMIN_UNBOOKING_DAY_SHOW_CONFIRM_MSG,
    State.ADMIN_SELECT_OTHER_DAY_BOOKING: State.ADMIN_OTHER_DAY_BOOKING,

    State.ADMIN_COPY_SCHEDULE_SELECT_DAY_ON_SRC_WEEK: State.ADMIN_COPY_SCHEDULE_SELECT_DAY_ON_DES_WEEK,
    State.ADMIN_COPY_SCHEDULE_SELECT_DAY_ON_DES_WEEK: State.ADMIN_COPY_SCHEDULE_SHOW_CONFIRM_MSG,
}

ADMIN_ACTIONS_PREV_ACTION = {
    State.ADMIN_ADD_TIMESLOT_SELECT_TIME :  State.ADMIN_ADD_TIMESLOT_SELECT_DATE,
    State.ADMIN_REMOVE_TIMESLOT_SELECT_SLOT : State.ADMIN_REMOVE_TIMESLOT_SELECT_DATE,
    State.ADMIN_LOCK_TIMESLOT_SELECT_SLOT : State.ADMIN_LOCK_TIMESLOT_SELECT_DATE,
    State.ADMIN_HIDE_TIMESLOT_SELECT_SLOT : State.ADMIN_HIDE_TIMESLOT_SELECT_DATE,
}

ADMIN_ACTIONS_MSG = {
    State.ADMIN_ADD_TIMESLOT_SELECT_DATE: CHOOSE_DATE_ADD_SLOT,
    State.ADMIN_ADD_TIMESLOT_SELECT_TIME: SELECT_TIME_ADD_SLOT,

    State.ADMIN_REMOVE_TIMESLOT_SELECT_DATE: CHOOSE_DATE_REMOVE_SLOT,
    State.ADMIN_REMOVE_TIMESLOT_SELECT_SLOT: CHOOSE_SLOT_REMOVE,

    State.ADMIN_LOCK_TIMESLOT_SELECT_DATE: CHOOSE_DATE_LOCK_SLOT,
    State.ADMIN_LOCK_TIMESLOT_SELECT_SLOT: CHOOSE_SLOT_LOCK,

    State.ADMIN_HIDE_TIMESLOT_SELECT_DATE: CHOOSE_DATE_HIDDEN_SLOT,
    State.ADMIN_HIDE_TIMESLOT_SELECT_SLOT: CHOOSE_SLOT_HIDDEN,

    State.ADMIN_REMOVE_TIMESLOT_CANCEL: REMOVE_TIMESLOT_CANCEL,
    State.ADMIN_ADD_TIMESLOT_CANCEL: ADD_TIMESLOT_CANCEL,

    State.ADMIN_LOCK_DAY_SELECT_DATE: DAY_LOCKE_SELECT,
    State.ADMIN_UNBOOKING_DAY_SELECT_DATE: DAY_UNBOOKING,

    State.ADMIN_COPY_SCHEDULE_CANCEL: COPY_SCHEDULE_CANCEL,

    State.ADMIN_CONFIRM_BOOKING: SUCCESS_CONFIRM_BOOKING_FOR_ADMIN,
    State.ADMIN_REJECT_BOOKING: SUCCESS_REJECT_BOOKING_FOR_ADMIN,

    State.ADMIN_UNBOOKING_DAY_CANCEL: UNBOOKING_DAY_CANCEL,
    State.ADMIN_SELECT_OTHER_DAY_BOOKING: SELECT_OTHER_DAY_BOOKING,

    State.ADMIN_COPY_SCHEDULE_SELECT_DAY_ON_SRC_WEEK: SELECT_DAY_ON_SRC_WEEK,
    State.ADMIN_COPY_SCHEDULE_SELECT_DAY_ON_DES_WEEK: SELECT_DAY_ON_DES_WEEK,
}
#====================================================================================================================
async def process_admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.callback_query.edit_message_text(NOT_ADMIN, reply_markup=create_start_keyboard(user_id))
        return
    function_name = ADMIN_ACTIONS_FUNC[params.state]
    function = globals()[function_name]
    await function(update, context, params)

async def process_unknown_action(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    await update.callback_query.edit_message_text(UNKNOWN_ERROR_MSG)
    await ServiceFactory.get_notification_service().send_notification_to_channel(UNKNOWN_ERROR_NOTIFICATION + f"\ntg_id={update.effective_user.id}\nparams={params.model_dump(exclude_unset=True)}", update.effective_user)
   
async def select_day(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    msg = ADMIN_ACTIONS_MSG.get(params.state, ERROR_MSG)
    next_action = ADMIN_ACTIONS_NEXT_ACTION[params.state]
    await show_calendar_admin(update, context, msg, next_action, params)

async def select_range_day(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    msg = ADMIN_ACTIONS_MSG.get(params.state, ERROR_MSG)
    next_action = ADMIN_ACTIONS_NEXT_ACTION[params.state]
    await show_range_calendar_admin(update, context, msg, next_action, params)

async def select_slot(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    msg = ADMIN_ACTIONS_MSG.get(params.state, ERROR_MSG).format(date=params.date)
    next_action = ADMIN_ACTIONS_NEXT_ACTION[params.state]
    prev_action = ADMIN_ACTIONS_PREV_ACTION[params.state]
    await show_list_timeslot_admin(update, context, params.date, msg, next_action, prev_action)

async def action_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    await show_admin_msg(update, context, ADMIN_ACTIONS_MSG.get(params.state, ERROR_MSG))

async def show_admin_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    await show_admin_msg(update, context, "Что будет делать?")
#===================================================================================================
async def add_timeslot_select_time(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    default = State.ADMIN_ADD_TIMESLOT_SELECT_TIME
    confirm = State.ADMIN_ADD_TIMESLOT_CONFIRM
    cancel = State.ADMIN_ADD_TIMESLOT_CANCEL
    msg = TIMESLOT_CREATE_SELECT_TIME.format(date = params.date)
    list_slot = await ServiceFactory.get_timeslot_service().get_list_timeslot_by_date(params.date)
    if list_slot:
        msg += TIMESLOT_ALREADY_CREATED.format(list_slot = "\n".join(map(lambda item: f"{item.time}", list_slot)))
    await show_time_picker(update, context, msg ,params.date, params.time, default, confirm, cancel)

async def add_timeslot_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    await ServiceFactory.get_timeslot_service().add_timeslot(params.date, params.time)
    msg = TIMESLOT_CREATED.format(date=params.date, time=params.time)
    await show_admin_msg(update, context, msg)
#========================================================================================================
async def remove_timeslot_confirm_msg(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    slot = await ServiceFactory.get_timeslot_service().get_timeslot_by_id(params.slot_id)
    callback_data_confirm = str(Params(state=State.ADMIN_REMOVE_TIMESLOT_CONFIRM, slot_id=slot.id))
    callback_data_cancel = str(Params(state=State.ADMIN_REMOVE_TIMESLOT_CANCEL, slot_id=slot.id))
    msg = CONFIRM_REMOVE.format(date=slot.date, time=slot.time)
    await show_confirm_msg(update, context, msg, callback_data_confirm, callback_data_cancel)

async def process_admin_remove_timeslot_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    slot = await ServiceFactory.get_timeslot_service().remove_timeslot(params.slot_id)
    msg = TIMESLOT_REMOVED.format(date = slot.date, time = slot.time)
    await show_admin_msg(update, context, msg)
#=========================================================================================================
async def process_lock_timeslot(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    slot = await ServiceFactory.get_timeslot_service().lock_timeslot(params.slot_id)
    msg = (TIMESLOT_UNLOCKED, TIMESLOT_LOCKED)[slot.lock].format(date = slot.date, time = slot.time)
    await show_admin_msg(update, context, msg)

async def process_hide_timeslot(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    slot = await ServiceFactory.get_timeslot_service().hide_timeslot(params.slot_id)
    msg = (TIMESLOT_SHOW, TIMESLOT_HIDDEN)[slot.hide].format(date = slot.date, time = slot.time)
    await show_admin_msg(update, context, msg)
#==========================================================================================================
async def process_lock_day(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    day = await ServiceFactory.get_day_service().lock_day(params.date)
    msg = (DAY_UNLOCKED, DAY_LOCKED)[day.lock].format(date = day.date)
    await show_admin_msg(update, context, msg)
#==========================================================================================================
async def admin_confirm_reject_booking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    if params.state == State.ADMIN_CONFIRM_BOOKING:
        func = ServiceFactory.get_booking_service().confirm_booking
    else:
        func = ServiceFactory.get_booking_service().reject_booking

    booking = await func(params.booking_id)
    msg = ADMIN_ACTIONS_MSG[params.state].format(date = booking.time_slot.date, time = booking.time_slot.time, name = booking.user.first_name, username = booking.user.username, tg_id = booking.user.tg_id)
  
    await show_admin_msg(update, context, msg)

async def admin_cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking = await ServiceFactory.get_booking_service().cancel_booking(booking_id=params.booking_id, is_admin=True)
    msg_admin = SUCCESS_CANCEL_BOOKING_ADMIN_FOR_ADMIN.format(date = booking.time_slot.date, time = booking.time_slot.time, name = booking.user.first_name, username = booking.user.username, tg_id = booking.user.tg_id)
    await show_admin_msg(update, context, msg_admin)

#=====================================================================================================================================
async def show_list_booking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    date_range = {
                    State.ADMIN_CUR_DAY_BOOKING:BOOKING_CUR_DATE, 
                    State.ADMIN_NEXT_DAY_BOOKING:BOOKING_NEXT_DATE, 
                    State.ADMIN_ALL_LIST_BOOKING: BOOOKING_ALL_DATE,
                    State.ADMIN_OTHER_DAY_BOOKING: params.date,
                }
    if params.state == State.ADMIN_CUR_DAY_BOOKING:
        bookings = await ServiceFactory.get_booking_service().get_list_booking_curday(params.booking_type, params.page)
    elif params.state == State.ADMIN_NEXT_DAY_BOOKING:
        bookings = await ServiceFactory.get_booking_service().get_list_booking_nextday(params.booking_type, params.page)
    elif params.date:
        bookings = await ServiceFactory.get_booking_service().get_list_booking_by_date(params.date, params.booking_type, params.page)
    else:
        bookings = await ServiceFactory.get_booking_service().get_all_actual_booking(params.booking_type, params.page)
        
    await update.callback_query.edit_message_text(
        ADMIN_BOOKING_LIST.format(date = date_range.get(params.state), actual_date = datetime.datetime.now()),
        reply_markup = create_booking_list_buttons(
            bookings, 
            params.booking_type, 
            next_state=State.ADMIN_BOOKING_DETAILS, 
            nav_state=params.state, 
            create_back_btn=lambda: create_back_btn(State.ADMIN_MAIN_MENU), 
            ignore_status=True,
            date=params.date))

async def show_booking_details(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking = await ServiceFactory.get_booking_service().get_booking_by_id(params.booking_id)
    msg = BOOKING_DETAILS_ADMIN.format(date = booking.time_slot.date, time = booking.time_slot.time, name = booking.user.first_name, username = booking.user.username, tg_id = booking.user.tg_id)
    await update.callback_query.edit_message_text(msg, reply_markup = confirm_admin_booking_keyboard(booking.id))
#==========================================================================================================================
async def show_confirm_msg_unbooking_day(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    callback_data_confirm = str(Params(state=State.ADMIN_UNBOOKING_DAY_CONFIRM, date=params.date))
    callback_data_cancel = str(Params(state=State.ADMIN_UNBOOKING_DAY_CANCEL, date=params.date))
    msg = CONFIRM_MSG_UNBOOKING_DAY.format(date=params.date)
    await show_confirm_msg(update, context, msg, callback_data_confirm, callback_data_cancel)

async def process_unbooking_day(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking_list = await ServiceFactory.get_booking_service().cancel_bookings_day(params.date)
    for booking in booking_list:
        msg_admin = SUCCESS_CANCEL_BOOKING_ADMIN_FOR_ADMIN.format(date = booking.time_slot.date, time = booking.time_slot.time, name = booking.user.first_name, username = booking.user.username, tg_id = booking.user.tg_id)
        await show_admin_msg(update, context, msg_admin)

#==========================================================================================================================
async def show_confirm_copy_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    callback_data_confirm = str(Params(state=State.ADMIN_COPY_SCHEDULE_CONFIRM, date=params.date, date2=params.date2))
    callback_data_cancel = str(Params(state=State.ADMIN_COPY_SCHEDULE_CANCEL, date=params.date))
    
    date_src_start = date_to_str(get_monday(params.date))
    date_src_end = date_to_str(get_sunday(params.date))

    date_des_start = date_to_str(get_monday(params.date2))
    date_des_end = date_to_str(get_sunday(params.date2))
    
    msg = CONFIRM_MSG_COPY_SCHEDULE.format(date_src_start = date_src_start, 
                                           date_src_end = date_src_end, 
                                           date_des_start = date_des_start, 
                                           date_des_end = date_des_end)
    
    await show_confirm_msg(update, context, msg, callback_data_confirm, callback_data_cancel)

async def process_copy_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    date_src_start = get_monday(params.date)
    date_src_end = get_sunday(params.date)

    date_des_start = get_monday(params.date2)
    date_des_end = get_sunday(params.date2)

    count_new_slot = await ServiceFactory.get_timeslot_service().copy_range(date_src_start, date_src_end, date_des_start, date_des_end)

    await show_admin_msg(update, context, COPY_SCHEDULE_RESULT.format(date_src_start = date_to_str(date_src_start), 
                                           date_src_end = date_to_str(date_src_end), 
                                           date_des_start = date_to_str(date_des_start), 
                                           date_des_end = date_to_str(date_des_end),
                                           count = count_new_slot))

#==========================================================================================================================
async def show_admin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str):
    await update.callback_query.edit_message_text(msg, reply_markup=get_admin_start_buttons())

async def show_calendar_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, msg:str, next_state: State, params:Params):
    actual_slots = await ServiceFactory.get_timeslot_service().get_actual_timeslots()
    kb = create_calendar_buttons(actual_slots,  
                                 year=params.year, 
                                 month=params.month, 
                                 next_state=next_state, 
                                 nav_state=params.state, 
                                 is_admin = True)
    await update.callback_query.edit_message_text(msg, reply_markup = kb) 

async def show_range_calendar_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, msg:str, next_state: State, params:Params):
    kb = create_calendar_range_buttons(params.year, params.month, next_state, params.state, set_date=params.date)
    await update.callback_query.edit_message_text(msg, reply_markup = kb) 

async def show_list_timeslot_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, date: datetime.date, text: str, next_state: State, back_state:State):
    list_slot = await ServiceFactory.get_timeslot_service().get_list_timeslot_by_date(date)
    addition_btns = [[InlineKeyboardButton(BACK, callback_data=f"state={back_state}&date={date}")]]
    kb = create_timeslots_buttons(list_slot, state=next_state, addition_btns=addition_btns, is_admin=True)
    await update.callback_query.edit_message_text(text, reply_markup = kb)

async def show_confirm_msg(update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str, callback_data_confirm: str, callback_data_cancel: str):
    kb = create_confirm_keyboard(callback_data_confirm, callback_data_cancel)
    await update.callback_query.edit_message_text(msg, reply_markup = kb)
#==================================================================================================================================
async def show_time_picker(update: Update, context: ContextTypes.DEFAULT_TYPE, msg:str, date: datetime.date, time: datetime.time = None, default_prefix: State = None, confirm_action:State=None, cancel_action:State=None):
    kb = create_time_picker(date, time, default_prefix, confirm_action, cancel_action)
    await update.callback_query.edit_message_text(msg, reply_markup = kb)