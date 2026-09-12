from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app import server
from app.server import app, cache
from unittest.mock import AsyncMock, Mock, patch

client = TestClient(app)


# Cache MISS
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


# Cache HIT
def test_cache_hit():
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
    ) as mock_get:
        first_response = client.get("/products/1")
        second_response = client.get("/products/1")

    assert first_response.headers["X-Cache"] == "MISS"
    assert second_response.headers["X-Cache"] == "HIT"
    assert mock_get.call_count == 1



# Query Paremeter
def test_query_parameters_have_different_cache_keys():
    cache.clear()
    server.origin = "http://test-origin"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {
        "content-type": "application/json"
    }
    mock_response.json.return_value = {
        "products": []
    }

    with patch(
        "httpx.AsyncClient.get",
        new_callable=AsyncMock,
        return_value=mock_response
    ) as mock_get:
        first_response = client.get("/products?limit=5")
        second_response = client.get("/products?limit=10")

    assert first_response.headers["X-Cache"] == "MISS"
    assert second_response.headers["X-Cache"] == "MISS"
    assert mock_get.call_count == 2


# Clear Cache
def test_clear_cache():
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
    ) as mock_get:
        first_response = client.get("/products/1")

        assert first_response.headers["X-Cache"] == "MISS"

        clear_response = client.delete("/clear-cache")

        assert clear_response.status_code == 200

        second_response = client.get("/products/1")

    assert second_response.headers["X-Cache"] == "MISS"
    assert mock_get.call_count == 2


