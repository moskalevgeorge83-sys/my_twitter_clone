"""SPA роуты — все ведут на index.html."""

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Главная страница SPA."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/profile/{user_id}", response_class=HTMLResponse)
async def profile(user_id: int, request: Request) -> HTMLResponse:
    """Профиль пользователя — SPA роут."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/favicon.ico")
async def favicon() -> FileResponse:
    """Favicon иконка."""
    return FileResponse("frontend/static/favicon.ico")
