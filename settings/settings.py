from pydantic_settings import BaseSettings, SettingsConfigDict
import datetime

class Settings(BaseSettings):
    telegram_bot_token:str
    telegram_channel_id:int
    admin_id:int
    connection_string:str
    bot_locale:str
    add_slot_start_time:datetime.time
    open_windows:int
    day_before:int
    day_after:int
    daily_reminder_time:datetime.time
    day_after_last_active:int
    day_before_future_booking:int
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()