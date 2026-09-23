import pytest


def _create_order(api_client, auth_headers):
    products = api_client.get("/products").json()
    product_id = products[0]["id"]
    api_client.post(
        "/cart/items",
        headers=auth_headers,
        json={"product_id": product_id, "quantity": 1},
    )
    order = api_client.post(
        "/orders", headers=auth_headers, json={"delivery_address": "ул. Тестовая, 1"}
    ).json()
    return order["id"]


@pytest.mark.parametrize(
    "card_number, expected_status, expected_order_status",
    [
        ("4242424242424242", 200, "paid"),
        ("4000000000000002", 402, "payment_failed"),
    ],
)
def test_payment_outcomes(
    api_client, auth_headers, card_number, expected_status, expected_order_status
):
    order_id = _create_order(api_client, auth_headers)

    response = api_client.post(
        f"/payment/{order_id}",
        headers=auth_headers,
        json={"card_number": card_number, "card_expiry": "12/28", "card_cvv": "123"},
    )

    assert response.status_code == expected_status

    order = api_client.get(f"/orders/{order_id}", headers=auth_headers).json()
    assert order["status"] == expected_order_status
