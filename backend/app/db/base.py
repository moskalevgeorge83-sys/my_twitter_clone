"""ORM настройка, движок БД и FastAPI dependency."""

from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from ..config import DATABASE_URL

# Глобальный движок БД (один на всё приложение)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для SQLAlchemy моделей
Base = declarative_base()


# FastAPI dependency для получения сессии БД
def get_db() -> Generator[Session, None, None]:
    """Dependency для внедрения БД сессии в роуты."""
    db: Session = SessionLocal()
    try:
        yield db  # Передаём сессию в роут
    finally:
        db.close()  # Гарантированное закрытие


# Инициализация схемы БД
def init_db() -> None:
    """Создаёт все таблицы из моделей при старте приложения."""
    Base.metadata.create_all(bind=engine)


# Инициализация тестовых данных
def create_test_users(db: Session) -> None:
    """Создаёт 3 тестовых пользователя при первом запуске.

    API ключи для тестов:
    * User1 → "123"
    * User2 → "456"
    * User3 → "789"
    """
    # Проверяем наличие пользователей (без импорта модели User)
    result = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
    if result > 0:
        print("ℹ️ Пользователи уже существуют")
        return

    # Вставляем напрямую через SQL (избегаем циклических импортов)
    test_users = [("User1", "123"), ("User2", "456"), ("User3", "789")]

    for name, api_key in test_users:
        db.execute(
            text("INSERT INTO users (name, api_key) VALUES (:name, :api_key)"),
            {"name": name, "api_key": api_key},
        )
    db.commit()
    print("Тестовые пользователи созданы!")
