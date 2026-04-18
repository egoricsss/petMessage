from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Message(Base):
    __tablename__ = "messages"

    content: Mapped[str] = mapped_column(nullable=False)
