from apscheduler.schedulers.asyncio import AsyncIOScheduler
from settings.settings import settings
from services.service_factory import ServiceFactory
from apscheduler.triggers.cron import CronTrigger
from reminder.reminde_template import *
from tg.keyboards.keyboards import get_user_start_buttons, create_booking_kb_admin_reminder
from tg.bot_holder import BotAppHolder

DAILY_REMINDER_ID = "daily_reminder_{bot_id}"

async def reminder_user_without_booking(bot_id) -> None:
    try:
        booking_service = await ServiceFactory.get_booking_service(bot_id)
        list_user = await booking_service.get_inactive_users_missing_future_bookings()
        notification_service = await ServiceFactory.get_notification_service(bot_id)
        result = await notification_service.send_message_to_users(list_user, REMINDER_TEXT, reply_markup=get_user_start_buttons())
        await notification_service.send_notification_to_channel(get_msg_list_user_with_reminde(result))
    except Exception as e:
        print(f"Fail reminder_user_without_booking error = {e}")

async def reminder_admin_check_status_booking(bot_id) -> None:
    try:
        notification_service = await ServiceFactory.get_notification_service(bot_id)
        await notification_service.send_message_to_admin(REMINDER_TEXT_CHECK_STAUS_BOOKING, create_booking_kb_admin_reminder())
    except Exception as e:
        print(f"Fail reminder_admin_check_status_booking  error = {e}")

async def daily_reminder_func(bot_id:int=None) -> None:
    print("daily_reminder_func start")
    #Временно на переходный период
    try:
        if bot_id == None:
            list_bot = await BotAppHolder.get_list_app()
            bot_id = list_bot[0]
    except Exception as e:
        print(f"Fail daily_reminder_func  error = {e}")
        return

    await reminder_user_without_booking(bot_id)
    
    if settings.daily_reminder_admin_check_status_booking:
        await reminder_admin_check_status_booking(bot_id)

    print("daily_reminder_func finish")


async def restart_reminder(bot_id, scheduler:AsyncIOScheduler) -> None:
    time = settings.daily_reminder_time
    job_id = DAILY_REMINDER_ID.format(bot_id=bot_id)

    #временно для удаления старого
    job = scheduler.get_job("daily_reminder")
    if job:
        scheduler.remove_job("daily_reminder")

    job = scheduler.get_job(job_id)
    print(job)
    if job:
        scheduler.remove_job(job_id)
        print("remove old reminder")
    trigger = CronTrigger(hour=time.hour, minute=time.minute)
    job = scheduler.add_job(daily_reminder_func, trigger=trigger, id=job_id, args=(bot_id,))
    print(job)
    print("add new reminder")
