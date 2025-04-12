from typing import List, TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from database.base import Base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete, func, and_, or_
from collections.abc import Iterable

T = TypeVar("T", bound=Base)

class BaseDAO(Generic[T]):
    model: Type[T] = None

    def __init__(self):
        if self.model is None:
            raise ValueError("Error DAO model unset")
        
    def build_query(self, filters=None, order=None, operation=select, query=None):
        if operation:
            query = operation(self.model)
        
        # 1. Фильтры (обязательно в списке, даже если одно условие)
        if filters is not None:
            if not isinstance(filters, (list, tuple)):
                filters = [filters]  # Превращаем одиночное условие в список
            query = query.where(and_(*filters))
        
        # 2. Сортировка (обязательно в списке)
        if order is not None:
            if not isinstance(order, (list, tuple)):
                order = [order]  # Превращаем одиночное условие в список
            query = query.order_by(*order)
        
        return query
        
        
        
    async def find_one_by_id(self, session: AsyncSession, id: int)->T:
        query = self.build_query(self.model.id==id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    async def find_one(self, session: AsyncSession, filters)->T:
        query = self.build_query(filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()
        
    async def find_all(self, session: AsyncSession, filters=None, limit:int|None=None, offset:int|None = None, order=None)->List[T]:
        query = self.build_query(filters, order)
        if limit!=None:
            query = query.limit(limit)
        if offset!=None:
            query = query.offset(offset)

        result = await session.execute(query)
        records = result.scalars().all()
        return records
    
    async def add(self, session: AsyncSession, values: dict) -> T:
        new_instance = self.model(**values)
        session.add(new_instance)
        await session.flush()
        return new_instance
        
    async def update(self, session: AsyncSession, filters, values)->int:
        query = (
            self.build_query(filters, operation = update)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)
        await session.flush()
        return result.rowcount

    async def delete(self, session: AsyncSession, filters)->int:
        if not filters:
            return 0
    
        query = self.build_query(filters, operation = delete)
        result = await session.execute(query)
        await session.flush()
        return result.rowcount

    async def count(self, session: AsyncSession, filters = None)->int:
        query = self.build_query(filters, query=select(func.count(self.model.id)), operation=None)
        result = await session.execute(query)
        count = result.scalar()
        return count