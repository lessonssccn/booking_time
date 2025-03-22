from pydantic import BaseModel
from typing import List
from dto.models import BookingDTO
import datetime

class BookingPage(BaseModel):
    items:List[BookingDTO]
    total:int
    page:int
    total_page:int

class NewBooking(BaseModel):
    time_slot_id:int
    user_id:int
    date: datetime.datetime
    status:str = "new"

class UpdateBooking(BaseModel):
    status:str|None = None

class BookingList(BaseModel):
    list_items: List[BookingDTO]
    total_count: int