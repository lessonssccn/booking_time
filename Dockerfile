# Используем базовый образ с Python
FROM python:3.12-slim

# Установка локалей
RUN apt-get update && \
    apt-get install -y locales && \
    localedef -i ru_RU -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Команда запуска
# CMD ["python", "main.py"]
RUN chmod +x ./run.sh
CMD ["./run.sh"]