from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.message import MessageCreateSchema, MessageSchema, MessageUpdateSchema
from .dependencies import DbSessionDep

from sqlalchemy import select
from src.database.message import Message


router = APIRouter()


@router.get("/messages/{message_id}", response_model=MessageSchema)
async def get_message(message_id: int, db_session: DbSessionDep) -> MessageSchema:
    stmt = select(Message).where(Message.id == message_id)
    message = db_session.scalar(stmt)
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="message not found"
        )
    return message


@router.patch("/messages/{message_id}", response_model=MessageSchema)
async def update_message(
    message_id: int, payload: MessageCreateSchema, db_session: DbSessionDep
) -> MessageSchema:
    update_data = payload.model_dump(exclude_unset=True)
    stmt = (
        update(Message)
        .where(Message.id == message_id)
        .values(**update_data)
        .returning(Message)
    )
    updated_message = db_session.scalar(stmt)
    if updated_message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="message not found"
        )
    return updated_message


@router.put("/messages/{message_id}", response_model=MessageSchema)
async def replace_message(
    message_id: int, payload: MessageUpdateSchema, db_session: DbSessionDep
) -> MessageSchema:
    replace_data = payload.model_dump(exclude_unset=True, by_alias=True)
    try:
        stmt = (
            update(Message)
            .where(Message.id == message_id)
            .values(**replace_data)
            .returning(Message)
        )
        replaced_message = db_session.scalar(stmt)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong message index."
        )
    else:
        if replaced_message is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="message not found"
            )
        return replaced_message


@router.delete("/messages/{message_id}", response_model=MessageSchema)
async def delete_message(message_id: int, db_session: DbSessionDep) -> MessageSchema:
    stmt = delete(Message).where(Message.id == message_id).returning(Message)
    deleted_message = db_session.scalar(stmt)
    if deleted_message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="message not found"
        )
    return deleted_message


@router.get("/messages", response_model=list[MessageSchema])
async def get_messages(db_session: DbSessionDep) -> list[MessageSchema]:
    stmt = select(Message)
    messages = db_session.scalars(stmt)
    return messages


@router.post("/messages", response_model=MessageSchema)
async def create_message(
    payload: MessageCreateSchema, db_session: DbSessionDep
) -> MessageSchema:
    create_data = payload.model_dump(exclude_unset=True)
    try:
        stmt = insert(Message).values(**create_data).returning(Message)
        created_message = db_session.scalar(stmt)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong message index."
        )
    else:
        return created_message
