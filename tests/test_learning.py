import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def message_data():
    return [{"content": fake.sentence()} for _ in range(5)]


class TestMessageRepositiry:
    async def test_create_message(self, message_service, message_data):
        await message_service.create_messages_bulk(message_data)
        messages = await message_service.get_all_messages()
        print(messages)
        assert len(messages) == 5
