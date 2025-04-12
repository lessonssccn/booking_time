from enum import Enum

class State(Enum):
    IGNORE = 0

    USER_SHOW_LIST_MY_BOOKING = 1
    USER_SHOW_CALENDAR = 2
    USER_SHOW_TIMESLOTS = 3
    USER_BOOKING = 4
    USER_CANCEL_SELECTED_SLOT = 5
    USER_CANCEL_BOOKING = 6
    USER_CANCEL_BOOKING_CONFIRM = 7
    USER_CANCEL_BOOKING_BACK = 8
    USER_SHOW_CONFIRM_BOOKING = 9
    USER_SHOW_CONFIRM_UNBOOKING = 10
    USER_UNBOOKING = 11
    USER_BOOKING_DETAILS = 12


    ADMIN_ADD_TIMESLOT_SELECT_DATE = -1
    ADMIN_ADD_TIMESLOT_SELECT_TIME = -2
    ADMIN_ADD_TIMESLOT_CONFIRM = -3
    ADMIN_ADD_TIMESLOT_CANCEL = -4

    ADMIN_REMOVE_TIMESLOT_SELECT_DATE = -5
    ADMIN_REMOVE_TIMESLOT_SELECT_SLOT = -6
    ADMIN_REMOVE_TIMESLOT_CONFIRM_MSG = -7
    ADMIN_REMOVE_TIMESLOT_CONFIRM = -8
    ADMIN_REMOVE_TIMESLOT_CANCEL = -9

    ADMIN_LOCK_TIMESLOT_SELECT_DATE = -10
    ADMIN_LOCK_TIMESLOT_SELECT_SLOT = -11
    ADMIN_LOCK_TIMESLOT = -12

    ADMIN_HIDE_TIMESLOT_SELECT_DATE = -13
    ADMIN_HIDE_TIMESLOT_SELECT_SLOT = -14
    ADMIN_HIDE_TIMESLOT = -15

    ADMIN_LOCK_DAY_SELECT_DATE = -16
    ADMIN_LOCK_DAY = -17 

    ADMIN_UNBOOKING_DAY_SELECT_DATE = -18
    ADMIN_UNBOOKING_DAY_CONFIRM = -19
    ADMIN_UNBOOKING_DAY_CANCEL = -20

    ADMIN_CONFIRM_BOOKING = -21
    ADMIN_REJECT_BOOKING = -22
    ADMIN_CANCEL_BOOKING = -23

    ADMIN_MOVE_BOOKING = -24

    ADMIN_UNBOOKING_DAY = -25

    ADMIN_CUR_DAY_BOOKING = -26
    ADMIN_ALL_LIST_BOOKING = -27
    
    ADMIN_BOOKING_DETAILS = -28
    ADMIN_MAIN_MENU = -29

    ADMIN_UNBOOKING_DAY_SHOW_CONFIRM_MSG = -30

    ADMIN_NEXT_DAY_BOOKING = -31

    def is_admin_state(self)->bool:
        return self.value<0

    def __str__(self):
        return str(self.value)
    
    def __int__(self):
        return self.value
    
    def __eq__(self, value):
        return self.value == value
    
    def __hash__(self):
        return super().__hash__()