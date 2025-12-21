"""Pytest фикстуры для тестирования FastAPI + SQLAlchemy."""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Переключаем на SQLite для тестов
os.environ["TEST_MODE"] = "1"
os.environ["DATABASE_URL"] = "sqlite:///./test_twitter.db"

from backend.app.core.security import create_test_users
from backend.app.db.base import Base, get_db
from backend.app.main import app

TEST_DATABASE_URL = "sqlite:///./test_twitter.db"
test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=test_engine)

# Создаём тестовую схему БД
Base.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> sessionmaker:
    """Изолированная БД сессия для каждого теста.

    Гарантирует:
    * Чистая БД в начале
    * Rollback изменений после теста
    * Тестовые пользователи созданы
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    create_test_users(session)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: sessionmaker) -> TestClient:
    """TestClient с переопределённой БД сессией."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def auth_client(client: TestClient) -> TestClient:
    """TestClient с авторизацией (api-key=123, User1)."""
    client.headers["api-key"] = "123"
    return client
