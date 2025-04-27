from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

class SchedulerHolder:
    _scheduler_instance: AsyncIOScheduler | None = None

    @classmethod
    def get_scheduler(cls) -> AsyncIOScheduler:
        if cls._scheduler_instance is None:
            raise RuntimeError("Scheduler not initialized! Call SchedulerHolder.init_scheduler() first.")
        return cls._scheduler_instance
    
    @classmethod
    def init_scheduler(cls, url:str = "sqlite:///jobs.sqlite"):
        cls._scheduler_instance = AsyncIOScheduler(
            jobstores={"default": SQLAlchemyJobStore(url)}
        )
        cls._scheduler_instance.start()
        print("init init_scheduler")
        
    @classmethod
    def stop_scheduler(cls):
        if cls._scheduler_instance:
            cls._scheduler_instance.shutdown()

