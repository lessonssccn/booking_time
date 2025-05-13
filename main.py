from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import locale
from settings.settings import settings
from tg.bot_holder import BotAppHolder
from tg.handlers import start, button_handler
from tg.general import on_startup, on_shutdown

locale.setlocale(locale.LC_TIME, settings.bot_locale)
# Основная функция
def main():
    # Чтение токена из .env
    token = settings.telegram_bot_token
    if not token:
        raise ValueError("Токен не найден в .env файле. Убедитесь, что переменная TELEGRAM_BOT_TOKEN задана.")

    # Создаем приложение и регистрируем обработчики
    # application = Application.builder().token(token).build()
    application = Application.builder().token(token).post_init(on_startup).post_shutdown(on_shutdown).build()
    BotAppHolder.set_app(application)
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()