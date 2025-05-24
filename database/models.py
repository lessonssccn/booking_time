from database.base import Base
import datetime
from sqlalchemy import BigInteger, String, DECIMAL, Integer, Date, ForeignKey, Computed
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class User(Base):
    __tablename__ = "users"

    tg_id:Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    lock_at:Mapped[datetime.datetime | None]
    reserve:Mapped[float] = mapped_column(DECIMAL(10,1), default=0)
    remind_inactive:Mapped[bool] = mapped_column(default=True, server_default="1")
    reminder_minutes_before:Mapped[str] = mapped_column(default="[60,15,5]", server_default="[60,15,5]")

    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user")

class Day(Base):
    __tablename__ = "days"

    date:Mapped[datetime.date]
    lock:Mapped[bool] = mapped_column(default=False)

class TimeSlot(Base):
    __tablename__ = "time_slots"

    time:Mapped[datetime.time]
    date:Mapped[datetime.date | None]
    dayweek:Mapped[int | None]
    max_capacity:Mapped[int] = mapped_column(default=1)
    capacity:Mapped[int] = mapped_column(default=1)
    duration:Mapped[int] = mapped_column(default=60)
    hide:Mapped[bool] = mapped_column(default=False)
    lock:Mapped[bool] = mapped_column(default=False, server_default="0")

    bookings: Mapped[list["Booking"]] = relationship(
        "Booking",
        back_populates="time_slot",
        cascade="all, delete-orphan"
    )

class Booking(Base):
    __tablename__ = "bookings"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    time_slot_id: Mapped[int] = mapped_column(Integer, ForeignKey("time_slots.id"))
    date: Mapped[datetime.datetime]
    status: Mapped[str]
    date_only:Mapped[datetime.date] = mapped_column(server_default=Computed("DATE(date)"))
    
    user: Mapped["User"] = relationship("User", back_populates="bookings")
    time_slot: Mapped["TimeSlot"] = relationship("TimeSlot", back_populates="bookings")




