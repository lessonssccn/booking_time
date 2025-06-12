#!/bin/bash

# Инициализация флагов
DO_UPDATE=false
DO_MIGRATE=false
DO_RESTART=false
DO_INSTALL=false

VENV_PATH="env"

# Парсинг аргументов командной строки
while getopts "umrd" opt; do
  case $opt in
    u) DO_UPDATE=true ;;
    m) DO_MIGRATE=true ;;
    r) DO_RESTART=true ;;
    d) DO_INSTALL=true ;;
    \?) echo "Использование: $0 [-u] [-m] [-r] [-d]"; exit 1 ;;
  esac
done

# Если ни один флаг не передан — включаем все действия
if [ "$OPTIND" -eq 1 ]; then
  DO_UPDATE=true
  DO_MIGRATE=true
  DO_RESTART=true
  DO_INSTALL=true
fi

# --- Шаг 1: Git update ---
if [ "$DO_UPDATE" = true ]; then
  echo "Проверяю наличие обновлений в репозитории..."

  git fetch origin

  LOCAL=$(git rev-parse HEAD)
  REMOTE=$(git rev-parse origin/main)
  BASE=$(git merge-base HEAD origin/main)

  if [ "$LOCAL" != "$REMOTE" ]; then
    if [ "$LOCAL" = "$BASE" ]; then
      echo "Выполняю git pull..."
      git pull origin main || { echo "Ошибка при выполнении git pull"; exit 1; }
    else
      echo "Локальная и удалённая ветки расходятся. Автоматическое обновление невозможно."
      exit 1
    fi
  else
    echo "Обновлений нет"
  fi
fi

# Активируем виртуальное окружение, если нужны миграции или установка зависимостей
if [ "$DO_MIGRATE" = true ] || [ "$DO_INSTALL" = true ]; then
  if [ ! -d "$VENV_PATH" ]; then
    echo "Виртуальное окружение не найдено в $VENV_PATH"
    exit 1
  fi

  source "$VENV_PATH/bin/activate" || { echo "Не могу активировать виртуальное окружение"; exit 1; }
fi

# --- Шаг 2: Установка зависимостей ---
if [ "$DO_INSTALL" = true ]; then
  echo "Устанавливаю зависимости из requirements.txt..."

  if [ ! -f "requirements.txt" ]; then
    echo "Файл requirements.txt не найден!"
    exit 1
  fi

  pip install -r requirements.txt || { echo "Ошибка при установке зависимостей"; exit 1; }
fi

# --- Шаг 3: Миграции Alembic ---
if [ "$DO_MIGRATE" = true ]; then
  echo "Выполняю миграции Alembic..."

  ALEMBIC_CMD="$VENV_PATH/bin/alembic"
  if [ ! -f "$ALEMBIC_CMD" ]; then
    echo "Alembic не найден в виртуальном окружении. Убедитесь, что он установлен."
    exit 1
  fi

  $ALEMBIC_CMD upgrade head || { echo "Ошибка при выполнении миграций Alembic"; exit 1; }
fi

# --- Шаг 4: Перезапуск сервиса ---
if [ "$DO_RESTART" = true ]; then

  # Получаем путь к директории, где находится скрипт
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  cd "$SCRIPT_DIR" || { echo "Не могу перейти в $SCRIPT_DIR"; exit 1; }

  # Поиск .service файла
  SERVICE_FILE=$(find . -maxdepth 1 -type f -name "*.service" | head -n1)
  if [ -z "$SERVICE_FILE" ]; then
    echo "Файл .service не найден в директории $SCRIPT_DIR"
    exit 1
  fi
  SERVICE_NAME=$(basename "$SERVICE_FILE")
  echo "Найден файл сервиса: $SERVICE_NAME"

  echo "Перезапускаю сервис $SERVICE_NAME..."
  sudo systemctl restart "$SERVICE_NAME" || { echo "Ошибка при перезапуске сервиса"; exit 1; }

  echo "Проверяю статус сервиса..."
  sudo systemctl is-active --quiet "$SERVICE_NAME"
  if [ $? -eq 0 ]; then
    echo "Сервис $SERVICE_NAME успешно перезапущен."
  else
    echo "Сервис $SERVICE_NAME не запущен после перезагрузки!" >&2
    exit 1
  fi
fi

echo "Операции завершены."