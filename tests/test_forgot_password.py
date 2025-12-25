import time
from pages.forgot_password_page import ForgotPasswordPage
from pages.reset_password_page import ResetPasswordPage


# =========================
# TC1 – Quên mật khẩu hợp lệ
# =========================
def test_forgot_password_success(driver):
    forgot_page = ForgotPasswordPage(driver)
    forgot_page.open()

    forgot_page.submit_forgot_password(
        email="minhchi@gmail.com",     # email tồn tại DB
        phone="0327264556"          # phone đúng
    )

    time.sleep(1)
    assert "/reset-password/" in driver.current_url


# =========================
# TC2 – Email hoặc phone sai
# =========================
def test_forgot_password_wrong_info(driver):
    forgot_page = ForgotPasswordPage(driver)
    forgot_page.open()

    forgot_page.submit_forgot_password(
        email="minhchi@gmail.com",
        phone="0000000000"
    )

    error = forgot_page.get_backend_error()
    assert "Email hoặc số điện thoại không chính xác" in error


# =========================
# TC3 – Bỏ trống email
# =========================
def test_forgot_password_empty_email(driver):
    forgot_page = ForgotPasswordPage(driver)
    forgot_page.open()

    forgot_page.submit_forgot_password(
        email="",
        phone="0912345678"
    )

    validation_message = forgot_page.get_input_validation("email")
    assert validation_message != ""


# =========================
# TC4 – Reset mật khẩu thành công
# =========================
def test_reset_password_success(driver):
    driver.get("http://127.0.0.1:8000/reset-password/1")

    reset_page = ResetPasswordPage(driver)
    reset_page.reset_password(
        password="123456",
        password_confirm="123456"
    )

    # Chờ redirect sang login
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    WebDriverWait(driver, 10).until(EC.url_contains("/login"))

    assert "/login" in driver.current_url


# =========================
# TC5 – Password không khớp
# =========================
def test_reset_password_not_match(driver):
    driver.get("http://127.0.0.1:8000/reset-password/1")

    reset_page = ResetPasswordPage(driver)
    reset_page.reset_password(
        password="123456",
        password_confirm="654321"
    )

    error = reset_page.get_error_message()
    assert "does not match" in error.lower()
