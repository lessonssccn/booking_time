from tg.keyboards.kb_text import *
FIRST_MSG = "Бот для записи на занятия\nЕсли что-то не работает свяжитесь с @step_sccn\nБот поддерживате только две команды /start и /help остальное делатеться через кнопки"
USER_BOOKING_LIST = "Ваши бронирования актуально на {date}\n🟢 - подтвержденная бронь\n🟡 - заявка не подтвержденна\n🔴 - завяка отклонена\n⚪ - отменнена пользователя\n⚫ - отмена админа"
SELECTE_DATE = "Выберите 🗓️ дату:"
SELECTE_TIME = "Вы выбрали 🗓️ {date}\nВыберите 🕒 время:"
CONFIRM_BOOKING_SLOT = "Подтвердить запись:\n🗓️ {date}\n🕒 {time}"
TEMPLATE_NOTIFICATION_CHANNAL = "{msg}\nПользователь {first_name} (@{username})"
SUCCESS_BOOKING = "✅ Вы успешно запбронировали время:\n🗓️ {date}\n🕒 {time}"
SUCCESS_BOOKING_CHANNAL_MSG = "✅ Забронировал время\n🗓️ {date}\n🕒 {time}"
CONFIRM_BOOKING_ADMIN_MSG = "{first_name} (@{username})\nЗабронировал\n🗓️ {date}\n🕒 {time}"
DETAILS_BOOKING = "Ваше бронирование\nКогда: {date}\nСтатус: {icon}\nВремя бронирования:{created_at}"
CONFIRM_UNBOOKING = "Подтвердить удалние брони:\n🗓️ {date}\n🕒 {time}"
SUCCESS_UNBOOKING = "✅ Вы отменили бронирование\n🗓️ {date}\n🕒 {time}"
SUCCESS_UNBOOKING_CHANNAL_MSG = "❌ Отменил бронь\n🗓️ {date}\n🕒 {date}"
BOT_START_NOTIFICATION = (
            "🤖 <b>Бот запущен {date}!</b>\n"
            "🆔 ID: <code>{bot_id}</code>\n"
            "👤 Имя: @{bot_username}\n"
            "✅ Готов к работе!"
        )


NOT_ADMIN = "❌ Вы не админ"
ADD_TIMESLOT_CANCEL = "✋ Создание слота отменено"
REMOVE_TIMESLOT_CANCEL =  "✋ Удаление слота отменено"
UNBOOKING_DAY_CANCEL =  "✋ Отмена всех бронирование за день отменна"
TIMESLOT_CREATED = "✅ Слот создан\n🗓️ Дата: {date}\n🕒 Время: {time}"
TIMESLOT_NOT_CREATED = "❌ Не удалось создать слот\n🗓️ Дата: {date}\n🕒 Время: {time}"
TIMESLOT_REMOVED = "✅ Слот удален\n🗓️ Дата: {date}\n🕒 Время: {time}"
TIMESLOT_NOT_REMOVED = "❌ Не удалить слот\n🗓️ Дата: {date}\n🕒 Время: {time}"
TIMESLOT_LOCKED = "✅ Слот 🔒 заблокирован\n🗓️ Дата: {date}\n🕒 Время: {time}"
TIMESLOT_UNLOCKED = "✅ Слот 🔓 разблокирован\n🗓️ Дата: {date}\n🕒 Время: {time}"
TIMESLOT_NOT_LOCKED = "❌ Не удалось заблокировать/разблокировать слот\n🗓️ Дата: {date}\n🕒 Время: {time}"
TIMESLOT_HIDDEN = "✅ Слот 🕶️ скрыт\n🗓️ Дата: {date}\n🕒 Время: {time}"
TIMESLOT_SHOW = "✅ Слот 💡 показан\n🗓️ Дата: {date}\n🕒 Время: {time}"
TIMESLOT_NOT_HIDDEN = "❌ Не удалось скрыть/показать слот\n🗓️ Дата: {date}\n🕒 Время: {time}"
TIMESLOT_CREATE_SELECT_TIME = "Созадние слота\n🗓️ Дата: {date}\nУкажите 🕒 время, на которое надо создать слот"
TIMESLOT_ALREADY_CREATED = "\nУже созданные тайм слоты:\n{list_slot}"

