def test_products_filtered_by_category_returns_only_that_category(api_client):
    response = api_client.get("/products", params={"category": "dairy"})
    products = response.json()

    assert response.json() != []
    assert response.status_code == 200
    assert isinstance(products , list) 

    for product in products:
        assert product["category"] == "dairy"
