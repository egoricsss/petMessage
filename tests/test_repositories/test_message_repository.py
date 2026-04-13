import pytest
from sqlalchemy import select

from app.repositories.message import MessageRepository
from app.database.models import Message


@pytest.fixture
def message_repository(db_session):
    return MessageRepository(session=db_session)


class TestCRUDOperations:
    @pytest.mark.parametrize(
        "index, expected_id, expected_content",
        [
            (0, 1, "first message in FastAPI"),
            (1, 2, "second message"),
            (2, 3, "third message in FastAPI"),
        ],
    )
    async def test_select(
        self, message_repository, index, expected_id, expected_content
    ):
        result = await message_repository.get_all()
        assert isinstance(result, list)
        assert all(isinstance(message, Message) for message in result)
        assert result[index].id == expected_id
        assert result[index].content == expected_content

    async def test_delete_all(self, message_repository, db_session):
        result = await message_repository.delete_all()

        messages = await db_session.scalars(select(Message))

        assert result == True
        assert messages.all() == []

    async def test_insert(self, message_repository, db_session):
        await message_repository.create(content="inserted message")
        stmt = select(Message).where(Message.content == "inserted message")
        result = await db_session.scalar(stmt)

        assert result.id == 4
        assert result.content == "inserted message"

    @pytest.mark.parametrize("expected_id", {1, 2, 3})
    async def test_get_by_id(self, message_repository, expected_id):
        result = await message_repository.get_by_id(obj_id=expected_id)
        assert result.id == expected_id

    @pytest.mark.parametrize(
        "updated_id, updated_content",
        [(1, "first update"), (2, "second update"), (3, "third update")],
    )
    async def test_update(
        self, message_repository, db_session, updated_id, updated_content
    ):
        result = await message_repository.update(
            obj_id=updated_id, content=updated_content
        )

        stmt = select(Message).where(Message.id == updated_id)
        updated_result = await db_session.scalar(stmt)

        assert result.id == updated_id
        assert result.content == updated_content
        assert result == updated_result

    @pytest.mark.parametrize("obj_id", {1, 2, 3})
    async def test_delete(self, message_repository, db_session, obj_id):
        result = await message_repository.delete(obj_id=obj_id)

        stmt = select(Message).where(Message.id == obj_id)
        checked_result = await db_session.scalar(stmt)

        assert result == True
        assert checked_result is None

    async def test_get_by_content(self, message_repository):
        result = await message_repository.get_messages_by_content(keyword="API")

        assert result[0].id == 1
        assert result[1].id == 3
