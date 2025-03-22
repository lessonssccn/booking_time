from database.base import Base
from datetime import datetime, time, date
from sqlalchemy import BigInteger, String, DECIMAL
from sqlalchemy import Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class User(Base):
    __tablename__ = "users"

    tg_id:Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    lock_at:Mapped[datetime | None]
    reserve:Mapped[float] = mapped_column(DECIMAL(10,1), default=0)

    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user")

class Day(Base):
    __tablename__ = "days"

    date:Mapped[date]
    lock:Mapped[bool] = mapped_column(default=False)

class TimeSlot(Base):
    __tablename__ = "time_slots"

    time:Mapped[time]
    date:Mapped[date | None]
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
    date: Mapped[datetime]
    status: Mapped[str]
    
    user: Mapped["User"] = relationship("User", back_populates="bookings")
    time_slot: Mapped["TimeSlot"] = relationship("TimeSlot", back_populates="bookings")




