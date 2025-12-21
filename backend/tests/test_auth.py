"""Тесты аутентификации по API ключу."""


def test_no_api_key(client):
    """Проверяет 401 без api-key заголовка."""
    response = client.get("/api/tweets/")
    assert response.status_code == 401


def test_wrong_api_key(client):
    """Проверяет 401 с неверным api-key."""
    response = client.get("/api/tweets/", headers={"api-key": "wrong-key"})
    assert response.status_code == 401


def test_valid_api_key(auth_client):
    """Проверяет успешный доступ с валидным api-key=123."""
    response = auth_client.get("/api/tweets/")
    assert response.status_code == 200
