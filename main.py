

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from conf import config
from blog import admin as admin_star


async def homepage(request):
    return Jinja2Templates("templates").TemplateResponse(
        "index.html", {"request": request, "config": config}
    )


app = Starlette(
    routes=[
        Route("/", homepage),
        Mount("/statics", app=StaticFiles(directory="statics"), name="statics"),
    ]
)
admin_star.mount_to(app)


