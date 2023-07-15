# import enum
# from datetime import datetime
# from typing import Optional, Union, List
#
# from pydantic import EmailStr
# from sqlalchemy import Column, String, Integer, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy_file import ImageField, File
# from sqlalchemy_file.validators import SizeValidator
# from starlette.requests import Request
# from core.base import Base
# from helpers import UploadFile
#
# # class Gender(str, enum.Enum):
# #     MALE = "male"
# #     FEMALE = "female"
# #     UNKNOWN = "unknown"
# class User(Base):
#     __tablename__ = 'user'
#
#     id: Optional[int] = Column(Integer, primary_key=True)
#     full_name: str = Column(String(30), unique=True, index=True)
#     # sex: str = Column(Enum(Gender), default=Gender.UNKNOWN, index=True)
#     avatar: Union[File, UploadFile, None] = Column(ImageField(
#         upload_storage="user-avatar",
#         thumbnail_size=(128, 128),
#         validators=[SizeValidator(max_size="100k")],
#     ))
#     username: EmailStr = Column(String, unique=True, index=True, nullable=False)
#     password: str = Column(String(20), nullable=False)
#
#     posts = relationship('Post', back_populates='publisher')
#     comments = relationship('Comment', back_populates='user')
#
#
#     async  def __admin_reper__(self, request: Request):
#         return self.full_name
#
