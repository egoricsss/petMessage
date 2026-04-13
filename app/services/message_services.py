from ..database.models import Message
from ..repositories.message import MessageRepository


class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    async def get_all_messages(self) -> list[Message]:
        return await self.repository.get_all()

    async def get_message_or_404(self, message_id: int) -> Message:
        message = await self.repository.get_by_id(message_id)
        if not message:
            from fastapi import HTTPException, status

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
            )
        return message

    async def create_message(self, content: str) -> Message:
        return await self.repository.create(content=content)

    async def create_messages_bulk(self, data: list[dict[str, str]]) -> list[Message]:
        return await self.repository.create_all(data)

    async def delete_all_messages(self) -> bool:
        return await self.repository.delete_all()
