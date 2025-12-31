import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.profile_page import ProfilePage

# ================= CONFIG =================
BASE_URL = "http://127.0.0.1:8000"
PROFILE_URL = f"{BASE_URL}/profile"
WAIT_TIME = 20

TEST_EMAIL = "minhchi@gmail.com"

ORIGINAL_DATA = {
    "name": "Lê Tuấn Anh Gốc",
    "email": TEST_EMAIL,
    "phone": "0987000000",
    "address": "Địa chỉ Gốc ban đầu",
    "day": "1",
    "month": "1",
    "year": "1990"
}
# =========================================


# ================= FIXTURE =================
@pytest.fixture
def profile_page(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, WAIT_TIME)

    driver.get(PROFILE_URL)
    profile = ProfilePage(driver)

    # Restore data gốc trước mỗi test
    wait.until(EC.presence_of_element_located(profile.NAME_INPUT))
    profile.fill_profile(**ORIGINAL_DATA)
    profile.submit()

    driver.get(PROFILE_URL)
    wait.until(EC.presence_of_element_located(profile.NAME_INPUT))

    return profile


# ================= TEST CASES =================

def test_01_update_all_fields_successful(profile_page):
    driver = profile_page.driver
    new_name = f"User Test {time.strftime('%M%S')}"

    profile_page.fill_profile(
        name=new_name,
        email=TEST_EMAIL,
        phone="0987111222",
        address="Dia Chi Test Thanh Cong",
        day="15",
        month="5",
        year="2000"
    )
    profile_page.submit()

    assert profile_page.is_success_displayed()

    driver.get(PROFILE_URL)
    profile_page.wait.until(EC.presence_of_element_located(profile_page.NAME_INPUT))

    assert driver.find_element(*profile_page.NAME_INPUT).get_attribute("value") == new_name
    assert driver.find_element(*profile_page.PHONE_INPUT).get_attribute("value") == "0987111222"


def test_02_address_missing_fails(profile_page):
    profile_page.fill_profile(
        name="Test Missing Address",
        email=TEST_EMAIL,
        phone="0999999999",
        address="",
        day=ORIGINAL_DATA["day"],
        month=ORIGINAL_DATA["month"],
        year=ORIGINAL_DATA["year"]
    )
    profile_page.submit()

    assert profile_page.is_error_displayed("address")


def test_03_invalid_email_format_fails(profile_page):
    email_input = profile_page.driver.find_element(*profile_page.EMAIL_INPUT)
    if email_input.get_attribute("readonly") or email_input.get_attribute("disabled"):
        pytest.skip("Email readonly")

    profile_page.fill_profile(
        name="Invalid Email",
        email="invalid-email",
        phone=ORIGINAL_DATA["phone"],
        address=ORIGINAL_DATA["address"],
        day=ORIGINAL_DATA["day"],
        month=ORIGINAL_DATA["month"],
        year=ORIGINAL_DATA["year"]
    )
    profile_page.submit()

    assert profile_page.is_error_displayed("email")


def test_04_invalid_phone_fails(profile_page):
    profile_page.fill_profile(
        name="Invalid Phone",
        email=TEST_EMAIL,
        phone="0900abcxyz",
        address=ORIGINAL_DATA["address"],
        day=ORIGINAL_DATA["day"],
        month=ORIGINAL_DATA["month"],
        year=ORIGINAL_DATA["year"]
    )
    profile_page.submit()

    assert profile_page.is_error_displayed("phone")


def test_05_future_birthday_fails(profile_page):
    future_year = str(time.localtime().tm_year + 1)

    year_select = profile_page.driver.find_element(*profile_page.YEAR_SELECT)
    values = [o.get_attribute("value") for o in year_select.find_elements(By.TAG_NAME, "option")]

    if future_year not in values:
        pytest.skip("Dropdown đã lọc năm tương lai")

    profile_page.fill_profile(
        name="Future Birthday",
        email=TEST_EMAIL,
        phone=ORIGINAL_DATA["phone"],
        address=ORIGINAL_DATA["address"],
        day="1",
        month="1",
        year=future_year
    )
    profile_page.submit()

    assert profile_page.is_error_displayed()
