from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get_all(self) -> list[T]:
        result = await self.session.scalars(select(self.model))
        return result.all()

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        return await self.session.scalar(
            select(self.model).where(self.model.id == obj_id)
        )

    async def create(self, **kwargs) -> T:
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        return await self.session.scalar(stmt)

    async def create_all(self, data: list[dict[str, Any]]) -> list[T]:
        stmt = insert(self.model).values(data).returning(self.model)
        return await self.session.scalars(stmt)

    async def update(self, obj_id: int, **kwargs) -> T:
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**kwargs)
            .returning(self.model)
        )
        return await self.session.scalar(stmt)

    async def delete(self, obj_id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def delete_all(self) -> bool:
        stmt = delete(self.model)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
