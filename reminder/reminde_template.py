from typing import List, Tuple
from dto.models import UserDTO
from utils.utils import get_user_info_as_txt

REMINDER_TEXT = "🟢 Вы можете записаться\n🔴 У вас нет записи на ближайшее время\n⚠️ Вы можете отключить отправку уведомлений в настройках (⚙️)"
REMINDER_TEXT_CHECK_STAUS_BOOKING = "Проверте статус бронирования"
USER_WITH_REMINDE = "Пользователти которым были отправлены уведомления:\n"
USER_WITH_ERROR_REMINDE = "Пользователти которым не удалось отправить уведомления:\n"
USER_WITHOUT_BOOKING_NOT_FOUND = "Пользователи без записи не найдены"
SHORT_USER_INFO = "👤 {name} @{username}"

def get_msg_list_user_with_reminde(list_result_reminde:List[Tuple[UserDTO, bool]])->str:
    if len(list_result_reminde) > 0:
        filtred_ok = filter(lambda item: item[1], list_result_reminde)
        filtred_error = filter(lambda item: not item[1], list_result_reminde)
        text_ok = "\n".join(map(lambda item: get_user_info_as_txt(item[0], SHORT_USER_INFO), filtred_ok))
        text_error = "\n".join(map(lambda item: get_user_info_as_txt(item[0], SHORT_USER_INFO), filtred_error))
        msg =  USER_WITH_REMINDE + text_ok + "\n" + USER_WITH_ERROR_REMINDE + text_error
    else:
        msg = USER_WITHOUT_BOOKING_NOT_FOUND
    return msg