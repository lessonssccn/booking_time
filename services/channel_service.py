from repositories.channel_repository import ChannelRepository
from services.notifications_service import NotificationService
from dto.models import ChannelDTO
from services.const_text import SUCCESS_ADD_CHANNEL, SUCCESS_REMOVE_CHANNEL
from utils.utils import get_msg_channel
from errors.errors import *


class ChannelService:
    def __init__(self, channel_repo:ChannelRepository, notification_service :NotificationService):
        self.channel_repo = channel_repo
        self.notification_service = notification_service

    async def add_channel(self, channel_id, bot_id)->ChannelDTO:
        channel = await self.channel_repo.find_channel(bot_id)
        if channel:
            raise BookingError(ErrorCode.CHANNEL_ALREADY_SET, channel_id=channel_id, bot_id = bot_id)
        channel = await self.channel_repo.add_channel(channel_id, bot_id)
        msg = get_msg_channel(channel, SUCCESS_ADD_CHANNEL)
        await self.notification_service.send_notification_to_channel(msg)
        await self.notification_service.send_message_to_admin(msg)
        return channel

    
    async def remove_chanel(self, bot_id)->ChannelDTO:
        channel = await self.channel_repo.remove_channel(bot_id)
        msg = get_msg_channel(channel, SUCCESS_REMOVE_CHANNEL)
        await self.notification_service.send_notification_to_channel(msg, channel_id=channel.channel_id)
        await self.notification_service.send_message_to_admin(msg)
        return channel
       

    async def find_channel(self, bot_id)->ChannelDTO:
        return await self.channel_repo.find_channel(bot_id)
