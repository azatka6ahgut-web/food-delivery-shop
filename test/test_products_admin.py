def test_add_products_without_authorization(api_client):
    response = api_client.post("/products", 
                                json={
                                "name": "test product", 
                                "price": 2
                                }) 
    assert response.status_code == 401


def test_create_products_default_user_expect_forbidden(api_client, auth_headers):
    response = api_client.post("/products",
                               headers=auth_headers,
                               json={
                                "name": "test product",
                                "price": 23,
                               })

    assert response.status_code == 403

    