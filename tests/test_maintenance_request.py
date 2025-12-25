import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.maintenance_request_page import MaintenanceRequestPage


# ================= CONFIG =================
BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/login"
MAINTENANCE_URL = f"{BASE_URL}/maintenance"
WAIT_TIME = 20

TEST_EMAIL = "minhchi@gmail.com"
TEST_PASSWORD = "password"
# =========================================


# ================= HELPER =================
def login(driver, wait):
    driver.get(LOGIN_URL)

    EMAIL = (By.XPATH, "//input[@type='email' or @name='email']")
    PASSWORD = (By.XPATH, "//input[@type='password' or @name='password']")
    LOGIN_BTN = (By.XPATH, "//button[@type='submit' or contains(text(),'ĐĂNG NHẬP') or contains(text(),'Login')]")

    wait.until(EC.presence_of_element_located(EMAIL)).send_keys(TEST_EMAIL)
    driver.find_element(*PASSWORD).send_keys(TEST_PASSWORD)
    driver.find_element(*LOGIN_BTN).click()

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1 | //input[contains(@placeholder,'Tìm kiếm')]")
        )
    )
    time.sleep(1)


# ================= FIXTURE =================
@pytest.fixture
def maintenance_page(driver):
    wait = WebDriverWait(driver, WAIT_TIME)
    login(driver, wait)

    driver.get(MAINTENANCE_URL)
    page = MaintenanceRequestPage(driver)

    wait.until(EC.presence_of_element_located(page.CUSTOMER_NAME_INPUT))
    return page


# ================= TEST CASES =================

# TC01 – Gửi yêu cầu bảo trì thành công
def test_01_create_maintenance_success(maintenance_page):
    maintenance_page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="Quận 1, TP.HCM",
        issue_description="Xe kêu khi đạp, đề sau không ăn"
    )
    maintenance_page.submit()

    assert maintenance_page.is_success_displayed()


# TC02 – Thiếu tên khách hàng
def test_02_missing_customer_name_fails(maintenance_page):
    maintenance_page.fill_maintenance_request(
        customer_name="",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="TP.HCM",
        issue_description="Xe rung"
    )
    maintenance_page.submit()

    assert maintenance_page.is_error_displayed("customer_name")


# TC03 – Email không hợp lệ
def test_03_invalid_email_fails(maintenance_page):
    maintenance_page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="invalid-email",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="TP.HCM",
        issue_description="Phanh yếu"
    )
    maintenance_page.submit()

    assert maintenance_page.is_error_displayed("email")


# TC04 – Email để trống (nullable – hợp lệ)
def test_04_email_nullable_success(maintenance_page):
    maintenance_page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="TP.HCM",
        issue_description="Xe kêu"
    )
    maintenance_page.submit()

    assert maintenance_page.is_success_displayed()


# TC05 – Thiếu mã sản phẩm
def test_05_missing_product_sku_fails(maintenance_page):
    maintenance_page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="",
        preferred_date="2026-01-25",
        address="TP.HCM",
        issue_description="Xích tuột"
    )
    maintenance_page.submit()

    assert maintenance_page.is_error_displayed("product_sku")


# TC06 – Ngày bảo trì sai định dạng
def test_06_missing_preferred_date_fails(maintenance_page):
    maintenance_page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="6918068022060",
        preferred_date="",   # để trống
        address="TP.HCM",
        issue_description="Phanh trước yếu"
    )
    maintenance_page.submit()

    assert maintenance_page.is_error_displayed("preferred_date")


# TC07 – Thiếu mô tả vấn đề
def test_07_missing_issue_description_fails(maintenance_page):
    maintenance_page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="TP.HCM",
        issue_description=""
    )
    maintenance_page.submit()

    assert maintenance_page.is_error_displayed("issue_description")


# TC08 – Thiếu địa chỉ
def test_08_missing_address_fails(maintenance_page):
    maintenance_page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="",
        issue_description="Xe rung mạnh"
    )
    maintenance_page.submit()

    assert maintenance_page.is_error_displayed("address")
