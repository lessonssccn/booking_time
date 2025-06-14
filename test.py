from services.service_factory import ServiceFactory
from scheduler.scheduler_holder import SchedulerHolder
from notifications.notification_func import prfix_reminder
from database.backup import backup_db, backup_jobs
import asyncio



async def test_booking_service_get_inactive_users_missing_future_bookings() -> None:
    await SchedulerHolder.init_scheduler()
    service = await ServiceFactory.get_booking_service(0)
    result = await service.get_inactive_users_missing_future_bookings()
    print(result)

async def test_prfix_reminder() -> None:
    print(prfix_reminder(60))
    print(prfix_reminder(80))
    print(prfix_reminder(15, False))


async def test_back_up() -> None:
    print(await backup_db())
    print(await backup_jobs())

if __name__ == "__main__":
    asyncio.run(test_back_up())
