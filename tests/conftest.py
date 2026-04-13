import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import insert

from app.database.utils import Base
from app.database.models import Message
from app.repositories.message import MessageRepository
from app.services.message_services import MessageService

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


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


@pytest.fixture(scope="function", autouse=True)
async def seeded_messages(db_session):
    data = [
        {"content": "first message in FastAPI"},
        {"content": "second message"},
        {"content": "third message in FastAPI"},
    ]
    await db_session.execute(insert(Message).values(data))
    yield data
