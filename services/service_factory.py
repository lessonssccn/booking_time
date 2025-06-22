from services.user_service import UserService
from repositories.user_repository import UserRepository

from services.day_service import DayService
from repositories.day_repository import DayRepository

from services.timeslot_service import TimeslotService
from repositories.timeslot_repository import TimeslotRepository

from services.booking_service import BookingService
from repositories.booking_repository import BookingRepository

from services.admin_service import AdminService
from repositories.admin_repository import AdminRepository

from services.channel_service import ChannelService
from repositories.channel_repository import ChannelRepository

from tg.bot_holder import BotAppHolder
from services.notifications_service import NotificationService
from scheduler.scheduler_holder import SchedulerHolder
from services.scheduler_service import SchedulerService

from services.booking_reminder_service import BookingReminderService
from cache.cache_holder import CacheHolder

class ServiceFactory:

    @staticmethod
    async def get_admin_service(bot_id:int)->AdminService:
        return AdminService(UserRepository(), AdminRepository(await CacheHolder.get_admin_cache()),await ServiceFactory.get_notification_service(bot_id))

    @staticmethod
    async def get_channel_service(bot_id:int)->ChannelService:
        return ChannelService(ChannelRepository(await CacheHolder.get_channel_cache()),await ServiceFactory.get_notification_service(bot_id))

    @staticmethod
    async def get_user_service(bot_id:int) -> UserService:
        return UserService(UserRepository(), await ServiceFactory.get_notification_service(bot_id))

    @staticmethod    
    async def get_timeslot_service(bot_id:int) -> TimeslotService:
        return TimeslotService(TimeslotRepository(), DayRepository(), BookingRepository(), UserRepository(), await ServiceFactory.get_notification_service(bot_id))
    
    @staticmethod
    async def get_day_service(bot_id:int) -> DayService:
        return DayService(DayRepository(), await ServiceFactory.get_notification_service(bot_id))
    
    @staticmethod
    async def get_booking_service(bot_id:int) -> BookingService:
        return BookingService(BookingRepository(), TimeslotRepository(), UserRepository(), DayRepository(), await ServiceFactory.get_booking_reminder_service(bot_id), await ServiceFactory.get_notification_service(bot_id))

    @staticmethod
    async def get_notification_service(bot_id:int) -> NotificationService:
        return NotificationService(await BotAppHolder.get_app(bot_id), AdminRepository(await CacheHolder.get_admin_cache()), ChannelRepository(await CacheHolder.get_channel_cache()))
    
    @staticmethod
    async def get_scheduler_service() -> SchedulerService:
        return SchedulerService(await SchedulerHolder.get_scheduler_async())
        
    @staticmethod
    async def get_booking_reminder_service(bot_id:int) -> BookingReminderService:
        return BookingReminderService(bot_id, await ServiceFactory.get_scheduler_service(), ChannelRepository(await CacheHolder.get_channel_cache()))