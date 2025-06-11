#!/bin/bash

# Получаем путь к директории, где находится скрипт
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Переходим в эту директорию
cd "$SCRIPT_DIR" || { echo "Не могу перейти в $SCRIPT_DIR"; exit 1; }

# Ищем файл с расширением .service в текущей директории
SERVICE_FILE=$(find . -maxdepth 1 -type f -name "*.service" | head -n1)

if [ -z "$SERVICE_FILE" ]; then
  echo "Файл .service не найден в директории $SCRIPT_DIR"
  exit 1
fi

# Получаем имя сервиса из имени файла
SERVICE_NAME=$(basename "$SERVICE_FILE")

echo "Найден файл сервиса: $SERVICE_NAME"

# Проверяем Git
echo "Проверяю наличие обновлений..."

git fetch origin

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)
BASE=$(git merge-base HEAD origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
  if [ "$LOCAL" = "$BASE" ]; then
    echo "Есть обновления на сервере. Выполняю git pull..."
    git pull origin main || { echo "Ошибка при выполнении git pull"; exit 1; }
  else
    echo "Локальная ветка и удаленная ветка расходятся. Возможно, были локальные коммиты."
    echo "Обновление не выполнено автоматически. Проверьте состояние репозитория."
    exit 1
  fi
else
  echo "Обновлений нет"
  exit 0
fi

# Активируем виртуальное окружение
VENV_PATH="env"
if [ ! -d "$VENV_PATH" ]; then
  echo "Виртуальное окружение не найдено в $VENV_PATH"
  exit 1
fi

source "$VENV_PATH/bin/activate" || { echo "Не могу активировать виртуальное окружение"; exit 1; }

# Выполняем миграции Alembic
ALEMBIC_CMD="$VENV_PATH/bin/alembic"
if [ ! -f "$ALEMBIC_CMD" ]; then
  echo "Alembic не найден в виртуальном окружении. Убедитесь, что он установлен."
  exit 1
fi

echo "Выполняю миграции Alembic..."
$ALEMBIC_CMD upgrade head || { echo "Ошибка при выполнении миграций Alembic"; exit 1; }

# Перезапускаем сервис
echo "Перезапускаю сервис $SERVICE_NAME..."
sudo systemctl restart "$SERVICE_NAME" || { echo "Ошибка при перезапуске сервиса"; exit 1; }

# Проверяем статус сервиса
sudo systemctl is-active --quiet "$SERVICE_NAME"
if [ $? -eq 0 ]; then
  echo "Сервис $SERVICE_NAME успешно перезапущен."
else
  echo "Сервис $SERVICE_NAME не запущен после перезагрузки!" >&2
  exit 1
fi

echo "Все операции успешно завершены."