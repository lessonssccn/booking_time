from dto.models import BookingDTO
from services.scheduler_service import SchedulerService
from services.notifications_service import NotificationService
from tg.bot_holder import BotAppHolder
from typing import List
from notifications.notification_func import create_user_notification_booking_msg, create_admin_notification_booking_msg
from utils.utils import get_channel_id
import datetime
from settings.settings import settings

class BookingReminderService:
    def __init__(self, bot_id:int, scheduler_service: SchedulerService, reminder_offsets_minutes:List[int]=[60,15,5]):
        self.scheduler_service = scheduler_service
        self.reminder_offsets_minutes = reminder_offsets_minutes
        self.bot_id = bot_id
        self.template_job_id = "rb_{bot_id}_{to}_{id}_{offset}"

    async def add_booking(self, booking:BookingDTO): 
        await self.add_reminder_for_user(booking)
        await self.add_reminder_for_channel(booking)

    async def remove_booking(self, booking:BookingDTO):
        await self.remove_reminder_for_user(booking)
        await self.remove_reminder_for_channel(booking)

    async def add_reminder_for_channel(self, booking:BookingDTO):
        chat_id = get_channel_id()
        if chat_id:
            await self.add_reminder(booking.id, booking.date, chat_id, create_admin_notification_booking_msg(booking))

    async def add_reminder_for_user(self, booking:BookingDTO):
        await self.add_reminder(booking.id, booking.date, booking.user.tg_id, create_user_notification_booking_msg(booking), booking.user.reminder_minutes_before)

    async def remove_reminder_for_channel(self, booking:BookingDTO):
        chat_id = get_channel_id()
        if chat_id:
            await self.remove_reminder(booking.id, chat_id)

    async def remove_reminder_for_user(self, booking:BookingDTO):
        await self.remove_reminder(booking.id, booking.user.tg_id)

    async def add_reminder(self, booking_id:int, booking_time:datetime.datetime, chat_id:int, text:str, reminder_offsets_minutes=None):
        if reminder_offsets_minutes == None:
            reminder_offsets_minutes = self.reminder_offsets_minutes

        for offset in reminder_offsets_minutes:
            job_id = self.template_job_id.format(bot_id=self.bot_id,to=chat_id, id = booking_id, offset = offset)
            when = booking_time - datetime.timedelta(minutes=offset)
            await self.scheduler_service.add_job(send_reminde, job_id = job_id, when=when, args=(self.bot_id, chat_id, text))

    async def remove_reminder(self, booking_id:int, chat_id:int):
        for offset in settings.reminder_minutes_before:
            job_id = self.template_job_id.format(bot_id=self.bot_id, to=chat_id, id = booking_id, offset = offset)
            await self.scheduler_service.remove_job(job_id)


async def send_reminde(bot_id:int, chat_id:int, text:str):
    await NotificationService(BotAppHolder.get_app(bot_id)).send_message(chat_id, text)    