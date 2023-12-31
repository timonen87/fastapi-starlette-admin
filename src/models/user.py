import enum
from datetime import datetime, date
from typing import Optional, Union, List
from sqlalchemy_file import ImageField, File
from sqlalchemy_file.validators import SizeValidator

from jinja2 import Template
from sqlalchemy import (
    Column,
    String,
    Integer,
    Enum,
    JSON,
    DateTime,
    ForeignKey,
    func,
    Text,
    sql,
    TEXT,
    Boolean,
)
from sqlalchemy.orm import relationship
from pydantic import EmailStr
from starlette.requests import Request

from core.base import Base
from . import post
from helpers import UploadFile


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


class User(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True)
    full_name: str = Column(String(30), index=True)
    sex = Column(Enum(Gender), default=Gender.UNKNOWN, index=True)
    username: EmailStr = Column(String, index=True, nullable=False)
    email: EmailStr = Column(String, index=True, default="mail@mail.ru")
    hashed_password: str = Column(String, default="sdfsdfsdffsdffsd")
    is_admin: Boolean = Column(Boolean, default=False)
    is_active: Boolean = Column(Boolean, default=True)
    avatar: Union[File, UploadFile, None] = Column(
        ImageField(
            upload_storage="user-avatar",
            thumbnail_size=(128, 128),
            validators=[SizeValidator(max_size="100k")],
        )
    )

    posts = relationship("Post", back_populates="publisher")
    comments = relationship("Comment", back_populates="user")

    async def __admin_reper__(self, request: Request):
        return self.full_name

    async def __admin_select2_repr__(self, request: Request) -> str:
        url = None
        if self.avatar is not None:
            storage, file_id = self.avatar.path.split("/")
            url = request.url_for(
                request.app.state.ROUTE_NAME + ":api:file",
                storage=storage,
                file_id=file_id,
            )
        template_str = (
            '<div class="d-flex align-items-center"><span class="me-2 avatar'
            ' avatar-xs"{% if url %} style="background-image:'
            ' url({{url}});--tblr-avatar-size: 1.5rem;{%endif%}">{% if not url'
            " %}obj.full_name[:2]{%endif%}</span>{{obj.full_name}} <div>"
        )
        return Template(template_str, autoescape=True).render(obj=self, url=url)
