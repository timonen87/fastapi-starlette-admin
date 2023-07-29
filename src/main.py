from fastapi import FastAPI
from fastapi import Depends, APIRouter, Request, Response, status
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import uvicorn

from config import config
from admin_app import admin as admin_star

# from pages.router import router as router_pages
# from user import router as user_router
# from core.base import Base
# from core.database import engine
from routers import users
from pages.router import router as adminlte_router
from starlette.exceptions import HTTPException as StarletteHTTPException

# templates = Jinja2Templates(directory="templates/")


def create_app():
    app = FastAPI()

    mount_static(app)
    custom_error_pages(app)
    admin_star.mount_to(app)
    app.include_router(users.router)
    app.include_router(adminlte_router)

    return app


def mount_static(app):
    app.mount("/static", StaticFiles(directory="static", html=True), name="static")


def custom_error_pages(app):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        templates = Jinja2Templates(directory="templates/")

        if exc.status_code == 403 or exc.status_code == 404 or exc.status_code == 500:
            return templates.TemplateResponse(
                f"home/page-{exc.status_code}.html", {"request": request}
            )

        if exc.status_code == 401:
            return templates.TemplateResponse(
                "home/page-403.html", {"request": request}
            )

        return templates.TemplateResponse(
            "home/page-error.html", {"request": request, "exc": exc}
        )


apps = create_app()

if __name__ == "__main__":
    uvicorn.run(apps, host="localhost", port=8000)
