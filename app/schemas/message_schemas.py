from pydantic import BaseModel, ConfigDict


class MessageSchema(BaseModel):
    id: int
    content: str

    model_config = ConfigDict(from_attributes=True, orm_mode=True)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        for attr in ["id", "content"]:
            if getattr(self, attr) != getattr(self, other):
                return False
        return True

    def to_dict_wo_id(self):
        return self.model_dump(exclude={"id"})


class MessageCreateSchema(BaseModel):
    content: str
