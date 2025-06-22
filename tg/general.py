from telegram.ext import Application
from telegram.constants import ParseMode
from utils.utils import *
from tg.constants import BOT_START_NOTIFICATION, BOT_STOP_NOTIFICATION
from scheduler.scheduler_holder import SchedulerHolder
from reminder.daily_reminder import restart_reminder
from tg.bot_holder import BotAppHolder
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from tg.handlers import start, button_handler, process_channel_msg, process_add_admin, process_remove_admin
from tg.tg_func_service import update_command, backup_handler
from jobs.jobs import restart_shared_jobs
import asyncio
import signal
from settings.settings import settings
from services.service_factory import ServiceFactory

def signal_handler(list_stop_event:List[asyncio.Event]):
    print("\nПолучен сигнал остановки (Ctrl+C)")
    for stop_event in list_stop_event:
        stop_event.set()
    

async def run_bots(token_list:List[str])->None:

    list_task = []
    list_stop_event = []

    for token in token_list:
        stop_event = asyncio.Event()
        list_task.append(asyncio.create_task(run_bot(token, stop_event)))
        list_stop_event.append(stop_event)

   
        
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, lambda : signal_handler(list_stop_event))
    loop.add_signal_handler(signal.SIGTERM, lambda : signal_handler(list_stop_event))

    await SchedulerHolder.init_scheduler()
    await restart_shared_jobs(await SchedulerHolder.get_scheduler_async())

    await asyncio.gather(*list_task)
    await SchedulerHolder.stop_scheduler()


async def run_bot(token:str, stop_event:asyncio.Event):
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler(settings.add_admin_command, process_add_admin))
    application.add_handler(CommandHandler(settings.rm_admin_command, process_remove_admin))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, process_channel_msg))
    
    if settings.bot_update_active:
        application.add_handler(CommandHandler(settings.bot_update_command, update_command))

    if settings.backup_command_active:
        application.add_handler(CommandHandler(settings.backup_command, backup_handler))
    
    
    await application.initialize()
    await on_startup(application)
    await application.updater.start_polling()
    await application.start()

    await stop_event.wait()

    message = BOT_STOP_NOTIFICATION.format(date = datetime.datetime.now(), bot_id = application.bot.id, bot_username = application.bot.username)
    notification_service = await ServiceFactory.get_notification_service(application.bot.id)
    await notification_service.send_notification_to_channel(message,parse_mode=ParseMode.HTML)

    await application.updater.stop()
    await application.stop()
    await application.shutdown()
    await on_shutdown(application)
    

async def on_startup(application: Application):
    try:
        await BotAppHolder.add_app(application)
        bot = application.bot

        await SchedulerHolder.init_scheduler()
        await restart_reminder(bot.id, await SchedulerHolder.get_scheduler_async())

        message = BOT_START_NOTIFICATION.format(date = datetime.datetime.now(), bot_id = bot.id, bot_username = bot.username)
        notification_service = await ServiceFactory.get_notification_service(application.bot.id)
        await notification_service.send_notification_to_channel(message,parse_mode=ParseMode.HTML)
        
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

