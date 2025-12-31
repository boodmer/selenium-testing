import logging
from pages.maintenance_request_page import MaintenanceRequestPage

# Khởi tạo logger cho file này
logger = logging.getLogger(__name__)

BASE_URL = "http://127.0.0.1:8000"
MAINTENANCE_URL = f"{BASE_URL}/maintenance"


# ======================================
# TC01: Gửi yêu cầu bảo trì thành công
# ======================================
def test_01_create_maintenance_success(logged_in_driver):
    logger.info("[TC01] Gửi yêu cầu bảo trì thành công")

    driver = logged_in_driver
    driver.get(MAINTENANCE_URL)
    page = MaintenanceRequestPage(driver)

    page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="Quận 1, TP.HCM",
        issue_description="Xe kêu khi đạp, đề sau không ăn"
    )
    page.submit()

    assert page.is_success_displayed()


# ======================================
# TC02: Thiếu tên khách hàng
# ======================================
def test_02_missing_customer_name_fails(logged_in_driver):
    logger.info("[TC02] Thiếu tên khách hàng")

    driver = logged_in_driver
    driver.get(MAINTENANCE_URL)
    page = MaintenanceRequestPage(driver)

    page.fill_maintenance_request(
        customer_name="",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="TP.HCM",
        issue_description="Xe rung"
    )
    page.submit()

    assert page.is_error_displayed("customer_name")


# ======================================
# TC03: Email không hợp lệ
# ======================================
def test_03_invalid_email_fails(logged_in_driver):
    logger.info("[TC03] Email không hợp lệ")

    driver = logged_in_driver
    driver.get(MAINTENANCE_URL)
    page = MaintenanceRequestPage(driver)

    page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="invalid-email",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="TP.HCM",
        issue_description="Phanh yếu"
    )
    page.submit()

    assert page.is_error_displayed("email")


# ======================================
# TC04: Email để trống (nullable – hợp lệ)
# ======================================
def test_04_email_nullable_success(logged_in_driver):
    logger.info("[TC04] Email để trống (nullable)")

    driver = logged_in_driver
    driver.get(MAINTENANCE_URL)
    page = MaintenanceRequestPage(driver)

    page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="TP.HCM",
        issue_description="Xe kêu"
    )
    page.submit()

    assert page.is_success_displayed()


# ======================================
# TC05: Thiếu mã sản phẩm
# ======================================
def test_05_missing_product_sku_fails(logged_in_driver):
    logger.info("[TC05] Thiếu mã sản phẩm")

    driver = logged_in_driver
    driver.get(MAINTENANCE_URL)
    page = MaintenanceRequestPage(driver)

    page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="",
        preferred_date="2026-01-25",
        address="TP.HCM",
        issue_description="Xích tuột"
    )
    page.submit()

    assert page.is_error_displayed("product_sku")


# ======================================
# TC06: Thiếu ngày bảo trì
# ======================================
def test_06_missing_preferred_date_fails(logged_in_driver):
    logger.info("[TC06] Thiếu ngày bảo trì")

    driver = logged_in_driver
    driver.get(MAINTENANCE_URL)
    page = MaintenanceRequestPage(driver)

    page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="6918068022060",
        preferred_date="",
        address="TP.HCM",
        issue_description="Phanh trước yếu"
    )
    page.submit()

    assert page.is_error_displayed("preferred_date")


# ======================================
# TC07: Thiếu mô tả vấn đề
# ======================================
def test_07_missing_issue_description_fails(logged_in_driver):
    logger.info("[TC07] Thiếu mô tả vấn đề")

    driver = logged_in_driver
    driver.get(MAINTENANCE_URL)
    page = MaintenanceRequestPage(driver)

    page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="TP.HCM",
        issue_description=""
    )
    page.submit()

    assert page.is_error_displayed("issue_description")


# ======================================
# TC08: Thiếu địa chỉ
# ======================================
def test_08_missing_address_fails(logged_in_driver):
    logger.info("[TC08] Thiếu địa chỉ")

    driver = logged_in_driver
    driver.get(MAINTENANCE_URL)
    page = MaintenanceRequestPage(driver)

    page.fill_maintenance_request(
        customer_name="Nguyễn Văn A",
        phone="0912345678",
        email="a@gmail.com",
        product_sku="6918068022060",
        preferred_date="2026-01-25",
        address="",
        issue_description="Xe rung mạnh"
    )
    page.submit()

    assert page.is_error_displayed("address")
