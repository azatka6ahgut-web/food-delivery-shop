from pages import LoginPage , CheckoutPage
from playwright.sync_api import expect

def test_login_via_page_object_with_class(api_client, page, unique_email):
    api_client.post("/auth/register", json={"email": unique_email, "password": "secret123"})
    page.goto('http://localhost:8000/login.html')
    login_page = LoginPage(page)
    login_page.login(unique_email, "secret123")

    assert page.url == 'http://localhost:8000/'

def test_full_checkout_flow_via_ui(api_client, page, unique_email):
    api_client.post("/auth/register", json={"email": unique_email, "password": "secret123"})
    page.goto('http://localhost:8000/login.html')
    login_page = LoginPage(page)
    login_page.login(unique_email, "secret123")
    first_card = page.locator('[data-testid="product-card"]').first
    add_button = first_card.locator('[data-testid="add-to-cart-btn"]')
    add_button.click()    
    expect(page.locator('#cart-count')).to_contain_text("1")
    page.goto('http://localhost:8000/cart.html')
    page.locator('[data-testid="checkout-btn"]').click()
    pay_page = CheckoutPage(page)
    pay_page.pay("Test_adres", "4242424242424242", "12/28", "322")
    page.wait_for_url("http://localhost:8000/orders.html")
    expect(page.locator('[data-testid="success-message"]')).to_contain_text("оплачен")


def test_full_checkout_flow_via_ui_bad_flow(api_client, page, unique_email):
    api_client.post("/auth/register", json={"email": unique_email, "password": "secret123"})
    page.goto('http://localhost:8000/login.html')
    login_page = LoginPage(page)
    login_page.login(unique_email, "secret123")
    first_card = page.locator('[data-testid="product-card"]').first
    add_button = first_card.locator('[data-testid="add-to-cart-btn"]')
    add_button.click()    
    expect(page.locator('#cart-count')).to_contain_text("1")
    page.goto('http://localhost:8000/cart.html')
    page.locator('[data-testid="checkout-btn"]').click()
    pay_page = CheckoutPage(page)
    pay_page.pay("Test_adres", "4000000000000002", "12/28", "322")
    expect(page.locator('[data-testid="error-message"]')).to_contain_text("отклонена")


    
    
