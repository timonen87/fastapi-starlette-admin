from fastapi import APIRouter, Request, Depends
from datetime import timedelta
from fastapi import Depends, APIRouter, Request, Response, status
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from jinja2 import TemplateNotFound
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from models import User
import schemas
from services.security import ALGORITHM, oauth2_scheme_token

from services import (
    get_current_user,
    get_user_by_username,
    get_hash_password,
    create_user,
    get_hash_password,
    authenticate_user,
    create_access_token,
)
from services.security import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="", tags=["Pages"])

templates = Jinja2Templates(directory="templates")


# @router.get("/home")
# async def main(request: Request):
#     return templates.TemplateResponse("home/index.html", {"request": request})


# @router.get("/{path}")
# async def get_page(request: Request, path: str):
#     return templates.TemplateResponse(f"home/{path}", {"request": request})


# @router.get("/home")
# def get_home(request: Request):
#     return templates.TemplateResponse("home/index.html", {"request": request})


# @router.get("/home", response_class=HTMLResponse)
# def index(request: Request, token: str = Depends(oauth2_scheme)):
#     context = {"token": token, "request": request}
#     return templates.TemplateResponse("home/index.html", context)


# @router.get("/home/{page}")
# def get_page(
#     request: Request,
#     page: str,
#     user: User = Depends(get_current_user),
# ):
#     return templates.TemplateResponse(
#         f"home/{page}", {"request": request, "user": user}
#     )


# @router.get("/")
# def get_index(request: Request):
#     try:
#         return templates.TemplateResponse("home/index.html", {"request": request})
#     except TemplateNotFound:
#         return templates.TemplateResponse(
#             "home/page-404.html", {"request": request}, status_code=404
#         )


# @router.get("/")
# async def route_default(response: Response):
#     response = RedirectResponse(url="/login")

#     return response


@router.get("/index", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "home/index.html",
        {"request": request, "current_user": user, "segment": "index"},
    )


@router.get("/{template}", response_class=HTMLResponse)
async def route_template(
    request: Request, template: str, user: User = Depends(get_current_user)
):
    if not template.endswith(".html"):
        template += ".html"

    # Detect the current page
    segment = get_segment(request)

    # Serve the file (if exists) from app/templates/home/FILE.html
    return templates.TemplateResponse(
        f"home/{template}",
        {"request": request, "current_user": user, "segment": segment},
    )


def get_segment(request):
    try:
        segment = request.url.path.split("/")[-1]

        if segment == "":
            segment = "index"

        return segment

    except:
        return None


@router.get("/signup")
def get_signup(request: Request):
    return templates.TemplateResponse(
        "home/examples-register.html", {"request": request}
    )


@router.post("/signup")
def create_new_user(
    request: Request,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    db_user = get_user_by_username(db=db, username=form_data.email)
    if db_user:
        error = "E-mail уже существует"
        return templates.TemplateResponse(
            "home/examples-register.html",
            {"request": request, "error": error},
            status_code=301,
        )
    else:
        new_user = User(
            email=form_data.email,
            username=form_data.email,
            password=get_hash_password(form_data.password),
        )
        user = create_user(db=db, signup=new_user)
        return templates.TemplateResponse(
            "home/examples-login.html",
            {"request": request, "user": user},
            status_code=200,
        )


@router.get("/signin")
def get_signin(request: Request):
    return templates.TemplateResponse("home/examples-login.html", {"request": request})


@router.post("/signin", response_model=schemas.Token)
def login_for_access_token(
    response: Response,
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        error = "Неверный логин или пароль "
        return templates.TemplateResponse(
            "home/examples-login.html",
            {"error": error, "request": request},
            status_code=301,
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)

    # to save token in cookie
    # response.set_cookie(
    #     key="access_token", value=f"Bearer {access_token}", httponly=True
    # )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return response
