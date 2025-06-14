from apscheduler.schedulers.asyncio import AsyncIOScheduler
from settings.settings import settings
from tg.bot_holder import BotAppHolder
from apscheduler.triggers.cron import CronTrigger
from tg.tg_func_service import backup_and_send

shared_backup_job_id = "bakup_job"


async def backup()->None:
    list_app = await BotAppHolder.get_list_app()
    if len(list_app)>0:
        app = list_app[0]
        await backup_and_send(app.bot)
        
async def restart_backup_job(scheduler:AsyncIOScheduler)->None:
    job = scheduler.get_job(shared_backup_job_id)
    print(job)
    if job:
        scheduler.remove_job(shared_backup_job_id)
        print("remove old sharedbackup")

    if settings.backup_cron_active:
        time = settings.backup_cron_time
        trigger = CronTrigger(hour=time.hour, minute=time.minute)
        job = scheduler.add_job(backup, trigger=trigger, id=shared_backup_job_id)
        print(job)


async def restart_shared_jobs(scheduler:AsyncIOScheduler)->None:
    await restart_backup_job(scheduler)
