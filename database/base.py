from datetime import datetime
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from errors.errors import *
from contextlib import asynccontextmanager
from settings.settings import settings

engine = create_async_engine(url=settings.connection_string)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

@asynccontextmanager
async def get_session():
    session = async_session_maker()
    try:
        yield session
    except BaseError as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise DAOError(error = str(e))
    finally:
        await session.close()

@asynccontextmanager
async def get_session_with_commit():
    session = async_session_maker()
    try:
        yield session
        await session.commit()
    except BaseError as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise DAOError(error = str(e))
    finally:
        await session.close()

class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True) 

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now()
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )