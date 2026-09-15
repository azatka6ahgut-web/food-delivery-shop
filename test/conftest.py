import uuid

import httpx
import pytest

BASE_URL = "http://localhost:8000"


@pytest.fixture
def api_client():
    """Готовый HTTP-клиент для обращения к нашему API."""
    with httpx.Client(base_url=BASE_URL) as client:
        yield client


@pytest.fixture
def unique_email():
    """Каждый вызов даёт новый email, чтобы тесты не мешали друг другу."""
    return f"user_{uuid.uuid4().hex[:8]}@example.com"

@pytest.fixture
def auth_headers(api_client, unique_email):
    """Регистрирует нового пользователя и возвращает готовые заголовки с токеном."""
    api_client.post(
        "/auth/register",
        json={"email": unique_email, "password": "secret123"},
    )
    response = api_client.post(
        "/auth/login",
        data={"username": unique_email, "password": "secret123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
