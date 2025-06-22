from telegram import Update
from telegram.ext import ContextTypes
import subprocess
from settings.settings import settings
from database.backup import backup_db, backup_jobs
import os
import asyncio
from services.service_factory import ServiceFactory

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot_id = context.bot.id
    total_attempt = context.bot_data.get(user_id, 0)
    print("update_command", total_attempt)

    admin_service = await ServiceFactory.get_admin_service(bot_id)
    if not await admin_service.is_admin(user_id, bot_id):
        return
    
    args = context.args

    if not args or len(args) == 0:
        return

    password = args[0]

    if password != settings.admin_password:
        total_attempt +=1
        context.bot_data[user_id] = total_attempt
        return

    await update.message.reply_text("Начинаю обновление...")
    total_attempt=0
    context.bot_data[user_id] = total_attempt

    script_path = settings.bot_update_script

    try:
        subprocess.Popen(
            [script_path],
            stdout=open(settings.bot_update_log, "w"),
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            close_fds=True
        )
        await update.message.reply_text("Обновление запущено. Бот будет перезапущен.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при запуске обновления: {e}")

async def send_file_to_channel(bot, file_path):
    try:
        with open(file_path, 'rb') as file:
            await bot.send_document(chat_id=settings.telegram_channel_id, document=file)
            print(f"Файл {file_path} отправлен!")
    except Exception as e:
        print(f"Ошибка при отправке {file_path}: {e}")

async def backup_and_send(bot):
    backup_db_path = await backup_db()
    await send_file_to_channel(bot, backup_db_path)
    await asyncio.to_thread(os.remove, backup_db_path)
    backup_jobs_path = await backup_jobs()
    await send_file_to_channel(bot, backup_jobs_path)
    await asyncio.to_thread(os.remove, backup_jobs_path)

async def backup_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await backup_and_send(context.bot)
    except Exception as e:
        print(f"backup error {e}")
