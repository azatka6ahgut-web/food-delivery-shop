from pages import LoginPage

def test_login_via_page_object_with_class(api_client, page, unique_email):
    api_client.post("/auth/register", json={"email": unique_email, "password": "secret123"})
    page.goto('http://localhost:8000/login.html')
    login_page = LoginPage(page)
    login_page.login(unique_email, "secret123")

    assert page.url == 'http://localhost:8000/'
    
