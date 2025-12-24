# tests/test_product_detail.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Import Page Object Model
from pages.view_product_page import ProductDetailPage

# ================= CẤU HÌNH =================
CHROME_DRIVER_PATH = r'C:\Users\P50\Desktop\kthu\chromedriver.exe' 
BASE_URL = 'http://127.0.0.1:8000' 
LOGIN_URL = f"{BASE_URL}/login" 
TEST_EMAIL = 'minhchi@gmail.com' 
TEST_PASSWORD = '12345678' 
DEFAULT_WAIT_TIME = 15 

# --- DỮ LIỆU SẢN PHẨM MỤC TIÊU ---
PRODUCT_DATA = {
    "id": '11', # ID của sản phẩm đang test (Xe Đạp Trẻ Em YOUTH STITCH)
    "title": "Xe Đạp Trẻ Em YOUTH STITCH Rainbow 2 - Bánh 20 Inches", 
    "discounted_price": '2.371.500', 
    "original_price": '2.790.000', 
    "discount_tag": 'Giảm 15%', # Hoặc '15%'
}
# ============================================

def _automatic_login(driver, wait):
    """Thực hiện quy trình đăng nhập tự động (Sử dụng lại logic từ code gốc)."""
    driver.get(LOGIN_URL)
    print("Bắt đầu đăng nhập...")
    
    EMAIL_INPUT = (By.XPATH, "//input[@type='email' or @name='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password' or @name='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'ĐĂNG NHẬP') or @type='submit']")
    
    try:
        email_field = wait.until(EC.presence_of_element_located(EMAIL_INPUT))
        password_field = driver.find_element(*PASSWORD_INPUT)
        login_button = driver.find_element(*LOGIN_BUTTON)
        
        email_field.send_keys(TEST_EMAIL) 
        password_field.send_keys(TEST_PASSWORD)
        login_button.click()
        
        wait.until(EC.url_contains('/home'))
        print("✅ Đăng nhập tự động thành công.")
        return True
    except Exception as e:
        pytest.fail(f"🛑 LỖI ĐĂNG NHẬP TỰ ĐỘNG: {e}")


def _navigate_to_detail_page(driver, wait, product_id):
    """Điều hướng đến trang chi tiết sản phẩm."""
    product_link_xpath = f"//a[contains(@href, '/details/{product_id}')]" 
    driver.get(f"{BASE_URL}/home")
    time.sleep(1)
    
    # Cuộn xuống để tìm sản phẩm trên trang chủ (Giả định nó nằm ở 1000px)
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(2) 
    
    try:
        product_link_element = wait.until( 
            EC.presence_of_element_located((By.XPATH, product_link_xpath))
        )
        
        driver.execute_script("arguments[0].click();", product_link_element)
        wait.until(EC.url_contains(f'/details/{product_id}'))
        print(f"✅ Đã điều hướng thành công đến trang chi tiết sản phẩm ID {product_id}.")
        return True
    except TimeoutException:
        pytest.fail(f"🛑 Không thể tìm thấy hoặc nhấp vào LINK SẢN PHẨM ID {product_id} trên trang chủ.")


@pytest.fixture(scope="module")
def product_detail_page():
    """Fixture khởi tạo WebDriver, đăng nhập và điều hướng đến trang chi tiết sản phẩm."""
    # Khởi tạo WebDriver
    service = Service(CHROME_DRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
    chrome_options.add_argument("--start-maximized")
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except WebDriverException as e:
        pytest.fail(f"🛑 Lỗi Khởi tạo WebDriver: {e}")
        
    wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)
    
    # Đăng nhập
    _automatic_login(driver, wait)
    
    # Điều hướng đến trang chi tiết sản phẩm
    _navigate_to_detail_page(driver, wait, PRODUCT_DATA["id"])
    
    # Khởi tạo Page Object Model
    page = ProductDetailPage(driver)
    
    # Chờ trang load xong (đã chuyển sang POM)
    try:
        print("Đang chờ trang chi tiết tải hoàn tất...")
        page.wait_for_page_to_load(PRODUCT_DATA["discounted_price"])
        print("Trang chi tiết đã tải xong.")
    except TimeoutException:
        pytest.fail("🛑 LỖI TIMEOUT: Trang chi tiết không tải xong.")
        
    yield page
    
    # Teardown
    print("\n[Teardown] Đóng WebDriver.")
    driver.quit()


# ================= TEST CASES =================

## 1. Kiểm tra giá và thông tin giảm giá
def test_01_product_price_and_discount(product_detail_page):
    """TC1: Kiểm tra hiển thị đúng giá niêm yết, giá khuyến mãi và phần trăm giảm giá."""
    is_displayed = product_detail_page.check_price_and_discount(
        PRODUCT_DATA["discounted_price"],
        PRODUCT_DATA["original_price"],
        PRODUCT_DATA["discount_tag"]
    )
    assert is_displayed, "TC1 FAILED: Không tìm thấy Giá khuyến mãi, Giá niêm yết hoặc Tag giảm giá."
    print("✅ TC1 PASSED: Giá niêm yết, giá khuyến mãi và tag giảm giá hiển thị đúng.")


## 2. Kiểm tra sự hiện diện của mô tả và đánh giá
def test_02_product_description_and_reviews_visible(product_detail_page):
    """TC2: Kiểm tra phần Mô tả Sản phẩm và Đánh giá/Bình luận phải có trên trang."""
    # Cần cuộn xuống để tìm thấy
    is_displayed = product_detail_page.check_content_sections(scroll_px=1500)
    
    assert is_displayed, "TC2 FAILED: Không tìm thấy tiêu đề 'Mô tả sản phẩm' hoặc 'Đánh giá & Bình luận'."
    print("✅ TC2 PASSED: Các phần Mô tả Sản phẩm và Đánh giá/Bình luận hiển thị thành công.")
    
    # Cuộn về 0 để tránh ảnh hưởng TC tiếp theo
    product_detail_page.driver.execute_script("window.scrollTo(0, 0);") 


## 3. Kiểm tra các phần tử mua hàng
def test_03_add_to_cart_elements_exist(product_detail_page):
    """TC3: Kiểm tra các phần tử cần thiết cho việc mua hàng (số lượng, nút Thêm vào giỏ) phải tồn tại."""
    # Cần cuộn xuống một chút (700px)
    product_detail_page.driver.execute_script("window.scrollTo(0, 700);")
    time.sleep(1)
    
    is_displayed = product_detail_page.check_purchase_elements()
    
    assert is_displayed, "TC3 FAILED: Không tìm thấy phần tử mua hàng (input số lượng, nút Thêm vào giỏ hoặc thông tin tồn kho)."
    print("✅ TC3 PASSED: Các phần tử mua hàng cơ bản hiển thị thành công.")


## 4. Kiểm tra Tăng số lượng sản phẩm
def test_04_quantity_increment(product_detail_page):
    """TC4: Kiểm tra nút tăng số lượng hoạt động chính xác."""
    try:
        initial_value, new_value = product_detail_page.increment_quantity()
        
        assert new_value == initial_value + 1, f"TC4 FAILED: Số lượng không tăng. Ban đầu: {initial_value}, Thực tế: {new_value}"
        print("✅ TC4 PASSED: Tăng số lượng sản phẩm thành công.")
    except Exception as e:
        pytest.fail(f"TC4 FAILED: Lỗi khi tương tác nút tăng số lượng. Chi tiết: {e}")

