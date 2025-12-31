import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Page Object
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


# ================= FIXTURE =================
@pytest.fixture
def product_detail_page(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, WAIT_TIME)

    # Điều hướng tới trang chủ
    driver.get(HOME_URL)
    time.sleep(1)

    # Cuộn để tìm sản phẩm
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

    # Khởi tạo Page Object
    page = ProductDetailPage(driver)

    # Chờ trang chi tiết load xong
    try:
        page.wait_for_page_to_load(PRODUCT_DATA["discounted_price"])
    except TimeoutException:
        pytest.fail("🛑 Trang chi tiết sản phẩm load quá lâu")

    return page


# ================= TEST CASES =================

def test_01_product_price_and_discount(product_detail_page):
    """TC1: Kiểm tra hiển thị giá & giảm giá"""
    assert product_detail_page.check_price_and_discount(
        PRODUCT_DATA["discounted_price"],
        PRODUCT_DATA["original_price"],
        PRODUCT_DATA["discount_tag"]
    ), "TC1 FAILED: Giá hoặc tag giảm giá không hiển thị đúng"


def test_02_product_description_and_reviews_visible(product_detail_page):
    """TC2: Kiểm tra mô tả và đánh giá"""
    assert product_detail_page.check_content_sections(scroll_px=1500), (
        "TC2 FAILED: Không thấy Mô tả hoặc Đánh giá"
    )

    # Cuộn về đầu trang
    product_detail_page.driver.execute_script("window.scrollTo(0, 0);")


def test_03_add_to_cart_elements_exist(product_detail_page):
    """TC3: Kiểm tra phần tử mua hàng"""
    product_detail_page.driver.execute_script("window.scrollTo(0, 700);")
    time.sleep(1)

    assert product_detail_page.check_purchase_elements(), (
        "TC3 FAILED: Thiếu input số lượng hoặc nút Thêm vào giỏ"
    )


def test_04_quantity_increment(product_detail_page):
    """TC4: Kiểm tra tăng số lượng"""
    initial_value, new_value = product_detail_page.increment_quantity()

    assert new_value == initial_value + 1, (
        f"TC4 FAILED: Số lượng không tăng (ban đầu {initial_value}, sau {new_value})"
    )
