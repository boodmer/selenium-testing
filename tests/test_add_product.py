import time
import logging
from pages.add_product_page import DashboardPage, ProductListPage, AddProductPage

logger = logging.getLogger(__name__)

def test_add_product_success(logged_in_admin_driver):
    driver = logged_in_admin_driver

    # ================= Mở dashboard và đi tới trang thêm sản phẩm =================
    dashboard = DashboardPage(driver)
    dashboard.click_product_menu()

    product_page = ProductListPage(driver)
    product_page.click_add_product()

    page = AddProductPage(driver)

    # ================= Nhập thông tin sản phẩm =================
    product_name = "Sản phẩm xe đạp tự động " + str(int(time.time()))
    page.enter_product_name(product_name)
    page.enter_category("Xe đạp")
    page.enter_original_price("200000")
    page.enter_discount("20")  # tự động cập nhật giá bán
    page.enter_stock("15")
    page.enter_brand("GRANT")
    page.enter_sku("SKU" + str(int(time.time())))
    page.enter_description("Sản phẩm test tự động bằng Selenium")
    page.upload_image("E:/test/bike.jpg")

    # ================= Submit form =================
    page.click_submit()

    # Debug URL
    print("[DEBUG] After submit:", driver.current_url)

    # ================= Check sản phẩm xuất hiện trên danh sách =================
    product_list = ProductListPage(driver)
    assert product_list.is_product_displayed(product_name)
    logger.info(f"[PASSED] Đã thêm sản phẩm thành công: {product_name}")

# ================= Test tên sản phẩm rỗng =================   
def test_add_product_missing_name(logged_in_admin_driver):
    driver = logged_in_admin_driver

    dashboard = DashboardPage(driver)
    dashboard.click_product_menu()

    product_page = ProductListPage(driver)
    product_page.click_add_product()

    page = AddProductPage(driver)

    # Bỏ trống tên sản phẩm
    page.enter_product_name("")  
    page.enter_category("Giày thể thao")
    page.enter_original_price("100000")
    page.enter_discount("10")
    page.enter_stock("5")
    page.enter_brand("Nike")
    page.enter_sku("SKU_EMPTY_" + str(int(time.time())))
    
    page.click_submit()

    # Kiểm tra hiển thị lỗi
    assert page.is_error_displayed("name")


 # ================= Test giá bán > giá gốc =================   
def test_add_product_price_gt_original(logged_in_admin_driver):
    driver = logged_in_admin_driver
    dashboard = DashboardPage(driver)
    dashboard.click_product_menu()
    ProductListPage(driver).click_add_product()
    page = AddProductPage(driver)

    page.enter_product_name("Test Giá bán > Giá gốc")
    page.enter_category("Giày thể thao")
    page.enter_original_price("100000")
    page.enter_discount("0")
    page.enter_price("150000")  # > original_price
    page.enter_stock("5")
    page.enter_brand("Nike")
    page.enter_sku("SKU_PRICE_" + str(int(time.time())))
    page.click_submit()

    assert page.is_error_displayed("price")

    # ================= Test giảm giá > 100% =================
def test_add_product_discount_gt_100(logged_in_admin_driver):
    driver = logged_in_admin_driver
    dashboard = DashboardPage(driver)
    dashboard.click_product_menu()
    ProductListPage(driver).click_add_product()
    page = AddProductPage(driver)

    page.enter_product_name("Test giảm giá > 100")
    page.enter_category("Giày thể thao")
    page.enter_original_price("200000")
    page.enter_discount("150")  # > 100%
    page.enter_stock("5")
    page.enter_brand("Nike")
    page.enter_sku("SKU_DISCOUNT_" + str(int(time.time())))
    page.click_submit()

    assert page.is_error_displayed("discount")

    # ================= Test stock âm =================
def test_add_product_stock_negative(logged_in_admin_driver):
    driver = logged_in_admin_driver
    dashboard = DashboardPage(driver)
    dashboard.click_product_menu()
    ProductListPage(driver).click_add_product()
    page = AddProductPage(driver)

    page.enter_product_name("Test stock âm")
    page.enter_category("Xe đạp")
    page.enter_original_price("100000")
    page.enter_discount("10")
    page.enter_stock("-5")  # âm
    page.enter_brand("GRANT")
    page.enter_sku("SKU_STOCK_" + str(int(time.time())))
    page.click_submit()

    assert page.is_error_displayed("stock")