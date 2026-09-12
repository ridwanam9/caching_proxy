from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app import server
from app.server import app, cache
from unittest.mock import AsyncMock, Mock, patch

client = TestClient(app)


def test_cache_miss():
    cache.clear()
    server.origin = "http://test-origin"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {
        "content-type": "application/json"
    }
    mock_response.json.return_value = {
        "id": 1,
        "title": "Test Product"
    }

    with patch(
        "httpx.AsyncClient.get",
        new_callable=AsyncMock,
        return_value=mock_response
    ):
        response = client.get("/products/1")

    assert response.status_code == 200
    assert response.headers["X-Cache"] == "MISS"