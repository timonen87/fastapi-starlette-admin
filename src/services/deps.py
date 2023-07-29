from typing import Any, Generator

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import schemas
from config import SECRET_AUTH
from core.database import SessionLocal

from .security import ALGORITHM, oauth2_scheme_signin, oauth2_scheme_token
from .users import get_user_by_username


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme_signin), db: Session = Depends(get_db)
):
    payload = jwt.decode(
        token,
        SECRET_AUTH,
        algorithms=[ALGORITHM],
    )
    user: str = get_user_by_username(db=db, username=payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_user_by_token(
    token: str = Depends(oauth2_scheme_token), db: Session = Depends(get_db)
):
    payload = jwt.decode(
        token,
        SECRET_AUTH,
        algorithms=[ALGORITHM],
    )
    user: str = get_user_by_username(db=db, username=payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# def get_current_user(
#     db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
# ) -> Any:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, config.secret, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         token_data = schemas.TokenData(username=username)
#     except JWTError:  # pragma: no cover
#         raise credentials_exception
#     user = get_user_by_username(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    if current_user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    return current_user


def get_current_admin(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme_signin)
):
    payload = jwt.decode(token, config.secret, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    token_data = schemas.TokenData(username=username)
    user = get_user_by_username(db, username=token_data.username)
    if user and user.is_admin == True:
        return user.username
    else:
        raise HTTPException(
            status_code=302,
            detail="Not authorized",
            # headers={"Location": "/signin"}
        )
