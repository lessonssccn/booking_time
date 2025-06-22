from dao.base_dao import BaseDAO
from database.models import Channel

class ChannelDao(BaseDAO[Channel]):
    model = Channel
