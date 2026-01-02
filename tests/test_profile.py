import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.profile_page import ProfilePage

BASE_URL = "http://127.0.0.1:8000"
PROFILE_URL = f"{BASE_URL}/profile"

TEST_EMAIL = "user@gmail.com"

ORIGINAL_DATA = {
    "name": "Lê Tuấn Anh Gốc",
    "email": TEST_EMAIL,
    "phone": "0987000000",
    "address": "Địa chỉ Gốc ban đầu",
    "day": "1",
    "month": "1",
    "year": "1990"
}


# ================= TC1 =================
def test_01_update_all_fields_successful(logged_in_driver):
    """TC1: Cập nhật đầy đủ thông tin hợp lệ"""
    driver = logged_in_driver
    page = ProfilePage(driver)

    driver.get(PROFILE_URL)
    page.wait.until(EC.presence_of_element_located(page.NAME_INPUT))

    new_name = f"User Test {time.strftime('%M%S')}"

    page.fill_profile(
        name=new_name,
        email=TEST_EMAIL,
        phone="0987111222",
        address="Dia Chi Test Thanh Cong",
        day="15",
        month="5",
        year="2000"
    )
    page.submit()

    assert page.is_success_displayed()

    driver.get(PROFILE_URL)
    assert driver.find_element(*page.NAME_INPUT).get_attribute("value") == new_name
    assert driver.find_element(*page.PHONE_INPUT).get_attribute("value") == "0987111222"


# ================= TC2 =================
def test_02_address_missing_fails(logged_in_driver):
    """TC2: Bỏ trống địa chỉ"""
    driver = logged_in_driver
    page = ProfilePage(driver)

    driver.get(PROFILE_URL)

    page.fill_profile(
        name="Missing Address",
        email=TEST_EMAIL,
        phone="0999999999",
        address="",
        day="1",
        month="1",
        year="1990"
    )
    page.submit()

    assert page.is_error_displayed("address")


# ================= TC3 =================
def test_03_invalid_email_format_fails(logged_in_driver):
    """TC3: Email sai định dạng"""
    driver = logged_in_driver
    page = ProfilePage(driver)

    driver.get(PROFILE_URL)

    email_input = driver.find_element(*page.EMAIL_INPUT)
    if email_input.get_attribute("readonly") or email_input.get_attribute("disabled"):
        pytest.skip("Email readonly/disabled")

    page.fill_profile(
        name="Invalid Email",
        email="invalid-email",
        phone="0987000000",
        address="Test",
        day="1",
        month="1",
        year="1990"
    )
    page.submit()

    assert page.is_error_displayed("email")


# ================= TC4 =================
def test_04_invalid_phone_fails(logged_in_driver):
    """TC4: Số điện thoại không hợp lệ"""
    driver = logged_in_driver
    page = ProfilePage(driver)

    driver.get(PROFILE_URL)

    page.fill_profile(
        name="Invalid Phone",
        email=TEST_EMAIL,
        phone="0900abcxyz",
        address="Test Address",
        day="1",
        month="1",
        year="1990"
    )
    page.submit()

    assert page.is_error_displayed("phone")


# ================= TC5 =================
def test_05_future_birthday_fails(logged_in_driver):
    """TC5: Ngày sinh trong tương lai"""
    driver = logged_in_driver
    page = ProfilePage(driver)

    driver.get(PROFILE_URL)

    future_year = str(time.localtime().tm_year + 1)

    year_select = driver.find_element(*page.YEAR_SELECT)
    values = [o.get_attribute("value") for o in year_select.find_elements(By.TAG_NAME, "option")]

    if future_year not in values:
        pytest.skip("Dropdown đã lọc năm tương lai")

    page.fill_profile(
        name="Future Birthday",
        email=TEST_EMAIL,
        phone="0987000000",
        address="Test Address",
        day="1",
        month="1",
        year=future_year
    )
    page.submit()

    assert page.is_error_displayed()
