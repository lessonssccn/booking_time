import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.utils import *
class TimeKeyboard:
    def __init__(self, date:datetime.date, time:datetime.time, default_pefix:str, confirm_prefix:str, cancel_pefix:str , delta_mm:int=15, disable_prefix:str="0"):
        self.date = date
        self.time = time
        self.default_pefix = default_pefix
        self.confirm_prefix = confirm_prefix
        self.cancel_pefix = cancel_pefix
        self.disable_prefix = disable_prefix
        self.delta_mm = delta_mm

    def _get_callback(self, time:datetime.time)->str:
        return f"state={self.default_pefix}&date={self.date}&time={time}"

    def _get_callback_up_hh(self, step):
        return self._get_callback(datetime.time((self.time.hour+step)%24, self.time.minute))

    def _get_callback_down_hh(self, step):
        return self._get_callback(datetime.time(self.time.hour-step if self.time.hour!=0 else 23, self.time.minute))

    def _get_callback_up_mm(self, step):
        return self._get_callback(datetime.time(self.time.hour, (self.time.minute + step)%60))
    
    def _get_callback_down_mm(self, step):
        return self._get_callback(datetime.time(self.time.hour, (self.time.minute - step) if (self.time.minute -step) >=0 else 60 - step))
    
    def _get_callback_confirm(self):
        return f"state={self.confirm_prefix}&date={self.date}&time={time_to_str_with_second(self.time)}"

    def _get_callback_cancel(self):
        return f"state={self.cancel_pefix}&date={self.date}&time={time_to_str_with_second(self.time)}"

    def _create_btn_next_hh(self):
        return InlineKeyboardButton("⬆️", callback_data=self._get_callback_up_hh(1))

    def _create_btn_prev_hh(self):
        return InlineKeyboardButton("⬇️", callback_data=self._get_callback_down_hh(1))

    def _create_btn_next_mm(self):
        return InlineKeyboardButton("⬆️", callback_data=self._get_callback_up_mm(self.delta_mm))

    def _create_btn_prev_mm(self):
        return InlineKeyboardButton("⬇️", callback_data=self._get_callback_down_mm(self.delta_mm))
    
    def _create_btn_up_2_hh(self):
        return InlineKeyboardButton("⏫", callback_data=self._get_callback_up_hh(2))

    def _create_btn_down_2_hh(self):
        return InlineKeyboardButton("⏬", callback_data=self._get_callback_down_hh(2))

    def _create_btn_up_2_mm(self):
        return InlineKeyboardButton("⏫", callback_data=self._get_callback_up_mm(self.delta_mm*2))

    def _create_btn_down_2_mm(self):
        return InlineKeyboardButton("⏬", callback_data=self._get_callback_down_mm(self.delta_mm*2))
    
    def _create_btn_confirm(self):
        return InlineKeyboardButton("ОК", callback_data=self._get_callback_confirm())

    def _create_btn_cancel(self):
        return InlineKeyboardButton("Отмена", callback_data=self._get_callback_cancel())

    def _create_btn_hh(self):
        return InlineKeyboardButton(f"{self.time.hour:02}", callback_data=self.disable_prefix)

    def _create_btn_mm(self):
        return InlineKeyboardButton(f"{self.time.minute:02}", callback_data=self.disable_prefix)

    def create_time_buttons(self):
        buttons = [
            [self._create_btn_up_2_hh(), self._create_btn_up_2_mm()],
            [self._create_btn_next_hh(), self._create_btn_next_mm()],
            [self._create_btn_hh(), self._create_btn_mm()],
            [self._create_btn_prev_hh(), self._create_btn_prev_mm()],
            [self._create_btn_down_2_hh(), self._create_btn_down_2_mm()],
            [self._create_btn_confirm()],
            [self._create_btn_cancel()]
        ]
        return InlineKeyboardMarkup(buttons)
        


