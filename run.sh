#!/bin/sh
# Применяем миграции
alembic upgrade head
# Запускаем приложение
python main.py