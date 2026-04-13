from sqlalchemy import Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)

    def __repr__(self):
        return f"Message(id={self.id!r}, content={self.content!r})"

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return self.id == other.id and self.content == self.content
