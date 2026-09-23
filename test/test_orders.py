def test_create_order_from_cart_succeeds(api_client, auth_headers):
    products = api_client.get("/products").json()
    product_id = products[0]["id"]
    api_client.post(
        "/cart/items",
        headers=auth_headers,
        json={"product_id": product_id, "quantity": 2},
    )

    response = api_client.post(
        "/orders",
        headers=auth_headers,
        json={"delivery_address": "ул. Тестовая, 1"},
    )

    assert response.status_code == 201
    order = response.json()
    assert order["status"] == "pending"
    assert order["total"] > 0
    assert len(order["items"]) == 1


def test_order_creation_clears_the_cart(api_client, auth_headers):
    products = api_client.get("/products").json()
    product_id = products[0]["id"]
    api_client.post(
        "/cart/items",
        headers=auth_headers,
        json={"product_id": product_id, "quantity": 1},
    )

    api_client.post(
        "/orders", headers=auth_headers, json={"delivery_address": "ул. Тестовая, 1"}
    )

    cart = api_client.get("/cart", headers=auth_headers).json()
    assert cart["items"] == []


def test_create_order_with_empty_cart_fails(api_client, auth_headers):
    """Регрессионный тест на баг, который мы нашли вручную: заказ нельзя
    создать из пустой корзины — сервер должен вернуть 400 с понятной ошибкой."""
    response = api_client.post(
        "/orders",
        headers=auth_headers,
        json={"delivery_address": "ул. Тестовая, 1"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Cart is empty"
