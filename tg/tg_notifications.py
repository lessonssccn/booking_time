from telegram import Update
from telegram.ext import ContextTypes
from utils.utils import *
from tg.constants import TEMPLATE_NOTIFICATION_CHANNAL


async def send_notification_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, msg:str):
    channel_id = get_channel_id()
    if channel_id:
        user = update.callback_query.from_user
        message = TEMPLATE_NOTIFICATION_CHANNAL.format(msg=msg, first_name = user.first_name, username = user.username)
        await context.bot.send_message(chat_id=channel_id, text=message)

async def send_msg_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, msg:str, reply_markup=None):
    await context.bot.send_message(chat_id=get_admin_id(), text=msg, reply_markup=reply_markup)

async def send_msg_to_client(update: Update, context: ContextTypes.DEFAULT_TYPE, tg_id:int, msg:str, reply_markup=None):
    await context.bot.send_message(chat_id=tg_id, text=msg, reply_markup=reply_markup)

