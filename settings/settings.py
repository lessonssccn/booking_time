from pydantic_settings import BaseSettings, SettingsConfigDict
import datetime
from typing import List

class Settings(BaseSettings):
    telegram_bot_token:List[str]
    connection_string:str
    url_jobs:str
    bot_locale:str
    add_slot_start_time:datetime.time
    open_windows:int
    copy_frame_day_before:int
    copy_frame_day_after:int
    daily_reminder_time:datetime.time
    day_after_last_active:int
    day_before_future_booking:int
    reminder_minutes_before:List[int]
    notification_create_new_user:bool
    daily_reminder_admin_check_status_booking:bool
    admin_select_other_day_booking_day_before:int

    bot_update_active:bool
    bot_update_command:str
    bot_update_script:str
    bot_update_log:str

    history_frame_size_before:int
    history_frame_size_after:int

    page_size:int

    actual_booking_frame_size_after:int

    backup_command_active:bool
    backup_command:str

    backup_cron_active:bool
    backup_cron_time:datetime.time

    admin_password:str
    limit_incorrect_password:int
    
    add_admin_command:str
    rm_admin_command:str
    
    add_channel_text:str
    rm_channel_text:str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()