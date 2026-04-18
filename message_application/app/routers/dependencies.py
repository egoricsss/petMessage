from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.utils import get_db
from ..repositories.message import MessageRepository
from ..services.message_services import MessageService

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_message_repository(session: SessionDep) -> MessageRepository:
    return MessageRepository(session)


def get_message_service(
    repository: Annotated[MessageRepository, Depends(get_message_repository)],
) -> MessageService:
    return MessageService(repository)


MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]
