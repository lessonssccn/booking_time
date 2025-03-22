from telegram import Update
from telegram.ext import ContextTypes
from tg.tg_func import *

# Асинхронный обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_start_msg(update, context)

# Асинхронный обработчик нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await process_press_btn(update, context, query.data)
