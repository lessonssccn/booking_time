from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
from tg.handlers import start, button_handler

# Загружаем переменные из .env
load_dotenv()

# Основная функция
def main():
    # Чтение токена из .env
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Токен не найден в .env файле. Убедитесь, что переменная TELEGRAM_BOT_TOKEN задана.")

    # Создаем приложение и регистрируем обработчики
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()