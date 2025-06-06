from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from tg.tg_func_admin import process_admin_action
from services.service_factory import ServiceFactory
from tg.keyboards.keyboards import *
from utils.utils import *
from tg.constants import *
from errors.errors import BaseError, UNKNOWN_ERROR_MSG, UNKNOWN_ERROR_NOTIFICATION
from tg.callback_params import extract_callback_data, Params
from utils.booking_status import get_status_booking_icon
from tg.states.states import State
from utils.booking_status import get_watch_status

USER_ACTIONS = {
    State.USER_SHOW_CALENDAR: "show_calendar",
    State.USER_SHOW_TIMESLOTS: "show_time_slots",
    State.USER_SHOW_CONFIRM_BOOKING: "show_confirm_booking",
    State.USER_SHOW_CONFIRM_UNBOOKING: "show_confirm_unbooking",

    State.USER_WATCH_SLOT: "watching",
    State.USER_BOOKING_WATCH_SLOT:"booking_watching_slot",
    State.USER_UNWATCHING:"unwatching",

    State.USER_BOOKING: "booking",
    State.USER_UNBOOKING: "unbooking",
    State.USER_SHOW_LIST_MY_BOOKING: "show_list_my_booking",
    State.USER_BOOKING_DETAILS: "show_booking_details",
    State.USER_SHOW_SETTINGS: "show_settings",
    State.USER_SHOW_START_MENU: "show_start_menu",
    State.USER_SHOW_REMINDE_SETTINGS: "show_reminde_settings",
    State.USER_TOGGLE_REMINDE_INACTIVE: "toggle_reminde_inactive",
    State.USER_TOGGLE_REMINDE_BEFORE: "toggle_reminde_before",
}

async def process_start_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        user_service = await ServiceFactory.get_user_service(context.bot.id)
        user = await user_service.get_or_create_user(user.id, user.username, user.first_name, user.last_name)
        await update.message.reply_text(FIRST_MSG.format(date=datetime_to_str(datetime.datetime.now())), reply_markup=create_start_keyboard(update.effective_user.id), parse_mode=ParseMode.HTML)
    except BaseError as e:
        await update.message.reply_text(e.get_user_msg(), reply_markup=create_start_keyboard(update.effective_user.id))
    except Exception as e:
        print(e)
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
    notification_service = await ServiceFactory.get_notification_service(context.bot.id)
    await notification_service.send_notification_to_channel(e.get_notification_msg()+f"\ntg_id={update.effective_user.id}\ncallback_data={callback_data}", tg_user=update.effective_user)

async def process_unknown_error(update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data:str, e:Exception):
    await update.callback_query.edit_message_text(f"({datetime.datetime.now()}) {UNKNOWN_ERROR_MSG}")
    notification_service = await ServiceFactory.get_notification_service(context.bot.id)
    await notification_service.send_notification_to_channel(UNKNOWN_ERROR_NOTIFICATION + f"\ntg_id={update.effective_user.id}\ncallback_data={callback_data}\nerror={e}", tg_user=update.effective_user)
    
async def show_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    timeslot_service = await ServiceFactory.get_timeslot_service(context.bot.id)
    actual_slots = await timeslot_service.get_actual_timeslots()
    await update.callback_query.edit_message_text(SELECTE_DATE, reply_markup = create_calendar_buttons(actual_slots, params.year, params.month))
    
