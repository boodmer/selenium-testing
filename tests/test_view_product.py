import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.view_product_page import ProductDetailPage

# ================= CONFIG =================
BASE_URL = "http://127.0.0.1:8000"
HOME_URL = f"{BASE_URL}/home"
WAIT_TIME = 15

PRODUCT_DATA = {
    "id": "11",
    "title": "Xe Đạp Trẻ Em YOUTH STITCH Rainbow 2 - Bánh 20 Inches",
    "discounted_price": "2.371.500",
    "original_price": "2.790.000",
    "discount_tag": "Giảm 15%",
}
# =========================================


# ========== HELPER ==========
def go_to_product_detail(driver):
    wait = WebDriverWait(driver, WAIT_TIME)

    driver.get(HOME_URL)
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(2)

    product_link_xpath = f"//a[contains(@href, '/details/{PRODUCT_DATA['id']}')]"

    try:
        product_link = wait.until(
            EC.presence_of_element_located((By.XPATH, product_link_xpath))
        )
        driver.execute_script("arguments[0].click();", product_link)
        wait.until(EC.url_contains(f"/details/{PRODUCT_DATA['id']}"))
    except TimeoutException:
        pytest.fail(f"🛑 Không tìm thấy link sản phẩm ID {PRODUCT_DATA['id']}")

    page = ProductDetailPage(driver)

    try:
        page.wait_for_page_to_load(PRODUCT_DATA["discounted_price"])
    except TimeoutException:
        pytest.fail("🛑 Trang chi tiết sản phẩm load quá lâu")

    return page


# ================= TEST CASES =================

# ================= TC1 =================
def test_01_product_price_and_discount(logged_in_driver):
    """TC1: Kiểm tra hiển thị giá & giảm giá"""
    driver = logged_in_driver
    page = go_to_product_detail(driver)

    assert page.check_price_and_discount(
        PRODUCT_DATA["discounted_price"],
        PRODUCT_DATA["original_price"],
        PRODUCT_DATA["discount_tag"]
    ), "TC1 FAILED: Giá hoặc tag giảm giá không hiển thị đúng"


# ================= TC2 =================
def test_02_product_description_and_reviews_visible(logged_in_driver):
    """TC2: Kiểm tra mô tả và đánh giá"""
    driver = logged_in_driver
    page = go_to_product_detail(driver)

    assert page.check_content_sections(scroll_px=1500), (
        "TC2 FAILED: Không thấy Mô tả hoặc Đánh giá"
    )

    driver.execute_script("window.scrollTo(0, 0);")


# ================= TC3 =================
def test_03_add_to_cart_elements_exist(logged_in_driver):
    """TC3: Kiểm tra phần tử mua hàng"""
    driver = logged_in_driver
    page = go_to_product_detail(driver)

    driver.execute_script("window.scrollTo(0, 700);")
    time.sleep(1)

    assert page.check_purchase_elements(), (
        "TC3 FAILED: Thiếu input số lượng hoặc nút Thêm vào giỏ"
    )


# ================= TC4 =================
def test_04_quantity_increment(logged_in_driver):
    """TC4: Kiểm tra tăng số lượng"""
    driver = logged_in_driver
    page = go_to_product_detail(driver)

    initial_value, new_value = page.increment_quantity()

    assert new_value == initial_value + 1, (
        f"TC4 FAILED: Số lượng không tăng (ban đầu {initial_value}, sau {new_value})"
    )
