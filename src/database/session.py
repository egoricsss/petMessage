from typing import Generator

from sqlalchemy.orm import Session

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

engine: Engine | None = None
SessionLocal: sessionmaker | None = None


def init_db(database_url: str, **kwargs) -> None:
    global engine, SessionLocal
    engine = create_engine(database_url, **kwargs)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_engine() -> Engine:
    if engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return engine



def get_session() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise RuntimeError("Database is not initialized")

    session: Session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
