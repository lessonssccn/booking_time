from dao.base_dao import BaseDAO
from database.models import TimeSlot

class TimeslotDao(BaseDAO[TimeSlot]):
    model = TimeSlot
