from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import Session

from .db.base import create_test_users, get_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация БД при старте, cleanup при завершении"""
    db: Session = next(get_db())
    try:
        init_db()
        create_test_users(db)
        print("✅ БД готова!")
        yield
    finally:
        db.close()


def create_app() -> FastAPI:
    """Фабрика приложения"""
    app = FastAPI(lifespan=lifespan, title="Twitter Clone")
    return app
