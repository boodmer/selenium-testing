# pages/product_detail_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class ProductDetailPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ================= LOCATORS (XPath) =================
    
    # Locators Thông tin Sản phẩm (Sẽ được định nghĩa linh hoạt trong hàm)
    PRODUCT_TITLE_HEADING = (By.XPATH, "//h1")
    
    # Locators Mua hàng
    QUANTITY_INPUT = (By.XPATH, "//input[@type='number' and @min='1']")
    INCREMENT_BUTTON = (By.XPATH, "//input[@type='number' and @min='1']/following-sibling::button[contains(text(), '+')]")
    DECREMENT_BUTTON = (By.XPATH, "//input[@type='number' and @min='1']/preceding-sibling::button[contains(text(), '-')]")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[normalize-space()='Thêm vào giỏ hàng']")
    STOCK_INFO = (By.XPATH, "//*[contains(text(), 'Số lượng còn lại')]")
    
    # Locators Nội dung
    DESCRIPTION_HEADING = (By.XPATH, "//*[normalize-space()='Mô tả sản phẩm']")
    REVIEW_HEADING = (By.XPATH, "//*[normalize-space()='Đánh giá & Bình luận']")
    
    # Locators Thông báo (Dùng chung)
    SUCCESS_ALERT = (By.XPATH, "//*[contains(text(), 'Thêm vào giỏ hàng thành công') or contains(text(), 'success')]")
    
    
    # ================= ACTIONS & CHECKS =================
    
    def wait_for_page_to_load(self, target_price_numeric, wait_time=30):
        """Chờ trang chi tiết tải hoàn tất (document ready và giá hiển thị)."""
        detail_wait = WebDriverWait(self.driver, wait_time)
        
        # BƯỚC 1: Chờ trạng thái tải trang hoàn tất
        detail_wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
        # BƯỚC 2: Chờ phần tử giá hiển thị (đảm bảo nội dung chính đã load)
        price_xpath_flexible = f"//*[contains(text(), '{target_price_numeric}')]"
        detail_wait.until(
            EC.visibility_of_element_located((By.XPATH, price_xpath_flexible))
        )
        
        # Cuộn về đầu trang (optional, để bắt giá dễ hơn)
        self.driver.execute_script("window.scrollTo(0, 0);") 
    
    
    def check_price_and_discount(self, discounted_price, original_price, discount_percent_text):
        """Kiểm tra sự hiện diện của giá KM, giá gốc và tag giảm giá."""
        try:
            # Giá khuyến mãi (giá mới)
            discounted_price_xpath = f"//*[contains(text(), '{discounted_price}')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, discounted_price_xpath)))
            
            # Giá niêm yết (gạch ngang)
            original_price_xpath = f"//*[contains(text(), '{original_price}')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, original_price_xpath)))
            
            # Tag giảm giá (Ưu tiên tìm bằng text chứa)
            discount_tag_xpath = f"//*[contains(text(), '{discount_percent_text}') or contains(text(), '{discount_percent_text.upper()}') or contains(normalize-space(), '{discount_percent_text}')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, discount_tag_xpath)))
            
            return True
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False

    def check_content_sections(self, scroll_px=1500):
        """Kiểm tra sự hiện diện của Mô tả và Đánh giá (cần cuộn)."""
        self.driver.execute_script(f"window.scrollTo(0, {scroll_px});")
        WebDriverWait(self.driver, 5).until(lambda driver: driver.execute_script(f"return window.scrollY == {scroll_px}"))
        
        try:
            # Tiêu đề Mô tả sản phẩm
            desc_heading = self.driver.find_element(*self.DESCRIPTION_HEADING)
            # Tiêu đề Đánh giá & Bình luận
            review_heading = self.driver.find_element(*self.REVIEW_HEADING)
            
            return desc_heading.is_displayed() and review_heading.is_displayed()
        except NoSuchElementException:
            return False

    def check_purchase_elements(self):
        """Kiểm tra sự hiện diện của input số lượng, nút Thêm vào giỏ và thông tin tồn kho."""
        try:
            qty_input = self.driver.find_element(*self.QUANTITY_INPUT)
            add_btn = self.driver.find_element(*self.ADD_TO_CART_BUTTON)
            stock_info = self.driver.find_element(*self.STOCK_INFO)
            
            return qty_input.is_displayed() and add_btn.is_displayed() and stock_info.is_displayed()
        except NoSuchElementException:
            return False

    def increment_quantity(self):
        """Tăng số lượng sản phẩm."""
        qty_input = self.driver.find_element(*self.QUANTITY_INPUT)
        initial_value = int(qty_input.get_attribute("value"))
        
        increment_button = self.wait.until(
            EC.element_to_be_clickable(self.INCREMENT_BUTTON)
        )
        # Sử dụng JS click để tránh bị che
        self.driver.execute_script("arguments[0].click();", increment_button)
        
        # Chờ 1s và lấy giá trị mới
        import time
        time.sleep(1) 
        new_value = int(self.driver.find_element(*self.QUANTITY_INPUT).get_attribute("value"))
        
        return initial_value, new_value

    def add_to_cart(self):
        """Nhấp vào nút Thêm vào giỏ hàng."""
        add_btn = self.wait.until(
            EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)
        )
        add_btn.click()

    def is_success_alert_displayed(self, wait_time=5):
        """Kiểm tra thông báo Thêm vào giỏ hàng thành công."""
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(self.SUCCESS_ALERT)
            )
            return True
        except TimeoutException:
            return False