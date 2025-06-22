from pydantic import BaseModel

class CreateChannel(BaseModel):
    bot_id:int
    channel_id:int