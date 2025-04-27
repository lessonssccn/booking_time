from telegram.ext import Application

class BotAppHolder:
    _bot_instance: Application | None = None

    @classmethod
    def set_app(cls, bot: Application) -> None:
        """Устанавливает экземпляр бота."""
        cls._bot_instance = bot

    @classmethod
    def get_app(cls) -> Application:
        """Возвращает экземпляр бота. Вызывает ошибку, если бот не инициализирован."""
        if cls._bot_instance is None:
            raise RuntimeError("Bot not initialized! Call BotHolder.set_bot() first.")
        return cls._bot_instance