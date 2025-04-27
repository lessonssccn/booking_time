from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from typing import Optional, Callable, Union
from apscheduler.triggers.interval import IntervalTrigger

class SchedulerService:
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    async def add_job(
        self,
        func: Callable,
        *,
        job_id: str,
        when: Union[int, datetime, timedelta],
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
        interval: Optional[int] = None,
    ) -> str:
        """
        Добавляет задачу.
        
        :param func: Функция для выполнения.
        :param job_id: Уникальный идентификатор задачи.
        :param when: 
            - Если `int`: задержка в секундах.
            - Если `datetime`: точное время запуска.
            - Если `timedelta`: относительное время.
        :param interval: Если указан, задача будет повторяться (в секундах).
        :param args: Аргументы для функции.
        :param kwargs: Ключевые аргументы для функции.
        :return: ID задачи.
        """
        if isinstance(when, int):
            trigger = DateTrigger(run_date=datetime.now() + timedelta(seconds=when))
        elif isinstance(when, (datetime, timedelta)):
            trigger = DateTrigger(run_date=when)
        else:
            raise ValueError("Неподдерживаемый тип для `when`")

        if interval:
            trigger = IntervalTrigger(seconds=interval)

        job = self.scheduler.add_job(
            func,
            trigger=trigger,
            id=job_id,
            args=args,
            kwargs=kwargs,
            replace_existing=True,
        )
        return job.id

    async def remove_job(self, job_id: str) -> bool:
        """Удаляет задачу по ID."""
        try:
            self.scheduler.remove_job(job_id)
            return True
        except Exception:
            return False
