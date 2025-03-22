from dao.base_dao import BaseDAO
from database.models import Day

class DayDao(BaseDAO[Day]):
    model = Day
