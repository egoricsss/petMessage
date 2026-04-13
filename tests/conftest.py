import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.database.utils import Base
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
