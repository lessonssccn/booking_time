from pydantic import BaseModel, model_serializer
from typing import List
import json

class CreateUserTG(BaseModel):
    tg_id:int
    username:str|None=None
    first_name:str|None=None
    last_name:str|None=None

class UpdateUser(BaseModel):
    tg_id:int|None = None
    remind_inactive:bool|None = None
    reminder_minutes_before:List[int]|None = None

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        data = handler(self)
        if data["reminder_minutes_before"]!=None:
            data["reminder_minutes_before"] = json.dumps(data["reminder_minutes_before"])
        return data