from fastapi import APIRouter, HTTPException, status

from src.schemas.message import MessageCreateSchema, MessageSchema, MessageUpdateSchema
from .dependencies import DbSessionDep

from sqlalchemy import select
from src.database.message import Message


router = APIRouter()


@router.get("/messages/{message_id}", response_class=MessageSchema)
async def get_message(message_id: int, db_session: DbSessionDep) -> MessageSchema:
    stmt = select(MessageSchema).where(MessageSchema.id == message_id)
    message = db_session.scalar(stmt)
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="message not found"
        )
    return message
