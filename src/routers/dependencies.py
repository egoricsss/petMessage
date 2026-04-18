from fastapi import Depends
from typing import Annotated

from src.database.session import get_session
from sqlalchemy.orm import Session


DbSessionDep = Annotated[Session, Depends(get_session)]
