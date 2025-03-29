from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import Application
from telegram.constants import ParseMode
from utils.utils import *
from tg.constants import TEMPLATE_NOTIFICATION_CHANNAL, BOT_START_NOTIFICATION


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

async def send_startup_message(application: Application):
    try:
        channel_id = get_channel_id()
        if not channel_id:
            print("Предупреждение: TELEGRAM_CHANNEL_ID не указан в .env, сообщение о запуске не будет отправлено")
            return
            
        bot = application.bot
        message = BOT_START_NOTIFICATION.format(date = datetime.datetime.now(), bot_id = bot.id, bot_username = bot.username)
        await bot.send_message(
            chat_id=channel_id,
            text=message,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        print(f"Ошибка при отправке сообщения о запуске: {e}")