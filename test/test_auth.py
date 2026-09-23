def test_register_new_user_succeeds(api_client, unique_email):
    response = api_client.post(
        "/auth/register",
        json={"email": unique_email, "password": "secret123"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == unique_email
    assert body["is_admin"] is False


def test_register_duplicate_email_fails(api_client, unique_email):
    payload = {"email": unique_email, "password": "secret123"}
    api_client.post("/auth/register", json=payload)  # первая регистрация — ок

    response = api_client.post(
        "/auth/register", json=payload
    )  # повторная — должна упасть

    assert response.status_code == 400


def test_login_with_correct_credentials_returns_token(api_client, unique_email):
    api_client.post(
        "/auth/register",
        json={"email": unique_email, "password": "secret123"},
    )

    response = api_client.post(
        "/auth/login",
        data={"username": unique_email, "password": "secret123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_wrong_password_fails(api_client, unique_email):
    api_client.post(
        "/auth/register",
        json={"email": unique_email, "password": "secret123"},
    )

    response = api_client.post(
        "/auth/login",
        data={"username": unique_email, "password": "wrong-password"},
    )

    assert response.status_code == 401
