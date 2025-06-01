NEW = "new"
CONFIRMED = "confirmed"
REJECTED = "rejected"
CANCELED_USER = "canceled-user"
CANCELED_ADMIN = "canceled-admin"
NOSHOW_USER = "noshow-user"
NOSHOW_PROVIDER = "noshow-provider"
COMPLETED = "completed"
COMPLETED_UNPAID = "completed-unpaid"
SYS_ERROR = "sys-error"

STATUC_ICONS = {
    NEW:"🟡", 
    CONFIRMED:"🟢", 
    REJECTED:"🔴", 
    CANCELED_USER:"⚪", 
    CANCELED_ADMIN:"⚫", 
    NOSHOW_USER:"🚫",
    NOSHOW_PROVIDER:"✖️",
    COMPLETED:"✅",
    COMPLETED_UNPAID:"💳",
    SYS_ERROR:"⚠️",
}

ACTUAL_BOOKING = "actual"
ALL_BOOKING = "all"

STATUS_BOOKING_TYPE = {
    ACTUAL_BOOKING:(NEW, CONFIRMED, NOSHOW_USER, NOSHOW_PROVIDER, COMPLETED, COMPLETED_UNPAID), 
    ALL_BOOKING:(NEW, CONFIRMED, REJECTED, CANCELED_USER, CANCELED_ADMIN, SYS_ERROR)
}

def is_new_booking(status:str):
    return status == NEW

def get_status_booking_icon(status:str):
    icon = STATUC_ICONS.get(status, "❓")
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
