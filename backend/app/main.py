from fastapi import FastAPI

from .api.routes import medias, spa, tweets, users
from .api.routes.static import setup_static
from .startup import create_app

app: FastAPI = create_app()

# SPA роуты
app.include_router(spa.router)

# API роуты
app.include_router(tweets.router, prefix="/api")
app.include_router(medias.router, prefix="/api")
app.include_router(users.router, prefix="/api")

# Статические файлы
setup_static(app)
