
from typing import Optional

import os

from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver

from sqlalchemy_file.storage import StorageManager
from starlette.staticfiles import StaticFiles

from core.database import engine

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette_admin import DropDown, I18nConfig
from starlette_admin.i18n import SUPPORTED_LOCALES
from starlette_admin.contrib.sqla import Admin as BaseAdmin
from starlette_admin.views import Link

from conf import config
from blog.models import Post, User, Comment
from blog.auth import MyAuthProvider
# from blog.models import Comment, Post, User
from blog.views import CommentView, HomeView, PostView, UserView

__all__ = ["engine", "admin"]

upload_dir: str = "upload/"
os.makedirs(f"{upload_dir}/avatars", 0o777, exist_ok=True)
container = get_driver(Provider.LOCAL)(upload_dir).get_container("avatars")
StorageManager.add_storage("user-avatar", container)

class Admin(BaseAdmin):
    def custom_render_js(self, request: Request) -> Optional[str]:
        return request.url_for("statics", path="js/custom_render.js")


# app.mount("/statics",StaticFiles(directory="statics", html=True), name="statics")

admin = Admin(
    engine,
    title="GetSpy Admin",
    base_url="/admin/sqla",
    route_name="admin-sqla",
    templates_dir="templates/admin/sqla",
    logo_url="https://preview.tabler.io/static/logo-white.svg",
    login_logo_url="https://preview.tabler.io/static/logo.svg",
    index_view=HomeView(label="Home", icon="fa fa-home"),
    auth_provider=MyAuthProvider(login_path="/sign-in", logout_path="/sign-out"),
    middlewares=[Middleware(SessionMiddleware, secret_key=config.secret)],
    i18n_config=I18nConfig(default_locale="en", language_switcher=SUPPORTED_LOCALES),
)

admin.add_view(UserView(User, icon="fa fa-users"))
admin.add_view(PostView(Post, label="blog Posts", icon="fa fa-blog"))
admin.add_view(CommentView(Comment, icon="fa fa-comments"))
admin.add_view(
    DropDown(
        "Resources",
        icon="fa fa-book",
        views=[
            Link(
                "StarletteAdmin Docs",
                url="https://jowilf.github.io/starlette-admin/",
                target="_blank",
            ),
            Link(
                "SQLAlchemy-file Docs",
                url="https://jowilf.github.io/sqlalchemy-file/",
                target="_blank",
            ),
        ],
    )
)
admin.add_view(Link(label="Go Back to Home", icon="fa fa-link", url="/"))