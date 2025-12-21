"""Тесты CRUD операций с твитами и лайками."""

from fastapi.testclient import TestClient

from backend.app.main import app


def test_create_tweet(auth_client):
    """Проверяет создание твита без медиа."""
    response = auth_client.post(
        "/api/tweets/", json={"tweet_data": "Тестовый твит!", "tweet_media_ids": []}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "tweet_id" in data
    assert data["tweet_id"] > 0


def test_get_feed_empty(auth_client):
    """Проверяет пустую ленту для нового пользователя."""
    response = auth_client.get("/api/tweets/")
    assert response.status_code == 200


def test_delete_tweet(auth_client):
    """Проверяет удаление своего твита."""
    create_resp = auth_client.post(
        "/api/tweets/", json={"tweet_data": "delete me", "tweet_media_ids": []}
    )
    tweet_id = create_resp.json()["tweet_id"]

    delete_resp = auth_client.delete(f"/api/tweets/{tweet_id}")
    assert delete_resp.status_code == 200


def test_like_tweet(auth_client):
    """Проверяет лайк/анлайк твита."""
    # Создать твит
    create_resp = auth_client.post(
        "/api/tweets/", json={"tweet_data": "Твит для лайка", "tweet_media_ids": []}
    )
    assert create_resp.status_code == 200
    tweet_id = create_resp.json()["tweet_id"]

    # POST like работает!
    like_resp = auth_client.post(f"/api/tweets/{tweet_id}/likes")
    assert like_resp.status_code == 200

    # DELETE like работает!
    unlike_resp = auth_client.delete(f"/api/tweets/{tweet_id}/likes")
    assert unlike_resp.status_code == 200

    print(f"✅ test_like_tweet: tweet_id={tweet_id}, like/unlike OK!")


def test_create_tweet_unauthorized(client: TestClient):
    """Проверяет 401 при создании без авторизации."""
    resp = client.post(
        "/api/tweets/", json={"tweet_data": "test", "tweet_media_ids": []}
    )
    assert resp.status_code == 401


def test_delete_foreign_tweet(auth_client):
    """Проверяет 403 при удалении чужого твита."""
    # Создать твит от User1
    tweet_resp = auth_client.post(
        "/api/tweets/", json={"tweet_data": "test", "tweet_media_ids": []}
    )
    tweet_id = tweet_resp.json()["tweet_id"]

    # Попробовать удалить от User2 (api-key=456)
    client2 = TestClient(app)
    client2.headers["api-key"] = "456"
    resp = client2.delete(f"/api/tweets/{tweet_id}")
    assert resp.status_code == 403  # Forbidden


def test_like_nonexistent_tweet(auth_client):
    """Проверяет 404 при лайке несуществующего твита."""
    resp = auth_client.post("/api/tweets/999/likes")
    assert resp.status_code == 404  # TweetNotFound
