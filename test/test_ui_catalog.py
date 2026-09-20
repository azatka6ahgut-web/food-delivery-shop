from playwright.sync_api import expect


def test_cui_catalog(page):
    page.goto("http://localhost:8000")
    assert page.title() == "ЗелёнаяКорзина — Доставка продуктов"
    assert "Каталог продуктов" in page.title() or "ЗелёнаяКорзина" in page.title()

def test_catalog_shows_products(page):
    page.goto("http://localhost:8000")
    product = page.locator('[data-testid="product-card"]')
    assert product.count() >0

def test_add_product_to_cart_updates_badge(page):
    page.goto('http://localhost:8000')
    first_card = page.locator('[data-testid="product-card"]').first
    add_button = first_card.locator('[data-testid="add-to-cart-btn"]')
    add_button.click()
    assert page.url == "http://localhost:8000/login.html"

def test_add_product_to_cart_updates_badge_2(page, auth_headers):
    token = auth_headers["Authorization"].replace("Bearer ", "")
    page.goto("http://localhost:8000")
    page.evaluate(f"localStorage.setItem('access_token', '{token}')")
    page.reload()
    first_card = page.locator('[data-testid="product-card"]').first
    add_button = first_card.locator('[data-testid="add-to-cart-btn"]')
    add_button.click()
    expect(page.locator("#cart-count")).to_have_text("1")

def _login_via_ui(page, api_client, unique_email):
    api_client.post("/auth/register", json={"email": unique_email , "password": "secret123"})
    page.goto("http://localhost:8000/login.html")
    page.locator('#login-email').fill(unique_email)
    page.locator('#login-password').fill("secret123")
    page.locator('[data-testid="login-submit-btn"]').click()
    page.wait_for_url('http://localhost:8000')


