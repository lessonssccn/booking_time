from services.user_service import UserService
from repositories.user_repository import UserRepository

from services.day_service import DayService
from repositories.day_repository import DayRepository

from services.timeslot_service import TimeslotService
from repositories.timeslot_repository import TimeslotRepository

from services.booking_service import BookingService
from repositories.booking_repository import BookingRepository

class ServiceFactory:
    @staticmethod
    def get_user_service() -> UserService:
        return UserService(UserRepository())

    @staticmethod    
    def get_timeslot_service() -> TimeslotService:
        return TimeslotService(TimeslotRepository(), DayRepository(), BookingRepository(), UserRepository())
    
    @staticmethod
    def get_day_service() -> DayService:
        return DayService(DayRepository())
    
    @staticmethod
    def get_booking_service() -> BookingService:
        return BookingService(BookingRepository(), TimeslotRepository(), UserRepository(), DayRepository())
        