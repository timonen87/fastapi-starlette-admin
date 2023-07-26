from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get('/home')
async def main(request: Request):
    return templates.TemplateResponse("home/index.html", {"request": request})

@router.get('/{path}')
async def get_page(request: Request, path: str):
    return templates.TemplateResponse(f"home/{path}", {"request": request})
