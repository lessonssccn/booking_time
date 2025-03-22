from typing import List, TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from database.base import Base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete, func
from collections.abc import Iterable

T = TypeVar("T", bound=Base)

class BaseDAO(Generic[T]):
    model: Type[T] = None

    def __init__(self):
        if self.model is None:
            raise ValueError("Error DAO model unset")
        
    def build_query_filter(self, filters, operation=select):
        query = operation(self.model)
        return self.add_filter(query, filters)
    
    def add_filter(self, query, filters):
        if isinstance(filters, Iterable):
            return query.where(*filters)
        else:
            return query.where(filters)
        # if filters:
        #     if isinstance(filters, Iterable):
        #         for filter in filters:
        #             query = query.filter(filter)
        #     else:
        #         query = query.filter(filters)
        # return query
        
        
    async def find_one_by_id(self, session: AsyncSession, id: int)->T:
        query = self.build_query_filter(self.model.id==id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    async def find_one(self, session: AsyncSession, filters)->T:
        query = self.build_query_filter(filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()
        
    async def find_all(self, session: AsyncSession, filters=None, limit:int|None=None, offset:int|None = None)->List[T]:
        query = self.build_query_filter(filters)
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
            self.build_query_filter(filters, operation = update)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)
        await session.flush()
        return result.rowcount

    async def delete(self, session: AsyncSession, filters)->int:
        if not filters:
            return 0
    
        query = self.build_query_filter(filters, delete)
        result = await session.execute(query)
        await session.flush()
        return result.rowcount

    async def count(self, session: AsyncSession, filters = None)->int:
        query =  self.add_filter(select(func.count(self.model.id)), filters)
        result = await session.execute(query)
        count = result.scalar()
        return count