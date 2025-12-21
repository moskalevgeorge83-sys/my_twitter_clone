"""Smoke тест — проверка запуска приложения."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_root():
    """Проверяет доступность главной страницы SPA."""
    response = client.get("/")
    assert response.status_code == 200
