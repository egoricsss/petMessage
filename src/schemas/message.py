from pydantic import BaseModel, ConfigDict


class MessageCreateSchema(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)


class MessageUpdateSchema(BaseModel):
    content: str | None = None

    model_config = ConfigDict(from_attributes=True)


class MessageSchema(BaseModel):
    id: int
    content: str

    model_config = ConfigDict(from_attributes=True)
