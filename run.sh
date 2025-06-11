#!/bin/bash

# Парсим аргументы
while getopts ":d:" opt; do
  case $opt in
    d)
      TARGET_DIR="$OPTARG"
      echo "[INFO] Создаю директорию: $TARGET_DIR"
      mkdir -p "$TARGET_DIR"
      ;;
    \?)
      echo "Использование: $0 [-d директория]" >&2
      exit 1
      ;;
    :)
      echo "Для флага -d требуется аргумент." >&2
      exit 1
      ;;
  esac
done

# Применяем миграции
echo "[INFO] Запускаю миграции..."
alembic upgrade head

# Запускаем приложение
echo "[INFO] Запускаю приложение..."
exec python -u main.py