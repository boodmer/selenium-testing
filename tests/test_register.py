from matplotlib import testing
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from pages.register_page import RegisterPage


@pytest.fixture
def driver():
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.wait = WebDriverWait(driver, 10)
    yield driver
    driver.quit()


# -----------------------------
# 1. Test đăng ký thành công
# -----------------------------
def test_register_success(driver):
    page = RegisterPage(driver)

    page.open()
    page.register(
        name="Nguyen Van A",
        phone="0912345678",
        birthday="12/11/2023",
        address="Ha Noi",
        email="testuser99999@example.com",
        password="123456",
        password_confirm="123456"
    )

    msg = page.get_flash_message()
    assert "Đăng ký tài khoản thành công" in msg


# # -----------------------------
# # 2. Test bỏ trống một trường bắt buộc
# # -----------------------------
# def test_register_missing_name(driver):
#     page = RegisterPage(driver)

#     page.open()

#     # bỏ trống name
#     page.register(
#         name="",
#         phone="0912345678",
#         birthday="2000-01-10",
#         address="Ha Noi",
#         email="user1@example.com",
#         password="123456",
#         password_confirm="123456"
#     )

#     msg = page.get_input_validation("name")
#     assert msg != ""


# # -----------------------------
# # 3. Test email sai định dạng
# # -----------------------------
# def test_register_invalid_email_format(driver):
#     page = RegisterPage(driver)

#     page.open()
#     page.register(
#         name="Nguyen Van A",
#         phone="0912345678",
#         birthday="2000-01-10",
#         address="Ha Noi",
#         email="abc123",        # email sai định dạng
#         password="123456",
#         password_confirm="123456"
#     )

#     msg = page.get_input_validation("email")
#     assert "email" in msg.lower() or msg != ""


# # -----------------------------
# # 4. Test password nhập lại không trùng
# # -----------------------------
# def test_register_password_mismatch(driver):
#     page = RegisterPage(driver)

#     page.open()
#     page.register(
#         name="Nguyen Van A",
#         phone="0912345678",
#         birthday="2000-01-10",
#         address="Ha Noi",
#         email="user2@example.com",
#         password="123456",
#         password_confirm="999999"
#     )

#     msg = page.get_error_message()
#     assert "không khớp" in msg.lower() or "mismatch" in msg.lower()


# # -----------------------------
# # 5. Test email đã tồn tại
# # -----------------------------
# def test_register_duplicate_email(driver):
#     page = RegisterPage(driver)

#     page.open()
#     page.register(
#         name="Nguyen Van A",
#         phone="0912345678",
#         birthday="2000-01-10",
#         address="Ha Noi",
#         email="testuser999@example.com",   # email đã dùng ở test trước
#         password="123456",
#         password_confirm="123456"
#     )

#     msg = page.get_error_message()
#     assert "Email đã tồn tại" in msg or "exists" in msg.lower()
