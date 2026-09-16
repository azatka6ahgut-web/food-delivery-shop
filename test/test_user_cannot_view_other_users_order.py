def test_user_cannot_view_other_users_order(api_client, auth_headers, second_user_headers):
    products = api_client.get("/products").json()
    product_id = products[1]["id"]
    api_client.post("/cart/items", headers=auth_headers , json={"product_id": product_id , "quantity": 2})
    response = api_client.post("/orders", headers=auth_headers ,json={"delivery_address": "Техническая"})
    order_id = response.json()["id"]
    view = api_client.get(f"/orders/{order_id}", headers=second_user_headers)
    assert view.status_code == 403
    

