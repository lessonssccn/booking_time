from enum import Enum

class ErrorCode(str,Enum):
    USER_NOT_FOUND = "❌ Юзер не найден"
    TIMESLOT_NOT_FOUND = "❌ Время не найдено"
    BOOKING_NOT_FOUND = "❌ Бронь не найдена"
    ERROR_UPDATE_STATUS_BOOKING = "❌ Проблемы с обновлением статуса брони"
    ERROR_UPDATE_CAPACITY = "❌ Проблемы с выбранным временем. Возможно его уже заняли. Попробуйте другое"
    ERROR_INTEGRITY_CAPACITY = "❌ Проблемы с выбранным временем. Возможно его уже заняли. Попробуйте другое"
    TIMESLOT_OCCUPIED = "❌ Время уже занято"
    TIMESLOT_OCCUPIED_CURRENT_USER = "❌ Вы уже забронировали это время"
    ERROR_CREATE_BOOKING = "❌ Не удалось забронировать время"
    TIMESLOT_EXIST = "❌ Слот с таким временем и дайто уже существует"
    ERROR_CREATE_TIMESLOT = "❌ Не удалось создать тайм слот"
    INCORRECT_PARAM = "❌ Переданны не верные параметры"
    ERROR_DELETE_TIMESLOT = "❌ Не удалось загрузить детали о времени"
    ERROR_UPDATE_TIMESLOT = "❌ Не удалось обновить слот"
    ERROR_UPDATE_DAY = "❌ Не удалось обновить день"
    ERROR_ADD_DAY = "❌ Не удалось добаить день"
    ERROR_DAO = "❌ Ошибка БД"
    ERROR_ADMIN_MATCH_BOOKING = "❌ невозможно изменить статус бронирования, бронь отменена клиентом или это отслеживание или ее не существует"
    ERROR_ADMIN_UPDATE_BOOKING = "❌ неудальс обновить статус брони"
    TIMESLOT_FREE = "❌ Это слот не занят, вы можете его забронировать"
    TIMESLOT_WATCHING_CURRENT_USER = "❌ Вы уже отслеживаете данный слот"
    ERROR_ADMIN_CANCEL_WATCHING = "❌ Администратор не может отменять отслеживания"
    ERROR_CANCEL_BOOKING = "❌ Невозможно отменит бронирование возможно бронь уже отменена"
    ERROR_CREATE_ADMIN = "❌ Не удалось создать админа"
    ADMIN_NOT_FOUND = "❌ Не удалось найти админа"
    ERROR_DELETE_ADMIN = "❌ Не удалось удалить админа"
    ERROR_CREATE_CHANNEL = "❌ Не удалось зарегестрировать канал"
    CHANNEL_NOT_FOUND = "❌ Не удалось найти канал"
    ERROR_DELETE_CHANNEL = "❌ Не удалось удалить канал"
    ADMIN_ALREADY_SET = "❌ Админ уже задан для этого бота"
    CHANNEL_ALREADY_SET = "❌ Канал уже задан для этого бота"


UNKNOWN_ERROR_MSG_CHANNEL = "💀 Что-то пошло не так"
UNKNOWN_ERROR_MSG = "💀 Что-то пошло не так\nВыполните команду /start повторно"
UNKNOWN_ERROR_NOTIFICATION = "💀 UNKNOWN_ERROR"


class BaseError(Exception):
    def __init__(self, error_code:ErrorCode, **kwargs):
        self.error_code = error_code
        self.error_data = dict(kwargs)

    def get_user_msg(self):
        return self.error_code.value
    
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
