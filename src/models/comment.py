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
from . import post
from . import user




class Comment(Base):
    __tablename__ = 'comment'
    pk: int = Column(Integer,primary_key=True)
    content: str = Column(TEXT)
    created_at: Optional[datetime] = Column(DateTime(timezone=True), server_default=sql.func.now())

    post_id: Optional[int] = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='comments')

    user_id: Optional[int] = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='comments')



