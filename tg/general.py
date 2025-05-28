from telegram.ext import Application
from telegram.constants import ParseMode
from utils.utils import *
from tg.constants import BOT_START_NOTIFICATION
from scheduler.scheduler_holder import SchedulerHolder
from reminder.daily_reminder import restart_reminder
from tg.bot_holder import BotAppHolder
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from tg.handlers import start, button_handler
import asyncio
import signal



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

    await asyncio.gather(*list_task)


async def run_bot(token:str, stop_event:asyncio.Event):
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    await application.initialize()
    await on_startup(application)
    await application.updater.start_polling()
    await application.start()

    await stop_event.wait()

    await application.updater.stop()
    await application.stop()
    await application.shutdown()
    await on_shutdown(application)
    

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

