from pydantic import BaseModel
from typing import List
from dto.models import UserDTO


class UserPage(BaseModel):
    items:List[UserDTO]
    total:int
    page:int
    total_page:int

class UserList(BaseModel):
    list_items: List[UserDTO]
    total_count: int