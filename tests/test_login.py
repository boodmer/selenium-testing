from pages.login_page import LoginPage
from selenium.webdriver.chrome.webdriver import WebDriver
import logging
import os

# Khởi tạo logger cho file này
logger = logging.getLogger(__name__)

# -----------------------------------
# TC1️ Không nhập email & password
# -----------------------------------
def test_login_without_email_and_password(driver):
    logger.info("[TC1] Không nhập Email và Password")
    login = LoginPage(driver)
    login.open()
    login.login("", "")

    # get_error_message lấy lỗi đầu tiên (email)
    error = login.get_error_message()
    assert "Vui lòng nhập email" in error

# -----------------------------------
# TC2 Không nhập email
# -----------------------------------
def test_login_without_email(driver):
    logger.info("[TC2] Không nhập Email")
    login = LoginPage(driver)
    login.open()
    login.login("", "123456")

    error = login.get_error_message()
    assert "Vui lòng nhập email" in error

# -----------------------------------
# TC3️ Không nhập password
# -----------------------------------
def test_login_without_password(driver):
    logger.info("[TC3] Không nhập Password")
    login = LoginPage(driver)
    login.open()
    login.login("nguyenminhieu12@gmail.com", "")

    error = login.get_second_error_message()
    assert "Vui lòng nhập mật khẩu" in error

# -----------------------------------
# TC4 Email sai định dạng
# -----------------------------------
def test_login_invalid_email_format(driver):
    logger.info("[TC4] Email sai định dạng")
    login = LoginPage(driver)
    login.open()
    login.login("abc123", "123456")

    error = login.get_error_message()
    assert "Bạn chưa nhập đúng định dạng email" in error

# -----------------------------------
# TC5 Sai email hoặc password
# -----------------------------------
def test_login_wrong_account(driver):
    logger.info("[TC5] Sai Email hoặc Password")
    login = LoginPage(driver)
    login.open()
    login.login("sai@gmail.com", "123456")

    flash = login.get_flash_message()
    assert "Email hoặc mật khẩu không chính xác" in flash

# -----------------------------------
# TC6 Đăng nhập thành công
# -----------------------------------
def test_login_success(driver):
    logger.info("[TC6] Đăng nhập thành công")
    TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "minhchi@gmail.com")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "12345678")
    login = LoginPage(driver)
    login.open()
    login.login(TEST_USER_EMAIL,TEST_USER_PASSWORD)

    flash = login.get_flash_message()
    assert "Đăng nhập thành công" in flash
