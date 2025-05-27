from telegram.ext import Application
from telegram.constants import ParseMode
from utils.utils import *
from tg.constants import BOT_START_NOTIFICATION
from scheduler.scheduler_holder import SchedulerHolder
from reminder.daily_reminder import restart_reminder
from tg.bot_holder import BotAppHolder
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from tg.handlers import start, button_handler

def run_bot(token:str):
    application = Application.builder().token(token).post_init(on_startup).post_shutdown(on_shutdown).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

async def on_startup(application: Application):
    try:
        BotAppHolder.set_app(application)
        await SchedulerHolder.init_scheduler()
        await restart_reminder(await SchedulerHolder.get_scheduler_async())

        channel_id = get_channel_id()
            
        bot = application.bot
        message = BOT_START_NOTIFICATION.format(date = datetime.datetime.now(), bot_id = bot.id, bot_username = bot.username)
        await bot.send_message(
            chat_id=channel_id,
            text=message,
            parse_mode=ParseMode.HTML
        )
        
        print(f"🟢 Бот {bot.username} запущен")
    except Exception as e:
        print(f"Ошибка при запуске {application.bot.username}: {e}")


async def on_shutdown(application: Application):
    """Остановка планировщика при завершении работы бота"""
    print(f"Остановка бота {application.bot.username}")
    try:
        await SchedulerHolder.stop_scheduler()
        print(f"🔴 Бот {application.bot.username} остановлен")
    except Exception as e:
        print(f"Ошибка при остановке {application.bot.username}: {e}")

