import locale
from settings.settings import settings
from tg.general import run_bots
import asyncio


locale.setlocale(locale.LC_TIME, settings.bot_locale)

async def main():
    await run_bots(settings.telegram_bot_token)

if __name__ == "__main__":
   asyncio.run(main())  