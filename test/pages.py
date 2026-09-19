class CheckoutPage:
    def __init__(self, page):
        self.page = page
        self.address_input = page.locator('[data-testid="address-input"]')
        self.card_number_input = page.locator('[data-testid="card-number-input"]')
        self.card_expiry_input = page.locator('[data-testid="card-expiry-input"]')
        self.card_cvv_input = page.locator('[data-testid="card-cvv-input"]')
        self.pay_button = page.locator('[data-testid="pay-btn"]')
        self.success_message = page.locator('[data-testid="success-message"]')
        self.error_message = page.locator('[data-testid="error-message"]')

    def pay(self, address, card_number, expiry, cvv):
        self.address_input.fill(address)
        self.card_number_input.fill(card_number)
        self.card_expiry_input.fill(expiry)
        self.card_cvv_input.fill(cvv)
        self.pay_button.click()

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.login_email = page.locator('#login-email')
        self.login_password = page.locator('#login-password')
        self.login_submit_btn = page.locator('[data-testid="login-submit-btn"]')
        

    def login(self, email, password):
        self.login_email.fill(email)
        self.login_password.fill(password)
        self.login_submit_btn.click()
        self.page.wait_for_url('http://localhost:8000')