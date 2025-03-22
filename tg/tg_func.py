from telegram import Update
from telegram.ext import ContextTypes
from tg.tg_func_admin import process_admin_action
from services.service_factory import ServiceFactory
from tg.keyboards.keyboards import *
from utils.utils import *
from tg.constants import *
from errors.errors import BaseError, UNKNOWN_ERROR_MSG, UNKNOWN_ERROR_NOTIFICATION
from tg.tg_notifications import send_notification_to_channel, send_msg_to_admin
from tg.callback_params import extract_callback_data, Params
from utils.booking_status import get_status_booking_icon
from tg.states.states import State

USER_ACTIONS = {
    State.USER_SHOW_CALENDAR: "show_calendar",
    State.USER_SHOW_TIMESLOTS: "show_time_slots",
    State.USER_SHOW_CONFIRM_BOOKING: "show_confirm_booking",
    State.USER_SHOW_CONFIRM_UNBOOKING: "show_confirm_unbooking",

    State.USER_BOOKING: "booking",
    State.USER_UNBOOKING: "unbooking",
    State.USER_SHOW_LIST_MY_BOOKING: "show_list_my_booking",
    State.USER_BOOKING_DETAILS: "show_booking_details",
}

async def process_start_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        user = await ServiceFactory.get_user_service().get_or_create_user(user.id, user.username, user.first_name, user.last_name)
        await update.message.reply_text(FIRST_MSG, reply_markup=create_start_keyboard(update.effective_user.id))
    except BaseError as e:
        await update.message.reply_text(e.get_user_msg(), reply_markup=create_start_keyboard(update.effective_user.id))
    except:
        await update.message.reply_text(UNKNOWN_ERROR_MSG)

async def process_press_btn(update: Update, context: ContextTypes.DEFAULT_TYPE, data:str):
    try:
        if data == str(State.IGNORE):
            return
        params = extract_callback_data(data)
        if params.state.is_admin_state():
            await process_admin_action(update, context, params)
        else:
            function_name = USER_ACTIONS[params.state]
            function = globals()[function_name]
            await function(update, context, params)
    except BaseError as e:
        print(e)
        await process_booking_error(update, context, data, e)
    except Exception as e:
        print(e)
        await process_unknown_error(update, context, data, e)

async def process_booking_error(update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data:str, e:BaseError):
    await update.callback_query.edit_message_text(f"({datetime.datetime.now()}) {e.get_user_msg()}", reply_markup=create_start_keyboard(update.effective_user.id))
    await send_notification_to_channel(update, context, e.get_notification_msg()+f"\ntg_id={update.effective_user.id}\ncallback_data={callback_data}")

async def process_unknown_error(update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data:str, e:Exception):
    await update.callback_query.edit_message_text(f"({datetime.datetime.now()}) {UNKNOWN_ERROR_MSG}")
    await send_notification_to_channel(update, context, UNKNOWN_ERROR_NOTIFICATION + f"\ntg_id={update.effective_user.id}\ncallback_data={callback_data}\nerror={e}")
    
async def show_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    actual_slots = await ServiceFactory.get_timeslot_service().get_actual_timeslots()
    await update.callback_query.edit_message_text(SELECTE_DATE, reply_markup = create_calendar_buttons(actual_slots, params.year, params.month))
    
async def show_time_slots(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    tg_id = update.callback_query.from_user.id
    list_timeslot = await ServiceFactory.get_timeslot_service().get_list_timeslot_for_tg_user(params.date, tg_id)
    await update.callback_query.edit_message_text(
        SELECTE_TIME.format(date=params.date),
        reply_markup=create_timeslots_buttons(list_timeslot, State.USER_SHOW_CONFIRM_BOOKING, is_admin=False,addition_btns=[[create_btn_show_calendar(OTHER_DATE, State.USER_SHOW_CALENDAR)]])
    )

async def show_confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    slot = await ServiceFactory.get_timeslot_service().get_timeslot_by_id(params.slot_id)
    await update.callback_query.edit_message_text(
        CONFIRM_BOOKING_SLOT.format(date=slot.date, time=slot.time),
        reply_markup=create_confirm_booking_kb(slot.date, slot.id)
    )

async def booking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    tg_user = update.callback_query.from_user
    booking = await ServiceFactory.get_booking_service().booking(params.slot_id, tg_user.id)
    date = booking.date.date()
    time = booking.date.time()
    await update.callback_query.edit_message_text(
        SUCCESS_BOOKING.format(date = date, time = time),
        reply_markup=create_unbooking_keyboard(booking.id))
    
    await send_notification_to_channel(update, context, SUCCESS_BOOKING_CHANNAL_MSG.format(date=date, time=time))
    await send_msg_to_admin(update, context, 
                            CONFIRM_BOOKING_ADMIN_MSG.format(first_name = tg_user.first_name, username = tg_user.username, date = date, time = time),
                            confirm_admin_booking_keyboard(booking.id))       

async def show_list_my_booking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    tg_id = update.callback_query.from_user.id
    bookings = await ServiceFactory.get_booking_service().get_list_actual_booking(tg_id, params.booking_type, params.page)
    await update.callback_query.edit_message_text(
        USER_BOOKING_LIST.format(date = datetime_to_str_with_second(datetime.datetime.now())),
        reply_markup = create_booking_list_buttons(bookings, params.booking_type))

async def show_booking_details(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    tg_id = update.callback_query.from_user.id
    booking = await ServiceFactory.get_booking_service().get_booking(params.booking_id, tg_id)
    details_msg = DETAILS_BOOKING.format(date = datetime_to_str(booking.date), 
                                         icon = get_status_booking_icon(booking.status), 
                                         created_at = datetime_to_str_with_second(booking.created_at))
    await update.callback_query.edit_message_text(details_msg, reply_markup=create_unbooking_keyboard(booking.id))

async def show_confirm_unbooking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    tg_id = update.callback_query.from_user.id
    booking = await ServiceFactory.get_booking_service().get_booking(params.booking_id, tg_id)
    await update.callback_query.edit_message_text(
        CONFIRM_UNBOOKING.format(date = booking.date.date(), time = booking.date.time()),
        reply_markup=create_confirm_unbooking_kb(booking.id)
    )

async def unbooking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    tg_id = update.callback_query.from_user.id
    deleted_booking = await ServiceFactory.get_booking_service().cancel_booking(params.booking_id, tg_id, False)
    date = deleted_booking.date.date()
    time = deleted_booking.date.time()
    await update.callback_query.edit_message_text(SUCCESS_UNBOOKING.format(date=date, time=time),
                                                   reply_markup=create_start_keyboard(tg_id))
    await send_notification_to_channel(update, context, SUCCESS_UNBOOKING_CHANNAL_MSG.format(date=date, time=time))

