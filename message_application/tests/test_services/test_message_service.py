import pytest
from message_application.app.database.models import Message
from contextlib import nullcontext as does_not_raise
from fastapi import HTTPException


class TestBaseFunction:
    async def test_get_all_messages(self, message_service):
        result = await message_service.get_all_messages()

        assert isinstance(result, list)
        assert all(isinstance(message, Message) for message in result)

    @pytest.mark.parametrize(
        "id, context", [(5, pytest.raises(HTTPException)), (1, does_not_raise())]
    )
    async def test_get_message_or_404(self, message_service, id, context):
        with context:
            result = await message_service.get_message_or_404(message_id=id)
            assert isinstance(result, Message)
            assert result.id == id

    @pytest.mark.parametrize("content", ("pipipupa", "pipiipppipipp", "papapappapapap"))
    async def test_create_message(self, message_service, content):
        result = await message_service.create_message(content=content)
        assert isinstance(result, Message)
        assert result.content == content

    async def test_delete_all_messages(self, message_service):
        result = await message_service.delete_all_messages()

        assert result == True
        