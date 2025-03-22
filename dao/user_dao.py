from dao.base_dao import BaseDAO
from database.models import User

class UserDao(BaseDAO[User]):
    model = User
