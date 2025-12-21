"""Тесты роутов пользователей и подписок."""


def test_get_me(auth_client):
    """Проверяет получение профиля текущего пользователя."""
    resp = auth_client.get("/api/users/me")
    assert resp.status_code == 200
    assert resp.json()["user"]["name"] == "User1"


def test_get_nonexistent_user(auth_client):
    """Проверяет 404 для несуществующего пользователя."""
    resp = auth_client.get("/api/users/999")
    assert resp.status_code == 404  # из UserService


def test_follow_user(auth_client):
    """Проверяет подписку на другого пользователя."""
    resp = auth_client.post("/api/users/2/follow")  # User1 follows User2
    assert resp.status_code == 200


def test_toggle_follow(auth_client):
    """Проверяет переключение подписки/отписки."""
    # Follow
    follow_resp = auth_client.post("/api/users/2/follow")
    assert follow_resp.status_code == 200

    # Unfollow
    unfollow_resp = auth_client.delete("/api/users/2/follow")
    assert unfollow_resp.status_code == 200
    assert unfollow_resp.json()["result"] is True
