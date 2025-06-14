from telegram import Update
from telegram.ext import CallbackContext
import subprocess
from utils.utils import is_admin
from settings.settings import settings
from database.backup import backup_db, backup_jobs
import os
import asyncio

async def who_am_i_command(update:Update, context: CallbackContext):
    try:
        if update.effective_chat and update.effective_chat.type!="private":
            chat_id = update.effective_chat.id
            await context.bot.send_message(chat_id, chat_id)
        else:
            user_id = update.effective_user.id
            await update.message.reply_text(user_id)
    except:
        print("Error finde id")

async def update_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("Неизвестная команда")
        return
    
    args = context.args

    if not args or len(args) == 0:
        await update.message.reply_text("Пароль не указан. Используйте: /update <пароль>")
        return

    password = args[0]

    if password != settings.bot_update_password:
        await update.message.reply_text("Неизвестная команда")
        return

    await update.message.reply_text("Начинаю обновление...")

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

async def backup_handler(update: Update, context: CallbackContext):
    try:
        await backup_and_send(context.bot)
    except Exception as e:
        print(f"backup error {e}")
