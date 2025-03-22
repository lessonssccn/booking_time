from pydantic import BaseModel
from dto.models import DayDTO
import datetime


class DayLock(BaseModel):
    lock:bool

class ResultLockDay(BaseModel):
    success:bool
    lock:bool|None = None

class CreateDay(BaseModel):
    date:datetime.date
    lock:bool = True