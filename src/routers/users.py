from datetime import datetime, timedelta
from typing import Any, List, Optional

from fastapi import Depends, HTTPException, Response, status, Request

from fastapi.templating import Jinja2Templates

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

# from fastapi_pagination import Page, pagination_params
# from fastapi_pagination.api import response
# from fastapi_pagination.ext.sqlalchemy import paginate
import schemas
from models import User

from core.database import get_db

from services import (
    authenticate_user,
    create_access_token,
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
    get_users,
    update_user,
    get_current_active_user,
    get_current_user,
)
from services.security import ACCESS_TOKEN_EXPIRE_MINUTES

templates = Jinja2Templates(directory="templates/")

router: Any = APIRouter(
    tags=["users"],
    responses={404: {"Description": "Not found"}},
)


# @router.get("/admin/home")
# def get_index(request: Request, current_user: User = Depends(get_current_user)):
#     try:
#         return templates.TemplateResponse(
#             "home/index.html", {"request": request, "user": current_user}
#         )
#     except:
#         return templates.TemplateResponse(
#             "home/examples-login.html", {"request": request}
#         )


@router.post(
    "/users",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> Any:
    db_username = get_user_by_username(db, username=user.username)
    db_email = get_user_by_email(db, email=user.email)
    deb_id = get_user_by_id(db, user_id=user.id)
    if db_username:
        raise HTTPException(
            status_code=400,
        )
    elif db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    elif deb_id:
        raise HTTPException(status_code=400, detail="User id exists")
    return create_user(db=db, user=user)


# @router.get(
#     "/users",
#     response_model=Page[schemas.Users],
#     dependencies=[Depends(pagination_params)],
# )
# def list_users(db: Session = Depends(get_db)) -> List:
#     users = get_users(db=db)
#     return paginate(users)


@router.get("/users/user", response_model=schemas.User)
def read_user(
    username: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get data about user
    """
    if username:
        db_user = get_user_by_username(db=db, username=username)
    elif user_id:
        db_user = get_user_by_id(db=db, user_id=user_id)
    else:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: Response = None,  # noqa
) -> Any:
    """
    Generate a token to access endpoints
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token_data = {"access_token": access_token, "token_type": "bearer"}
    response.set_cookie(
        key="token",
        value=access_token,
        max_age=access_token_expires.total_seconds(),
        httponly=True,
    )
    return token_data


@router.put(
    "/users/{username}",
    response_model=schemas.User,
    response_model_exclude_none=True,
)
def update_user_data(
    username: str,
    user: schemas.user.UserUpdate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    The password field is optional
    """
    if username != current_user.username:
        raise HTTPException(status_code=403, detail="Don't have permission")

    result = update_user(db, user, username)

    return result
