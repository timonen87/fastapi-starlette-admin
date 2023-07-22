from fastapi import FastAPI
from fastapi import Depends,APIRouter,Request,Response,status
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from conf import config
from blog.app import admin as admin_star


templates = Jinja2Templates(directory="templates/")

app = FastAPI()

app.mount("/statics",StaticFiles(directory="statics",html=True ), name="statics")

@app.get("/")
def get_signup(request:Request):
    return templates.TemplateResponse("index.html",{"request": request, "config": config})


# async def homepage(request):
#     return Jinja2Templates("templates").TemplateResponse(
#         "index.html", {"request": request, "config": config}
#     )

# app = Starlette(
#     routes=[
#         Route("/", homepage),
#         Mount("/statics", app=StaticFiles(directory="statics"), name="statics"),
#     ]
# )


admin_star.mount_to(app)

