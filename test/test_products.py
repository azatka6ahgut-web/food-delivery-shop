def test_products_not_empty(api_client):
    response = api_client.get('/products')
    assert len(response.json()) > 0
    assert isinstance(response.json(), list)

def test_products_fillter_unknow_category(api_client):
    response = api_client.get('/products', params={'category': 'несуществующая_категория_123'},)
    assert response.status_code == 200
    assert response.json() == []

def test_products_non_exits_id(api_client , auth_headers):
    response = api_client.get('/products/43453', headers=auth_headers)
    assert response.status_code == 404