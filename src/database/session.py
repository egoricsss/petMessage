from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session

from src.database import SessionLocal


@contextmanager
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
