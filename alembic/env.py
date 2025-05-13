from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
# Импортируйте ваши модели SQLAlchemy
from database.models import Base
# Настройка Alembic
config = context.config

# Подключение к базе данных
def get_async_engine():
    url = config.get_main_option("sqlalchemy.url")
    return create_async_engine(url)

# Асинхронная функция для применения миграций
async def run_migrations_online():
    connectable = get_async_engine()

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

# Функция для выполнения миграций
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=Base.metadata)

    with context.begin_transaction():
        context.run_migrations()

# Запуск миграций
if context.is_offline_mode():
    raise Exception("Асинхронные миграции не поддерживаются в offline-режиме.")
else:
    import asyncio
    asyncio.run(run_migrations_online())