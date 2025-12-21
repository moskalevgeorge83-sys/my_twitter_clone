"""Тесты SPA роутов и favicon."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("path", ["/", "/profile/1", "/profile/123"])
def test_spa_routes(client: TestClient, path):
    """Проверяет, что все SPA роуты возвращают index.html."""
    resp = client.get(path)
    assert resp.status_code == 200
    assert '<div id="app"></div>' in resp.text


def test_favicon(client: TestClient):
    """Проверяет доступность favicon.ico."""
    resp = client.get("/favicon.ico")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("image/")
