from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import asyncio

class SchedulerHolder:
    _scheduler_instance: AsyncIOScheduler | None = None
    _ref_count = 0
    _lock = asyncio.Lock()

    @classmethod
    def get_scheduler(cls) -> AsyncIOScheduler:
        if cls._scheduler_instance is None:
                raise RuntimeError("Scheduler not initialized! Call SchedulerHolder.init_scheduler() first.")
        return cls._scheduler_instance
    
    @classmethod
    async def get_scheduler_async(cls) -> AsyncIOScheduler:
        async with cls._lock:
            if cls._scheduler_instance is None:
                raise RuntimeError("Scheduler not initialized! Call SchedulerHolder.init_scheduler() first.")
            return cls._scheduler_instance
    
    @classmethod
    async def init_scheduler(cls, url:str = "sqlite:///jobs.sqlite"):
        async with cls._lock:
            if cls._ref_count==0:
                cls._scheduler_instance = AsyncIOScheduler(
                    jobstores={"default": SQLAlchemyJobStore(url)}
                )
                cls._scheduler_instance.start()
                print("🟢 планировщик запущен")
            cls._ref_count += 1

    @classmethod
    async def stop_scheduler(cls):
        async with cls._lock:
            if cls._scheduler_instance:
                cls._ref_count -= 1
                if cls._ref_count<=0:
                    cls._scheduler_instance.shutdown()
                    print("🔴 Планировщик задач остановлен")

