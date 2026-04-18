from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import StaticPool

from src.database import get_engine, init_db
from src.database.base import Base
from src.routers import message_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db(database_url="sqlite:///:memory:", echo=True, poolclass=StaticPool)

    from src.database.message import Message

    Base.metadata.create_all(bind=get_engine())

    yield

    Base.metadata.drop_all(bind=get_engine())
    if engine := getattr(init_db, "__globals__", {}).get("engine"):
        engine.dispose()


app = FastAPI(title="Messages CRUD", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_router)

if __name__ == "__main__":
    uvicorn.run("src.__main__:app", reload=True)
