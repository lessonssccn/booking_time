from telegram.ext import Application
from telegram.constants import ParseMode
from utils.utils import *
from tg.constants import BOT_START_NOTIFICATION
from scheduler.scheduler_holder import SchedulerHolder

async def on_startup(application: Application):
    try:
        SchedulerHolder.init_scheduler()

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
        print("🟢 Бот запущен")
    except Exception as e:
        print(f"Ошибка при запуске: {e}")


async def on_shutdown(application: Application):
    """Остановка планировщика при завершении работы бота"""
    SchedulerHolder.stop_scheduler()
    print("🔴 Планировщик задач остановлен")

