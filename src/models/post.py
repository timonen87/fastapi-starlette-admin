import enum
from datetime import datetime, date
from typing import Optional, Union, List
from sqlalchemy_file import ImageField, File
from sqlalchemy_file.validators import SizeValidator

from jinja2 import Template
from sqlalchemy import Column, String, Integer, Enum, JSON, DateTime, ForeignKey, func, Text, sql, TEXT, Boolean
from sqlalchemy.orm import relationship
from pydantic import EmailStr
from starlette.requests import Request

from core.base import Base
from . import user
from . import comment


class Post(Base):
    __tablename__ = 'post'

    id: Optional[int] = Column(Integer, primary_key=True)
    title: str = Column(String(100))
    content = Column(TEXT)
    tags: List[str] = Column(JSON)
    published_at: Optional[datetime] = Column(DateTime(timezone=True), server_default=sql.func.now())
    # published_at: Optional[datetime] = Field(
    #     sa_column=Column(DateTime(timezone=True), default=datetime.utcnow)
    # )
    # published_at: Optional[datetime] = Column( default=datetime.utcnow)
    publisher_id = Column(Integer, ForeignKey("user.id"))
    publisher = relationship('User', back_populates='posts')

    comments = relationship('Comment', back_populates='post')

    async def __admin_reper__(self, request: Request):
        return self.title

    async def __admin_select2_repr__(self, request: Request) -> str:
        template_str = (
            "<span><strong>Title: </strong>{{obj.title}}, <strong>Publish by:"
            " </strong>{{obj.publisher.full_name}}</span>"
        )
        return Template(template_str, autoescape=True).render(obj=self)