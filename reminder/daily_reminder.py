from apscheduler.schedulers.asyncio import AsyncIOScheduler
from settings.settings import settings
from services.service_factory import ServiceFactory
from apscheduler.triggers.cron import CronTrigger
from notifications.constants import *
from tg.keyboards.keyboards import get_user_start_buttons 
from tg.bot_holder import BotAppHolder

DAILY_REMINDER_ID = "daily_reminder_{bot_id}"

async def daily_reminder_func(bot_id:int) -> None:
    print("daily_reminder_func start")
    try:
        booking_service = await ServiceFactory.get_booking_service(bot_id)
        list_user = await booking_service.get_inactive_users_missing_future_bookings()
        notification_service = await ServiceFactory.get_notification_service(bot_id)
        await notification_service.send_message_to_users(list_user, REMINDER_TEXT, reply_markup=get_user_start_buttons())
    except Exception as e:
        print(f"daily_reminder_func fail error = {e}")
    print("daily_reminder_func finish")
    

async def restart_reminder(bot_id, scheduler:AsyncIOScheduler) -> None:
    time = settings.daily_reminder_time
    job_id = DAILY_REMINDER_ID.format(bot_id=bot_id)
    job = scheduler.get_job(job_id)
    print(job)
    if job:
        scheduler.remove_job(job_id)
        print("remove old reminder")
    trigger = CronTrigger(hour=time.hour, minute=time.minute)
    job = scheduler.add_job(daily_reminder_func, trigger=trigger, id=job_id, args=(bot_id,))
    print(job)
    print("add new reminder")
