from sqlalchemy import func, or_, and_, select, not_
from dao.booking_dao import BookingDao
from dao.timeslot_dao import TimeslotDao
from database.models import TimeSlot, Booking, User
from dto.models import BookingDTO, UserDTO
from dto.booking_models import NewBooking, UpdateBooking, BookingList
from dto.timeslot_models import UpdateTimeslot
from typing import List
import datetime
from database.base import get_session, get_session_with_commit
from errors.errors import *

class BookingRepository:
    def __init__(self):
        self.booking_dao = BookingDao()
        self.timeslot_dao = TimeslotDao()

    async def add_new_booking(self, timeslot_id, user_id) -> BookingDTO:
        async with get_session_with_commit() as session:
            timeslot = await self.timeslot_dao.find_one_by_id(session, timeslot_id)
            if not timeslot:
                raise BookingError(error_code=ErrorCode.TIMESLOT_NOT_FOUND, timeslot_id = timeslot_id)
            
            new_booking = NewBooking(user_id=user_id, time_slot_id=timeslot_id, date=datetime.datetime.combine(timeslot.date, timeslot.time))
            booking = await self.booking_dao.add(session, new_booking.model_dump())
            if not booking:
                raise BookingError(error_code=ErrorCode.ERROR_CREATE_BOOKING, timeslot_id = timeslot_id, user_id = user_id)

            update_slot = UpdateTimeslot(capacity=timeslot.capacity-1)
            updated_row = await self.timeslot_dao.update(session, TimeSlot.id == timeslot_id, update_slot.model_dump(exclude_unset=True))
            if updated_row!=1:
                raise BookingError(error_code=ErrorCode.ERROR_UPDATE_CAPACITY, timeslot_id = timeslot_id)
            
            return BookingDTO.model_validate(await self.booking_dao.get_one_booking(session, [Booking.id == booking.id]))
                  

    async def get_booking_by_id(self, booking_id:int) -> BookingDTO:
        async with get_session() as session:
            booking = await self.booking_dao.get_one_booking(session, [Booking.id == booking_id])
            if booking:
                return BookingDTO.model_validate(booking)
            raise BookingError(error_code=ErrorCode.BOOKING_NOT_FOUND, booking_id = booking_id)

    async def exsist_booking(self, timeslot_id:int, list_status:List[str]):
        filters = [Booking.time_slot_id == timeslot_id, Booking.status.in_(list_status)]
        async with get_session() as session:
            count = await self.booking_dao.get_count_booking(session, filters)
            return count > 0

    async def exsist_booking_for_user(self, user_id:int, timeslot_id:int, list_status:List[str]):
        filters = [Booking.time_slot_id == timeslot_id, Booking.status.in_(list_status), Booking.user_id == user_id]
        async with get_session() as session:
            count = await self.booking_dao.get_count_booking(session, filters)
            return count > 0

    async def update_staust_booking(self, booking_id:int, new_status:str) -> bool:
        return await self.update_booking(booking_id, UpdateBooking(status=new_status))

    async def update_booking(self, booking_id:int, update_booking:UpdateBooking) -> bool:
        async with get_session_with_commit() as session:
            try:
                count = await self.booking_dao.update(session, Booking.id == booking_id, update_booking.model_dump(exclude_unset=True))
                return count!=0
            except:
                return False

    async def cancel_booking(self, booking_id: int, user_id:int, cancel_status:str)->BookingDTO:
        async with get_session_with_commit() as session:
            filters = [Booking.id == booking_id]
            if user_id!=None:
                filters.append(Booking.user_id == user_id)

            update_date = UpdateBooking(status=cancel_status).model_dump(exclude_unset=True)
            if not await self.booking_dao.update(session, filters, update_date):
                return BookingError(error_code=ErrorCode.ERROR_UPDATE_STATUS_BOOKING, booking_id = booking_id, user_id = user_id)

            booking = await self.booking_dao.get_one_booking(session, filters)

            update_date = UpdateTimeslot(capacity=booking.time_slot.capacity+1).model_dump(exclude_unset=True)
            if not await self.timeslot_dao.update(session, TimeSlot.id == booking.time_slot_id, update_date):
                return BookingError(error_code=ErrorCode.ERROR_UPDATE_STATUS_BOOKING, booking_id = booking_id, user_id = user_id, timeslot_id = booking.time_slot_id)
            return BookingDTO.model_validate(await self.booking_dao.get_one_booking(session, [Booking.id == booking_id]))

    async def get_list_booking_for_user(self, date: datetime.date, user_id:int, list_status:List[str])->List[BookingDTO]:
        async with get_session() as session:
            list_booking = await self.booking_dao.get_list_booking(session, [Booking.date_only == date, Booking.user_id == user_id, Booking.status.in_(list_status)])
            return list(map(lambda booking: BookingDTO.model_validate(booking), list_booking))
        
    async def get_booking(self, booking_id:int, user_id:int) -> BookingDTO:
        async with get_session() as session:
            filters = [Booking.user_id == user_id, Booking.id == booking_id]
            booking = await self.booking_dao.get_one_booking(session, filters)
            if booking:
                return BookingDTO.model_validate(booking)
            raise BookingError(error_code=ErrorCode.BOOKING_NOT_FOUND, booking_id = booking_id, user_id = user_id)

    async def get_list_booking(self, date: datetime.date, list_status:List[str], limit:int|None=None, offset:int|None=None)->BookingList:
        async with get_session() as session:
            filters = [Booking.date_only == date, Booking.status.in_(list_status)]
            list_booking = await self.booking_dao.get_list_booking(session,filters, limit, offset)
            total_count = await self.booking_dao.get_count_booking(session, filters)
            result = BookingList(list_items=list(map(lambda booking: BookingDTO.model_validate(booking), list_booking)), total_count=total_count)
            return result

    async def get_all_booking_by_date_range(self, status:List[str], min_date:datetime.date, max_date:datetime.date, limit:int, offset:int) -> BookingList:
        async with get_session() as session:
            filters = [Booking.status.in_(status), Booking.date_only >=min_date, Booking.date_only<=max_date]
            list_booking = await self.booking_dao.get_list_booking(session,filters, limit, offset)
            total_count = await self.booking_dao.get_count_booking(session, filters)
            result = BookingList(list_items=list(map(lambda booking: BookingDTO.model_validate(booking), list_booking)), total_count=total_count)
            return result
        
    async def get_list_booking_for_user_by_date_range(self, user_id:int, status:List[str], min_date:datetime.date, max_date:datetime.date, limit:int, offset:int)->BookingList:
        async with get_session() as session:
            filters = [Booking.user_id == user_id, Booking.status.in_(status), Booking.date_only>=min_date, Booking.date_only<=max_date]
            list_booking = await self.booking_dao.get_list_booking(session,filters, limit, offset)
            total_count = await self.booking_dao.get_count_booking(session, filters)
            result = BookingList(list_items=list(map(lambda booking: BookingDTO.model_validate(booking), list_booking)), total_count=total_count)
            return result
        
    async def find_reminde_users_with_appointments_in_period_a_but_not_in_b(self, start_a:datetime.date, end_a:datetime.date, status_a:List[str], start_b:datetime.date, end_b:datetime.date, status_b:List[str])->UserDTO:
        """
        Находит пользователей, у которых:
        ✅ есть записи в период A
        ❌ нет записей в период B
        с учетом статусов
        """
        async with get_session() as session:
            # Подзапрос: есть ли у пользователя записи в период B?
            subquery = (
                select(1)
                .select_from(Booking)
                .where(
                    and_(
                        Booking.user_id == User.id,
                        Booking.date_only.between(start_b, end_b),
                        Booking.status.in_(status_b)
                    )
                )
                .exists()
                .correlate(User)
            )
            
            # Основной запрос: выбрать пользователей с записями в период A и без записей в B
            stmt = (
                select(User)
                .distinct()
                .join(Booking)
                .where(and_(Booking.date_only.between(start_a, end_a), Booking.status.in_(status_a), User.remind_inactive==True))
                .where(not_(subquery))
            )
            
            result = await session.execute(stmt)
            users = result.scalars().all()
            return list(map(lambda user: UserDTO.model_validate(user), users))