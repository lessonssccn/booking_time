from cache.cache import Cache
from dto.models import ChannelDTO
from dao.channel_dao import ChannelDao
from dto.channel_models import CreateChannel
from database.models import Channel
from database.base import get_session, get_session_with_commit
from errors.errors import *

class ChannelRepository:
    def __init__(self, cache:Cache):
        self.cache = cache
        self.channel_dao = ChannelDao()

    async def add_channel(self, channel_id:int, bot_id:int)->ChannelDTO:
        async with get_session_with_commit() as session:
            channel = await self.channel_dao.add(session=session, values=CreateChannel(channel_id=channel_id, bot_id=bot_id).model_dump(exclude_unset=True))
            if not channel:
                raise BookingError(error_code=ErrorCode.ERROR_CREATE_CHANNEL, bot_id = bot_id, channel_id = channel_id)
            
            channel_dto =  ChannelDTO.model_validate(channel)
            await self.cache.put(bot_id, channel_dto)

            return channel_dto
            
    async def get_channel(self, bot_id:int)->ChannelDTO:
        channel_dto = await self.find_channel(bot_id)
        if not channel_dto:
            raise BookingError(error_code=ErrorCode.CHANNEL_NOT_FOUND, bot_id = bot_id)
        return channel_dto


    async def find_channel(self, bot_id:int)->ChannelDTO:
        channel_dto = await self.cache.get(bot_id)
        if channel_dto:
            return channel_dto
        
        async with get_session() as session:
            channel = await self.channel_dao.find_one(session, [Channel.bot_id == bot_id])
            if not channel:
                return None
            channel_dto =  ChannelDTO.model_validate(channel)
            await self.cache.put(bot_id, channel_dto)
            return channel_dto
        

    async def remove_channel(self, bot_id:int)->ChannelDTO:
        async with get_session_with_commit() as session:
            filters = [Channel.bot_id == bot_id]

            channel = await self.channel_dao.find_one(session=session, filters=filters)
            if not channel:
                raise BookingError(error_code=ErrorCode.CHANNEL_NOT_FOUND, bot_id = bot_id)

            result = await self.channel_dao.delete(session=session, filters=filters)
            if result != 1:
                raise BookingError(ErrorCode.ERROR_DELETE_CHANNEL, bot_id = bot_id)
            
            await self.cache.remove(bot_id)
            
            return  ChannelDTO.model_validate(channel)
    