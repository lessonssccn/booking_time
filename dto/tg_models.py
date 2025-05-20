from pydantic import BaseModel

class CreateUserTG(BaseModel):
    tg_id:int
    username:str|None=None
    first_name:str|None=None
    last_name:str|None=None

class UpdateUser(BaseModel):
    tg_id:int|None = None
    remind_inactive:bool|None = None