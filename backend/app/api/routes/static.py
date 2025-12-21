"""Настройка статических файлов для SPA и медиа."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def setup_static(app: FastAPI) -> None:
    """Монтирует все статические директории в приложение.

    Пути:
    * `/static` → frontend/static/
    * `/css` → frontend/static/css/
    * `/js` → frontend/static/js/
    * `/media` → media/ (загруженные файлы)
    """
    app.mount("/static", StaticFiles(directory="frontend/static"))
    app.mount("/css", StaticFiles(directory="frontend/static/css"))
    app.mount("/js", StaticFiles(directory="frontend/static/js"))
    app.mount("/media", StaticFiles(directory="media"), name="media")
