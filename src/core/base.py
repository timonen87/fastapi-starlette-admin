from typing import Any

from sqlalchemy.ext.declarative import as_declarative

from .database import SessionLocal, engine


@as_declarative()
class Base:
    id: Any
    __name__: str
