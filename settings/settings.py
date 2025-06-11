from pydantic_settings import BaseSettings, SettingsConfigDict
import datetime
from typing import List

class Settings(BaseSettings):
    telegram_bot_token:List[str]
    telegram_channel_id:int
    admin_id:int
    connection_string:str
    url_jobs:str
    bot_locale:str
    add_slot_start_time:datetime.time
    open_windows:int
    day_before:int
    day_after:int
    daily_reminder_time:datetime.time
    day_after_last_active:int
    day_before_future_booking:int
    reminder_minutes_before:List[int]
    notification_create_new_user:bool
    daily_reminder_admin_check_status_booking:bool
    admin_select_other_day_booking_day_before:int

    bot_update_active:bool
    bot_update_command:str
    bot_update_password:str
    bot_update_script:str
    bot_update_log:str
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()