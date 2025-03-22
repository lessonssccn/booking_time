from pydantic import BaseModel
from dto.models import TimeSlotDTO, DayDTO
import datetime
from typing import List

class ResultCreateTimeslot(BaseModel):
    success:bool
    slot_exist:bool = False
    new_slot: TimeSlotDTO | None = None

class CreateTimeslot(BaseModel):
    date:datetime.date|None = None
    time:datetime.time|None = None

class SlotId(BaseModel):
    id:int

class UpdateTimeslot(BaseModel):
    lock:bool|None = None
    hide:bool|None = None
    capacity:int|None = None

class ActualTimeslots(BaseModel):
    min_date:datetime.date
    max_date:datetime.date
    list_timeslot:List[TimeSlotDTO]
    list_locked_day:List[DayDTO]
    