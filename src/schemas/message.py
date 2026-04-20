from pydantic import BaseModel, ConfigDict, Field


class MessageCreateSchema(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)


class MessageUpdateSchema(BaseModel):
    update_id: int | None = Field(default=None, alias="id")
    update_content: str | None = Field(default=None, alias="content")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class MessageSchema(BaseModel):
    id: int
    content: str

    model_config = ConfigDict(from_attributes=True)
