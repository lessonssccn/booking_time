#!/bin/bash
# Применяем миграции
alembic upgrade head
# Запускаем приложение
exec python main.py