def test_admin_changed_status_order_true(
    api_client, auth_headers, admin_headers, second_user_headers
):
    products = api_client.get("/products").json()
    product_id = products[0]["id"]
    api_client.post(
        "/cart/items",
        headers=auth_headers,
        json={"product_id": product_id, "quantity": 2},
    )
    response = api_client.post(
        "/orders", headers=auth_headers, json={"delivery_address": "Техническая"}
    )
    order_id = response.json()["id"]
    order_status = response.json()["status"]
    admin_change = api_client.patch(
        f"/orders/{order_id}/status",
        headers=admin_headers,
        json={"status": "delivered"},
    )

    assert admin_change.status_code == 200

    user_change = api_client.patch(
        f"/orders/{order_id}/status",
        headers=second_user_headers,
        json={"status": "delivered"},
    )

    assert user_change.status_code == 403
