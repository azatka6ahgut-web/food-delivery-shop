def test_empty_cart_returns_zero_total(api_client, auth_headers):
    response = api_client.get("/cart", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["total"] == 0


def test_add_item_to_cart(api_client, auth_headers):
    products = api_client.get("/products").json()
    product_id = products[0]["id"]

    response = api_client.post(
        "/cart/items",
        headers=auth_headers,
        json={"product_id": product_id, "quantity": 2},
    )

    assert response.status_code == 201
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["quantity"] == 2


def test_add_same_item_twice_increases_quantity(api_client, auth_headers):
    products = api_client.get("/products").json()
    product_id = products[0]["id"]

    api_client.post(
        "/cart/items",
        headers=auth_headers,
        json={"product_id": product_id, "quantity": 1},
    )
    response = api_client.post(
        "/cart/items",
        headers=auth_headers,
        json={"product_id": product_id, "quantity": 2},
    )

    body = response.json()
    assert (
        len(body["items"]) == 1
    )  # не два разных элемента, а один с увеличенным количеством
    assert body["items"][0]["quantity"] == 3


def test_cart_requires_authentication(api_client):
    response = api_client.get("/cart")

    assert response.status_code == 401
