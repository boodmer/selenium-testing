from matplotlib import testing
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pages.register_page import RegisterPage
import logging
logger = logging.getLogger(__name__)

@pytest.fixture
def driver():
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.wait = WebDriverWait(driver, 10)
    yield driver
    driver.quit()


# -----------------------------
# TC1. Test đăng ký thành công
# -----------------------------
def test_register_success(driver):
    logger.info("[TC1] Đăng kí tài khoản thành công")
    page = RegisterPage(driver)
    page.open()
    page.register(
        name="Nguyen Van A",
        phone="0912345678",
        birthday="12/11/2023",
        address="Ha Noi",
        email="testuser10@example.com",  # email ở mỗi lần đăng kí không được trùng lặp 
        password="123456",
        password_confirm="123456"
    )

    msg = page.get_flash_message()
    assert "Đăng ký tài khoản thành công" in msg


# -----------------------------
# TC2. Test bỏ trống trường dữ liệu họ tên
# -----------------------------
def test_register_missing_name(driver):
    logger.info("[TC2] Test bỏ trống trường dữ liệu họ tên")
    page = RegisterPage(driver)
    page.open()

    page.register(
        name="",                     # bỏ trống name
        phone="0912345678",
        birthday="2000-01-10",
        address="Ha Noi",
        email="user1@example.com",
        password="123456",
        password_confirm="123456"
    )

    msg = page.get_input_validation("name")
    assert msg != ""


# -----------------------------
# TC3. Test bỏ trống trường dữ liệu số điện thoại
# -----------------------------
def test_register_missing_phone(driver):
    logger.info("[TC3] Test bỏ trống trường dữ liệu số điện thoại")
    page = RegisterPage(driver)
    page.open()

    page.register(
        name="Name",
        phone="",                   # bỏ trống phone
        birthday="2000-01-10",
        address="Ha Noi",
        email="user1@example.com",
        password="123456",
        password_confirm="123456"
    )

    msg = page.get_input_validation("phone")
    assert msg != ""


# -----------------------------
# TC4. Test bỏ trống trường dữ liệu ngày sinh
# -----------------------------
def test_register_missing_birthday(driver):
    logger.info("[TC4] Test bỏ trống trường dữ liệu ngày sinh")
    page = RegisterPage(driver)
    page.open()

    page.register(
        name="name",
        phone="0912345678",
        birthday="",            # bỏ trống birthday
        address="Ha Noi",
        email="user1@example.com",
        password="123456",
        password_confirm="123456"
    )

    msg = page.get_input_validation("birthday")
    assert msg != ""


# -----------------------------
# TC5. Test bỏ trống trường dữ liệu địa chỉ
# -----------------------------
def test_register_missing_address(driver):
    logger.info("[TC5] Test bỏ trống trường dữ liệu địa chỉ")
    page = RegisterPage(driver)
    page.open()

    page.register(
        name="name",
        phone="0912345678",
        birthday="2000-01-10",
        address="",                     # bỏ trống address
        email="user1@example.com",
        password="123456",
        password_confirm="123456"
    )

    msg = page.get_input_validation("address")
    assert msg != ""


# -----------------------------
# TC6. Test bỏ trống trường dữ liệu email
# -----------------------------
def test_register_missing_email(driver):
    logger.info("[TC6] Test bỏ trống trường dữ liệu email")
    page = RegisterPage(driver)
    page.open()

    page.register(
        name="name",
        phone="0912345678",
        birthday="2000-01-10",
        address="Ha Noi",
        email="",                          # bỏ trống Email
        password="123456",
        password_confirm="123456"
    )

    msg = page.get_input_validation("email")
    assert msg != ""


# -----------------------------
# TC7. Test bỏ trống trường dữ liệu mật khẩu
# -----------------------------
def test_register_missing_password(driver):
    logger.info("[TC7] Test bỏ trống trường dữ liệu mật khẩu")
    page = RegisterPage(driver)
    page.open()

    page.register(
        name="name",
        phone="0912345678",
        birthday="2000-01-10",
        address="Ha Noi",
        email="user1@example.com",
        password="",                       # bỏ trống password
        password_confirm="123456"
    )

    msg = page.get_input_validation("password")
    assert msg != ""


# -----------------------------
# TC8. Test bỏ trống trường dữ liệu xác nhận mật khẩu
# -----------------------------
def test_register_missing_password_confirm(driver):
    logger.info("[TC8] Test bỏ trống trường dữ liệu xác nhận mật khẩu")
    page = RegisterPage(driver)
    page.open()

    page.register(
        name="name",
        phone="0912345678",
        birthday="2000-01-10",
        address="Ha Noi",
        email="user1@example.com",
        password="123456",
        password_confirm=""         # bỏ trống password_confirm
    )

    msg = page.get_input_validation("password_confirmation")
    assert msg != ""



# -----------------------------
# TC9. Test email sai định dạng
# -----------------------------
def test_register_invalid_email_format(driver):
    logger.info("[TC9] Test email sai định dạng")
    page = RegisterPage(driver)
    page.open()
    page.register(
        name="Nguyen Van A",
        phone="0912345678",
        birthday="2000-01-10",
        address="Ha Noi",
        email="abc123",        # email sai định dạng
        password="123456",
        password_confirm="123456"
    )

    msg = page.get_input_validation("email")
    assert "email" in msg.lower() or msg != ""


# -----------------------------
# TC10. Test password nhập lại không trùng
# -----------------------------
def test_register_password_mismatch(driver):
    logger.info("[TC10] Test password nhập lại không trùng")
    page = RegisterPage(driver)

    page.open()
    page.register(
        name="Nguyen Van A",
        phone="0912345678",
        birthday="2000-01-10",
        address="Ha Noi",
        email="user2@example.com",
        password="123456",
        password_confirm="999999"       #password_mismatch
    )

    msg = page.get_error_message()
    assert "The password field confirmation does not match" in msg


# -----------------------------
# TC11. Test email đã tồn tại
# -----------------------------
def test_register_duplicate_email(driver):
    logger.info("[TC11] Test email đã tồn tại")
    page = RegisterPage(driver)

    page.open()
    page.register(
        name="Nguyen Van A",
        phone="0912345678",
        birthday="2000-01-10",
        address="Ha Noi",
        email="testuser999@example.com",   # email đã dùng ở test success
        password="123456",
        password_confirm="123456"
    )

    msg = page.get_error_message()
    assert "The email has already been taken" in msg


# -----------------------------
# TC12. Test mật khẩu nhỏ hơn 6 kí tự
# -----------------------------
def test_register_password_less_than_6_chars(driver):
    logger.info("[TC12] Test mật khẩu nhỏ hơn 6 ký tự")
    page = RegisterPage(driver)

    page.open()
    page.register(
        name="Nguyen Van A",
        phone="0912345678",
        birthday="2000-01-10",
        address="Ha Noi",
        email="testpassshort@example.com",
        password="12345",              # < 6 ký tự
        password_confirm="12345"
    )

    msg = page.get_error_message()
    assert "The password field must be at least 6 characters" in msg
