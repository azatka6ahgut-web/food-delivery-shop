import uuid
import psycopg2
import httpx
import pytest
import allure

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


@pytest.fixture
def second_user_headers(api_client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    api_client.post(
        "/auth/register",
        json={"email": email, "password": "secret123"},
    )
    response = api_client.post(
        "/auth/login",
        data={"username": email, "password": "secret123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(api_client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    api_client.post(
        "/auth/register",
        json={"email": email, "password": "secret123"},
    )
    response = api_client.post(
        "/auth/login",
        data={"username": email, "password": "secret123"},
    )
    token = response.json()["access_token"]
    connection = psycopg2.connect(
        "postgresql://shop_user:shop_password@localhost:5432/food_delivery"
    )
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET is_admin = true WHERE email = %s", (email,))

    connection.commit()
    cursor.close()
    connection.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            allure.attach(
                page.screenshot(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
