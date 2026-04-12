from sqlalchemy import select

from ..database.models import Message
from .base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def __init__(self, session):
        super().__init__(session, Message)

    async def get_message_by_content(self, keyword: str) -> list[Message]:
        stmt = select(Message).where(Message.content.ilike(f"%{keyword}%"))
        result = await self.session.scalars(stmt)
        return result.all()