CONFIRM_REMOVE = "Удалить слот\n🗓️ {date}\n🕒 {time}"
CONFIRM_MSG_UNBOOKING_DAY = "Точно ❌ отменить все бронирования❓\n🗓️ {date}"
DAY_LOCKED = "✅ День 🔒 заблокирован\n🗓️ Дата: {date}\n"
DAY_UNLOCKED = "✅ День 🔓 разблокирован\n🗓️ Дата: {date}\n"
DAY_NOT_LOCKED = "❌ Не удалось заблокировать/разблокировать день\n🗓️ Дата: {date}"

CHOOSE_DATE_ADD_SLOT = "На какую дату 🗓️ создать слот:"
CHOOSE_DATE_REMOVE_SLOT = "C какой даты 🗓️ удалить слот слот:"
CHOOSE_DATE_LOCK_SLOT = "На какую дату 🗓️ заблокировать слот:"
CHOOSE_DATE_HIDDEN_SLOT = "На какую дату 🗓️ скрыть слот:"

SELECT_TIME_ADD_SLOT = "🗓️ Дата {date}\nНа какое время 🕒:"
CHOOSE_SLOT_REMOVE = "Вы выбрали 🗓️ {date}\nВыберите 🕒 слот, который надо удалить:"
CHOOSE_SLOT_LOCK = "Вы выбрали 🗓️ {date}\nВыберите 🕒 слот, который надо за(раз)блокировать:"
CHOOSE_SLOT_HIDDEN = "Вы выбрали 🗓️ {date}\nВыберите 🕒 слот, который надо скрыть/показать:"

SUCCESS_CONFIRM_BOOKING_FOR_CLIENT = "🟢 Бронирование одобренно\n🗓️ {date}\n🕒 {time}"
SUCCESS_REJECT_BOOKING_FOR_CLIENT = "🔴 Бронирование отклоненно\n🗓️ {date}\n🕒 {time}"
SUCCESS_CONFIRM_BOOKING_FOR_ADMIN = "🟢 Бронирование одобренно\n🗓️ {date}\n🕒 {time}\n👤 {name} @{username}\n🆔 tg_id = {tg_id}"
SUCCESS_REJECT_BOOKING_FOR_ADMIN = "🔴 Бронирование отклоненно\n🗓️ {date}\n🕒 {time}\n👤 {name} @{username}\n🆔 tg_id = {tg_id}"

FAIL_MATCH_BOOKING = "❌ Не удалось подтвердить бронь с id={id}"
SUCCESS_CANCEL_BOOKING_ADMIN_FOR_CLIENT = "⚫ Бронирование отменно администратором\n🗓️ {date}\n🕒 {time}"
SUCCESS_CANCEL_BOOKING_ADMIN_FOR_ADMIN = "⚫ Бронирование отменно администратором\n🗓️ {date}\n🕒 {time}\n👤 {name} @{username}\n🆔 tg_id = {tg_id}" 

DAY_LOCKE_SELECT = "Какой день 🗓️ заблокировать/разблокировать"
DAY_UNBOOKING = "На какой день отменить все бронирования 🗓️ ?"

ERROR_MSG = "❌ ERROR"

ADMIN_BOOKING_LIST= "Бронирования на {date}\nактульно на {actual_date}\n🟢 - подтвержденная бронь\n🟡 - заявка не подтвержденна\n🔴 - завяка отклонена\n⚪ - отменнена пользователя\n⚫ - отмена админа"

BOOKING_DETAILS_ADMIN = "🗓️ Дата {date}\n🕒 Время {time}\n👤 {name} @{username}\n🆔 tg_id = {tg_id}"