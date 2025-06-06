USER_INFO = "👤 {name} @{username}\n🆔 tg_id = {tg_id}\n🆔 user_id = {user_id}\ncreate_at = {date}"
POSTFIX_NOTIFICATION_CHANNAL = "{msg}\nПользователь {first_name} (@{username})"

SUCCESS_BOOKING_MSG = "✅ Пользователь забронировал время\n🗓️ {date}\n👤 {name} @{username}"
SUCCESS_UNBOOKING_MSG = "❌ Пользователь отменил бронь\n🗓️ {date}\n👤 {name} @{username}"
SUCCESS_UNBOOKING_ADMIN_MSG = "⚫ Администратор отменил бронь\n🗓️ {date}\n👤 {name} @{username}"
SUCCESS_UNBOOKING_ADMIN_MSG_FOR_USER = "⚫ Администратор отменил вашу бронь на\n🗓️ {date}"
SUCCESS_CONFIRM_BOOKING_MSG = "🟢 Бронирование одобренно\n🗓️ {date}\n👤 {name} @{username}"
SUCCESS_CONFIRM_BOOKING_MSG_FOR_USER = "🟢 Ваша бронь подтверждена\n🗓️ {date}"
SUCCESS_REJECT_BOOKING_MSG = "🔴 Бронирование отклонено\n🗓️ {date}\n👤 {name} @{username}"
SUCCESS_REJECT_BOOKING_MSG_FOR_USER = "🔴 Администратор не подтвердил вашу бронь\n🗓️ {date}\nВозможно вам подойдет другой день"
SUCCESS_WATCH_BOOKING_MSG = "✅ Пользователь начал отслеживать слот\n🗓️ {date}\n👤 {name} @{username}"
SUCCESS_UNWATCH_BOOKING_MSG = "✅ Пользователь перестал отслеживать слот\n🗓️ {date}\n👤 {name} @{username}"
WATCH_BOOKING_FREE_MSG = "✅ Время для записи свободно\n🟢 Можете записаться, подтвердите запись\n🗓️ {date}"

SUCCESS_TIMESLOT_CREATED = "✅ Слот успешно создан\n🗓️ Дата: {date}\n🕒 Время: {time}"
SUCCESS_TIMESLOT_REMOVED = "✅ Слот успешно ❌ удален\n🗓️ Дата: {date}\n🕒 Время: {time}"
SUCCESS_TIMESLOT_LOCKED = "✅ Слот успешно 🔒 заблокирован\n🗓️ Дата: {date}\n🕒 Время: {time}"
SUCCESS_TIMESLOT_UNLOCKED = "✅ Слот успешно 🔓 разблокирован\n🗓️ Дата: {date}\n🕒 Время: {time}"
SUCCESS_TIMESLOT_HIDDEN = "✅ Слот успешно 🕶️ скрыт\n🗓️ Дата: {date}\n🕒 Время: {time}"
SUCCESS_TIMESLOT_SHOW = "✅ Слот успешно 💡 показан\n🗓️ Дата: {date}\n🕒 Время: {time}"

COPY_SCHEDULE_RESULT = "Копирование расписания завершенно\n🗓️ {date_src_start} - {date_src_end}\n🗓️ {date_des_start} - {date_des_end}\nБыло скопированно {count} слотов"

SUCCESS_DAY_LOCKED = "✅ День успешно 🔒 заблокирован\n🗓️ Дата: {date}\n"
SUCCESS_DAY_UNLOCKED = "✅ День успешно 🔓 разблокирован\n🗓️ Дата: {date}\n"

LIST_USER_HOW_GET_MSG_FREE_SLOT = "Пользоватлеи получивышие уведомления, об осовобождении слота\n{list_user}"
SHORT_USER_INFO = "{name} @{username}"