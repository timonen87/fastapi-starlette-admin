from typing import Any, Optional

from pydantic import BaseModel, StrictBool, validator


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str

    @validator("username")
    def validate_username(cls: Any, username: str, **kwargs: Any) -> Any:
        if len(username) == 0:
            raise ValueError("Username can t be empty")
        return username

    @validator("email")
    def validate_email(cls: Any, email: str, **kwargs: Any) -> Any:
        if len(email) == 0:
            raise ValueError("An email is required")
        return email


class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode: bool = True


class UserInDb(User):
    hashed_password: str


class Users(User):
    id: int


class UserUpdate(UserBase):
    password: Optional[str]

    class Config:
        orm_mode: bool = True


class UserPassword(BaseModel):
    password: Optional[str] = None
