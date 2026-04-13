from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.database.models import Message
from app.database.utils import Base
from app.repositories.message import MessageRepository
from app.services.message_services import MessageService

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


# Изоляция - Mock`ирование`
@pytest.fixture
def mock_message_repo():
    repo = AsyncMock(spec=MessageRepository)

    repo.get_id = {AsyncMock(return_value={"id": 1, "content": "first message"})}

    return repo


@pytest.fixture
def service(mock_message_repo):
    return MessageService(mock_message_repo)


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(test_engine):
    connection = await test_engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(bind=connection, expire_on_commit=False)

    yield session

    await transaction.rollback()
    await connection.close()
    await session.close()


@pytest.fixture(scope="function")
def message_service(db_session) -> MessageService:
    repo = MessageRepository(session=db_session)
    return MessageService(repository=repo)
