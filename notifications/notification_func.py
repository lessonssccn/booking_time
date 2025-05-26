from dto.models import BookingDTO
from notifications.notification_template import *
from utils.utils import date_to_str, time_to_str

def create_user_notification_booking_msg(booking:BookingDTO)->str:
    return USER_BOOKING_NOTIFICATION.format(date = date_to_str(booking.time_slot.date), time = time_to_str(booking.time_slot.time))

def create_admin_notification_booking_msg(booking:BookingDTO)->str:
    return ADMIN_BOOKING_NOTIFICATION.format(date = date_to_str(booking.time_slot.date), 
                                             time = time_to_str(booking.time_slot.time), 
                                             name = booking.user.first_name, 
                                             username = booking.user.username, 
                                             tg_id = booking.user.tg_id)

