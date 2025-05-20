from pydantic import BaseModel
from pydantic.config import ConfigDict
from datetime import datetime, date, time
from typing import List

class UserDTO(BaseModel):
    id:int
    tg_id:int
    username: str | None
    first_name: str | None
    last_name: str | None
    lock_at: datetime | None
    reserve: float
    remind_inactive:bool
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)

class DayDTO(BaseModel):
    id:int
    date:date
    lock:bool
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)

class TimeSlotDTO(BaseModel):
    id:int
    time:time
    date:date | None
    dayweek:int | None
    max_capacity:int
    capacity:int
    duration:int
    hide:bool
    lock:bool
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)

class BookingDTO(BaseModel):
    id:int
    user_id: int
    time_slot_id: int
    date: datetime
    status: str
    created_at:datetime
    updated_at:datetime

    user: UserDTO
    time_slot: TimeSlotDTO

    model_config = ConfigDict(from_attributes=True)
    