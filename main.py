import locale
from settings.settings import settings

from tg.general import run_bot

locale.setlocale(locale.LC_TIME, settings.bot_locale)
def main():
    token = settings.telegram_bot_token
    run_bot(token)


if __name__ == "__main__":
    main()