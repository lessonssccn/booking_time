# Makefile для работы с Alembic миграциями

# Создает новую миграцию
migrate:
ifndef NAME
	$(error NAME не задано! Используйте: make migrate NAME="revision_name")
endif
	alembic revision --autogenerate -m "$(NAME)"

# Применяет все миграции (upgrade до последней версии)
up:
	alembic upgrade head

# Откатывает все миграции (downgrade до базовой версии)
base:
	alembic downgrade base

# Показывает текущую версию БД
cur:
	alembic current

# Откатывает одну миграцию
down:
	alembic downgrade -1

# Выводит справку
help:
	@echo "Доступные команды:"
	@echo "  make migrate              - Создать новую миграцию"
	@echo "  make up                   - Применить миграции"
	@echo "  make base                 - Откатить все миграции"
	@echo "  make down                 - Откатить одну миграцию"
	@echo "  make cur                  - Показать текущую версию БД"
	@echo "  make clean-migrations     - Удалить все файлы миграций"
	@echo "  make help                 - Эта справка"