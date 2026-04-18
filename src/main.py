from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from contextlib import asynccontextmanager

from sqlalchemy import create_engine, StaticPool, Engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column
from typing import Generator


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Message(Base):
    content: Mapped[str] = mapped_column(nullable=False)


engine = create_engine("sqlite:///:memory:", echo=True, pool_class=StaticPool)

session_maker = sessionmaker(engine, expire_on_commit=False)


def init_db(engine: Engine) -> Generator[None, None]:
    with engine.begin() as conn:
        Base.metadata.create_all(conn)


def get_db() -> Generator[Session, None]:
    with session_maker() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Messages CRUD", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageCreate(BaseModel):
    content: str


class MessageUpdate(BaseModel):
    content: str | None = None


class Message(BaseModel):
    id: int
    content: str
