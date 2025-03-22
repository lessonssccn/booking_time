NEW = "new"
CONFIRMED = "confirmed"
REJECTED = "rejected"
CANCELED_USER = "canceled-user"
CANCELED_ADMIN = "canceled-admin"

STATUC_ICONS = {NEW:"🟡", CONFIRMED:"🟢", REJECTED:"🔴", CANCELED_USER:"⚪", CANCELED_ADMIN:"⚫"}

ACTUAL_BOOKING = "actual"
ALL_BOOKING = "all"

STATUS_BOOKING_TYPE = {ACTUAL_BOOKING:(NEW, CONFIRMED), ALL_BOOKING:(NEW, CONFIRMED, REJECTED, CANCELED_USER, CANCELED_ADMIN)}


def get_status_booking_icon(status:str):
    icon = STATUC_ICONS.get(status, "⚫")
    return icon

def get_canceled_status(is_admin:bool):
    return CANCELED_ADMIN if is_admin else CANCELED_USER

def get_disable_status():
    return (CANCELED_USER, CANCELED_ADMIN, REJECTED)

def get_locked_status():
    return (CONFIRMED, )

def get_actual_status():
    return (NEW, CONFIRMED,)

def get_list_status_by_type(type_booking:str):
    return STATUS_BOOKING_TYPE.get(type_booking, (CONFIRMED, ))

def get_admin_confirm_status():
    return CONFIRMED

def get_admin_reject_status():
    return REJECTED

def can_update_status(status:str):
    return status != CANCELED_USER
