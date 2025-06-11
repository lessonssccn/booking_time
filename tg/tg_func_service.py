from telegram import Update
from telegram.ext import CallbackContext
import subprocess
from utils.utils import is_admin
from settings.settings import settings

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
