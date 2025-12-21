"""Тесты загрузки медиафайлов и привязки к твитам."""


def test_upload_media(auth_client):
    """Проверяет успешную загрузку медиафайла."""
    test_file_data = b"test image content"
    files = {"file": ("test.png", test_file_data, "image/png")}

    response = auth_client.post("/api/medias/", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "media_id" in data
    assert data["media_id"] > 0


def test_create_tweet_with_media(auth_client):
    """Проверяет создание твита с прикреплённым медиафайлом."""
    # 1. Загрузить медиа
    test_file_data = b"test image"
    files = {"file": ("test.jpg", test_file_data, "image/jpeg")}
    media_resp = auth_client.post("/api/medias/", files=files)
    media_id = media_resp.json()["media_id"]

    # 2. Создать твит с медиа ID
    tweet_resp = auth_client.post(
        "/api/tweets/",
        json={"tweet_data": "Твит с картинкой!", "tweet_media_ids": [media_id]},
    )
    assert tweet_resp.status_code == 200