async def show_time_slots(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    timeslot_service = await ServiceFactory.get_timeslot_service(context.bot.id)
    tg_id = update.callback_query.from_user.id
    list_timeslot = await timeslot_service.get_list_timeslot_for_tg_user(params.date, tg_id)
    await update.callback_query.edit_message_text(
        SELECTE_TIME.format(date= date_to_str(params.date)),
        reply_markup=create_timeslots_buttons(list_timeslot, State.USER_SHOW_CONFIRM_BOOKING, is_admin=False,addition_btns=[[create_btn_show_calendar(OTHER_DATE, State.USER_SHOW_CALENDAR)], [create_start_menu_btn()]])
    )

async def show_confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    timeslot_service = await ServiceFactory.get_timeslot_service(context.bot.id)
    slot = await timeslot_service.get_timeslot_by_id(params.slot_id)

    booking_service = await ServiceFactory.get_booking_service(context.bot.id)

    if await booking_service.exsist_actual_booking_by_slot_id_for_tg_id(params.slot_id, update.effective_user.id):
        msg = OCCUPIED_SLOT_CURRENT_USER
        kb = create_skip_booking_kb(slot.date)
    elif await booking_service.exsist_watching_booking_by_slot_id_for_tg_id(params.slot_id, update.effective_user.id):
        msg = WATCHING_SLOT_CURRENT_USER
        kb = create_skip_booking_kb(slot.date)
    elif await booking_service.exsist_actual_booking_by_slot_id(params.slot_id):
        msg = OCCUPIED_SLOT
        kb = create_watch_booking_kb(slot.date, slot.id)
    else:
        msg = CONFIRM_BOOKING_SLOT
        kb = create_confirm_booking_kb(slot.date, slot.id)
        
    await update.callback_query.edit_message_text(get_msg_for_slot(slot, msg),reply_markup=kb)

async def watching(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking_service = await ServiceFactory.get_booking_service(context.bot.id)
    tg_user = update.callback_query.from_user
    booking = await booking_service.watching(params.slot_id, tg_user.id)
    await update.callback_query.edit_message_text(
        get_msg_for_booking(booking, SUCCESS_WATCHING),
        reply_markup=create_unbooking_keyboard(booking.id))

async def booking_watching_slot(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking_service = await ServiceFactory.get_booking_service(context.bot.id)
    tg_user = update.callback_query.from_user
    booking = await booking_service.booking_watching_slot(params.booking_id, tg_user.id)
    await update.callback_query.edit_message_text(
        get_msg_for_booking(booking, SUCCESS_BOOKING),
        reply_markup=create_unbooking_keyboard(booking.id))

async def booking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking_service = await ServiceFactory.get_booking_service(context.bot.id)
    tg_user = update.callback_query.from_user
    booking = await booking_service.booking(params.slot_id, tg_user.id)
    await update.callback_query.edit_message_text(
        get_msg_for_booking(booking, SUCCESS_BOOKING),
        reply_markup=create_unbooking_keyboard(booking.id))
        
async def show_list_my_booking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking_service = await ServiceFactory.get_booking_service(context.bot.id)
    tg_id = update.callback_query.from_user.id
    bookings = await booking_service.get_list_actual_booking(tg_id, params.booking_type, params.page)
    await update.callback_query.edit_message_text(
        USER_BOOKING_LIST.format(date = datetime_to_str_with_second(datetime.datetime.now())),
        reply_markup = create_booking_list_buttons(bookings, params.booking_type))

async def show_booking_details(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking_service = await ServiceFactory.get_booking_service(context.bot.id)
    tg_id = update.callback_query.from_user.id
    booking = await booking_service.get_booking(params.booking_id, tg_id)
    details_msg = DETAILS_BOOKING.format(date = datetime_to_str(booking.date), 
                                         icon = get_status_booking_icon(booking.status), 
                                         created_at = datetime_to_str_with_second(booking.created_at))
    await update.callback_query.edit_message_text(details_msg, reply_markup=create_unbooking_keyboard(booking.id))

async def show_confirm_unbooking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking_service = await ServiceFactory.get_booking_service(context.bot.id)
    tg_id = update.callback_query.from_user.id
    booking = await booking_service.get_booking(params.booking_id, tg_id)

    if booking.status != get_watch_status():
        await update.callback_query.edit_message_text(
            get_msg_for_booking(booking, CONFIRM_UNBOOKING),
            reply_markup=create_confirm_unbooking_kb(booking.id)
        )
    else:
        await update.callback_query.edit_message_text(
            get_msg_for_booking(booking, CONFIRM_UNWATCHING),
            reply_markup=create_confirm_unwatching_kb(booking.id)
        )

async def unbooking(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking_service = await ServiceFactory.get_booking_service(context.bot.id)
    tg_id = update.callback_query.from_user.id
    deleted_booking = await booking_service.cancel_booking(params.booking_id, tg_id, False)
    await update.callback_query.edit_message_text(get_msg_for_booking(deleted_booking, SUCCESS_UNBOOKING),
                                                   reply_markup=create_start_keyboard(tg_id))
    
async def unwatching(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    booking_service = await ServiceFactory.get_booking_service(context.bot.id)
    tg_id = update.callback_query.from_user.id
    deleted_booking = await booking_service.cancel_watching(params.booking_id, tg_id)
    await update.callback_query.edit_message_text(get_msg_for_booking(deleted_booking, SUCCESS_UNWATCHING),
                                                   reply_markup=create_start_keyboard(tg_id))


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    await update.callback_query.edit_message_text(SHOW_SETTINGS_MSG, reply_markup=create_settings_kb())

async def show_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    await update.callback_query.edit_message_text(FIRST_MSG.format(date=datetime_to_str(datetime.datetime.now())), reply_markup=create_start_keyboard(update.effective_user.id), parse_mode=ParseMode.HTML)

async def show_reminde_settings(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    user_service = await ServiceFactory.get_user_service(context.bot.id)
    user = await user_service.get_user_by_tg_id(update.effective_user.id)
    await update.callback_query.edit_message_text(SHOW_REMINDE_SETTINGS_MSG, reply_markup=create_reminde_settings_kb(user))

async def toggle_reminde_inactive(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    user_service = await ServiceFactory.get_user_service(context.bot.id)
    user = await user_service.update_user_reminde_inactive(update.effective_user.id, params.data)
    await update.callback_query.edit_message_text(SHOW_REMINDE_SETTINGS_MSG, reply_markup=create_reminde_settings_kb(user))

async def toggle_reminde_before(update: Update, context: ContextTypes.DEFAULT_TYPE, params:Params):
    user_service = await ServiceFactory.get_user_service(context.bot.id)
    user = await user_service.update_user_reminde_before(update.effective_user.id, params.data)
    await update.callback_query.edit_message_text(SHOW_REMINDE_SETTINGS_MSG, reply_markup=create_reminde_settings_kb(user))