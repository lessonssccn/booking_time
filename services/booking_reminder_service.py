from dto.models import BookingDTO
from services.scheduler_service import SchedulerService
from services.notifications_service import NotificationService
from repositories.admin_repository import AdminRepository
from repositories.channel_repository import ChannelRepository
from tg.bot_holder import BotAppHolder
from typing import List
from notifications.notification_func import create_user_notification_booking_msg, create_admin_notification_booking_msg, prfix_reminder
import datetime
from settings.settings import settings
from telegram.constants import ParseMode
from cache.cache_holder import CacheHolder

class BookingReminderService:
    def __init__(self, bot_id:int, scheduler_service: SchedulerService, channel_repo:ChannelRepository, reminder_offsets_minutes:List[int]=[60,15,5]):
        self.scheduler_service = scheduler_service
        self.reminder_offsets_minutes = reminder_offsets_minutes
        self.bot_id = bot_id
        self.channel_repo = channel_repo
        self.template_job_id = "rb_{bot_id}_{to}_{id}_{offset}"

    async def add_booking(self, booking:BookingDTO): 
        await self.add_reminder_for_user(booking)
        await self.add_reminder_for_channel(booking)

    async def remove_booking(self, booking:BookingDTO):
        await self.remove_reminder_for_user(booking)
        await self.remove_reminder_for_channel(booking)

    async def add_reminder_for_channel(self, booking:BookingDTO):
        channel = await self.channel_repo.get_channel(self.bot_id)
        if channel:
            await self.add_reminder(booking.id, booking.date, channel.channel_id, create_admin_notification_booking_msg(booking))

    async def add_reminder_for_user(self, booking:BookingDTO):
        await self.add_reminder(booking.id, booking.date, booking.user.tg_id, create_user_notification_booking_msg(booking), booking.user.reminder_minutes_before)

    async def remove_reminder_for_channel(self, booking:BookingDTO):
        channel = await self.channel_repo.get_channel(self.bot_id)
        if channel:
            await self.remove_reminder(booking.id, channel.channel_id)

    async def remove_reminder_for_user(self, booking:BookingDTO):
        await self.remove_reminder(booking.id, booking.user.tg_id)

    async def add_reminder(self, booking_id:int, booking_time:datetime.datetime, chat_id:int, text:str, reminder_offsets_minutes=None):
        if reminder_offsets_minutes == None:
            reminder_offsets_minutes = self.reminder_offsets_minutes

        for offset in reminder_offsets_minutes:
            job_id = self.template_job_id.format(bot_id=self.bot_id,to=chat_id, id = booking_id, offset = offset)
            when = booking_time - datetime.timedelta(minutes=offset)
            text_with_prefix = f"{prfix_reminder(offset)}\n{text}"
            await self.scheduler_service.add_job(send_reminde, job_id = job_id, when=when, args=(self.bot_id, chat_id, text_with_prefix))

    async def remove_reminder(self, booking_id:int, chat_id:int):
        for offset in settings.reminder_minutes_before:
            job_id = self.template_job_id.format(bot_id=self.bot_id, to=chat_id, id = booking_id, offset = offset)
            await self.scheduler_service.remove_job(job_id)


async def send_reminde(bot_id:int, chat_id:int, text:str):
    notification_service = NotificationService(await BotAppHolder.get_app(bot_id),
                                               AdminRepository(await CacheHolder.get_admin_cache()),
                                               ChannelRepository(await CacheHolder.get_channel_cache()))
    await notification_service.send_message(chat_id, text, parse_mode=ParseMode.HTML)

