import pytest

@pytest.mark.smoke
def test_health_check_returns_ok(api_client):
    response = api_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_products_list_returns_items(api_client):
    response = api_client.get("/products")

    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0


def test_single_product_has_expected_fields(api_client):
    products = api_client.get("/products").json()
    first_product_id = products[0]["id"]

    response = api_client.get(f"/products/{first_product_id}")

    assert response.status_code == 200
    product = response.json()
    assert "name" in product
    assert "price" in product
    assert product["price"] > 0
