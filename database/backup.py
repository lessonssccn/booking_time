import aiosqlite
import datetime
from settings.settings import settings


def extract_path_from_url(url:str):
    return url.split("///")[-1]

async def live_backup_sqlite(src_db, dst_db):
    try:
        async with aiosqlite.connect(src_db) as src:
            async with aiosqlite.connect(dst_db) as dst:
                await src.backup(dst)
    except Exception as e:
        print(f"back up error = {e}")
        return False
    return True

async def backup_db():
    dst_db = f"backup_db_{datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M%S")}.db"
    await live_backup_sqlite(extract_path_from_url(settings.connection_string), dst_db)
    return dst_db

async def backup_jobs():
    dst_db = f"backup_jobs_{datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M%S")}.db"
    await live_backup_sqlite(extract_path_from_url(settings.url_jobs), dst_db)
    return dst_db