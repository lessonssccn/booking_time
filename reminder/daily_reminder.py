from apscheduler.schedulers.asyncio import AsyncIOScheduler
from settings.settings import settings
from services.service_factory import ServiceFactory
from apscheduler.triggers.cron import CronTrigger
from notifications.constants import *
from tg.keyboards.keyboards import get_user_start_buttons 

DAILY_REMINDER_ID = "daily_reminder"

async def daily_reminder_func() -> None:
    print("daily_reminder_func start")
    try:
        list_user = await ServiceFactory.get_booking_service().get_inactive_users_missing_future_bookings()
        await ServiceFactory.get_notification_service().send_message_to_users(list_user, REMINDER_TEXT, reply_markup=get_user_start_buttons())
    except Exception as e:
        print(f"daily_reminder_func fail error = {e}")
    print("daily_reminder_func finish")
    

async def restart_reminder(scheduler:AsyncIOScheduler) -> None:
    time = settings.daily_reminder_time
    job = scheduler.get_job(DAILY_REMINDER_ID)
    print(job)
    if job:
        scheduler.remove_job(DAILY_REMINDER_ID)
        print("remove old reminder")
    trigger = CronTrigger(hour=time.hour, minute=time.minute)
    job = scheduler.add_job(daily_reminder_func, trigger=trigger, id=DAILY_REMINDER_ID)
    print(job)
    print("add new reminder")
