import datetime
from pydantic import BaseModel
from tg.states.states import State
from errors.errors import ParamError
from typing import Dict
from utils.utils import *
from utils.booking_status import *

class Params(BaseModel):
    state:State
    slot_id:int|None = None
    booking_id:int|None = None
    date:datetime.date|None = None
    date2:datetime.date|None = None
    time:datetime.time|None = None
    year:int|None = None
    month:int|None = None
    booking_type:str|None = None
    page:int|None = None
    confirm:int|None = None
    data:int|None = None
    kb:int|None = None
    user_id:int|None = None

    def __str__(self):
        return build_callback_data(**self.model_dump(exclude_unset=True))

def convert_data_to_str_args(key, value)->str:
    if key == "time":
        return time_to_str_with_second(value)
    return str(value)

def build_callback_data(**kwargs):
    return "&".join(map(lambda pair: f"{pair[0]}={convert_data_to_str_args(pair[0], pair[1])}", kwargs.items()))

def convert_str_to_value(key, value):
    if value=="None":
        return None
    if key == "state":
        return State(int(value))
    elif key == "date" or key == "date2":
        return conver_str_to_date(value)
    elif key == "time":
        return conver_str_to_time(value)
    elif key == "booking_type":
        return value
    return int(value)

def convert_args_to_params(args:Dict[str,str])->Params:
    data = {}
    for key, value in args.items():
        try:
            data[key] = convert_str_to_value(key, value)
        except Exception as e:
            raise ParamError(key = key, value = value)
    params = Params(**data)
    if not params.page: 
            params.page = 0
    if not params.booking_type:
        params.booking_type = ACTUAL_BOOKING
    return params

def extract_callback_data(data:str)->Params:
    parts = data.split("&")
    args = {}
    for item in parts:
        pair = item.split("=")
        if len(pair)!=2:
            raise ParamError(data=data, part = item)
        args[pair[0]] = pair[1]
    return convert_args_to_params(args)


