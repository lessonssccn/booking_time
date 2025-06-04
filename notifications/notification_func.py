from dto.models import BookingDTO
from notifications.notification_template import *
from utils.utils import date_to_str, time_to_str
import datetime

def create_user_notification_booking_msg(booking:BookingDTO)->str:
    return USER_BOOKING_NOTIFICATION.format(date = date_to_str(booking.time_slot.date), time = time_to_str(booking.time_slot.time))

def create_admin_notification_booking_msg(booking:BookingDTO)->str:
    return ADMIN_BOOKING_NOTIFICATION.format(date = date_to_str(booking.time_slot.date), 
                                             time = time_to_str(booking.time_slot.time), 
                                             name = booking.user.first_name, 
                                             username = booking.user.username, 
                                             tg_id = booking.user.tg_id)

def prfix_reminder(offset_minutes:int, blob_html=True) -> str:
    prefix = f"Через {offset_minutes} минут"
    if blob_html:
        return f"<b>{prefix}</b>"
    else:
        return prefix