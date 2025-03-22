from enum import Enum

class ErrorCode(Enum):
    USER_NOT_FOUND = 1
    TIMESLOT_NOT_FOUND = 2
    BOOKING_NOT_FOUND = 3
    ERROR_UPDATE_STATUS_BOOKING = 3
    ERROR_UPDATE_CAPACITY = 4
    ERROR_INTEGRITY_CAPACITY = 5
    TIMESLOT_OCCUPIED = 6
    TIMESLOT_OCCUPIED_CURRENT_USER = 7
    ERROR_CREATE_BOOKING = 8
    TIMESLOT_EXIST = 9
    ERROR_CREATE_TIMESLOT = 10
    INCORRECT_PARAM = 11
    ERROR_DELETE_TIMESLOT = 12
    ERROR_UPDATE_TIMESLOT = 13
    ERROR_UPDATE_DAY = 14
    ERROR_ADD_DAY = 15
    ERROR_DAO = 16
    ERROR_ADMIN_MATCH_BOOKING = 17


UNKNOWN_ERROR_MSG = f"💀 Что-то пошло не так\nВыполните команду /start повторно"
UNKNOWN_ERROR_NOTIFICATION = "💀 UNKNOWN_ERROR"

error_code_to_user_msg = {
    ErrorCode.USER_NOT_FOUND:"❌ Ошибка. Выполните команду /start повторно",
    ErrorCode.TIMESLOT_NOT_FOUND:"❌ Выбирете другое время с жтим какие-то проблемы",
    ErrorCode.BOOKING_NOT_FOUND:"❌ Бронь не найдена",
    ErrorCode.ERROR_UPDATE_STATUS_BOOKING:"❌ Проблемы с бронью",
    ErrorCode.ERROR_UPDATE_CAPACITY:"❌ Проблемы с выбранным временем. Попробуйте другое",
    ErrorCode.ERROR_INTEGRITY_CAPACITY:"❌ Проблемы с выбранным временем. Попробуйте другое",
    ErrorCode.TIMESLOT_OCCUPIED:"❌ Время уже занято",
    ErrorCode.TIMESLOT_OCCUPIED_CURRENT_USER:"❌ Вы уже забронировали это время",
    ErrorCode.ERROR_CREATE_BOOKING:"❌ Не удалось забронировать время",
    ErrorCode.TIMESLOT_EXIST: "❌ Слот с таким временем и дайто уже существует",
    ErrorCode.ERROR_CREATE_TIMESLOT: "❌ Не удалось создать тайм слот",
    ErrorCode.INCORRECT_PARAM:"❌ Переданны не верные параметры",
    ErrorCode.ERROR_ADMIN_MATCH_BOOKING: "❌ невозможно подтвердить статус бронирования, бронь отменна клиентом"
}

class BaseError(Exception):
    def __init__(self, error_code:ErrorCode, **kwargs):
        self.error_code = error_code
        self.error_data = dict(kwargs)

    def get_user_msg(self):
        return error_code_to_user_msg.get(self.error_code, UNKNOWN_ERROR_MSG)
    
    def get_notification_msg(self):
        error_text = "❌"+self.error_code.name
        error_parts = [error_text]
        for k, v in self.error_data.items():
            error_parts.append(f"{k} = {v}")
        return "\n".join(error_parts)


class ParamError(BaseError):
    def __init__(self, **kwargs):
        super().__init__(ErrorCode.INCORRECT_PARAM, **kwargs)

class DAOError(BaseError):
    def __init__(self, **kwargs):
        super().__init__(ErrorCode.ERROR_DAO, **kwargs)

class BookingError(BaseError):
    pass

class MatchBookingError(BookingError):
    def __init__(self, **kwargs):
        super().__init__(ErrorCode.ERROR_ADMIN_MATCH_BOOKING, **kwargs)
