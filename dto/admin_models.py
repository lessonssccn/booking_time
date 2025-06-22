from pydantic import BaseModel

class CreateAdmin(BaseModel):
    bot_id:int
    user_id:int