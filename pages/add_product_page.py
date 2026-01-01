from time import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time

# ================= Dashboard Page =================
class DashboardPage:
    def __init__(self, driver):
        self.driver = driver

    def click_product_menu(self):
        menu = self.driver.find_element(By.XPATH, "//span[text()='Sản phẩm']")
        menu.click()


# ================= Product List Page =================
class ProductListPage:
    def __init__(self, driver):
        self.driver = driver

    def click_add_product(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Thêm sản phẩm')]"))
        )
        
        # Use JavaScript click directly
        self.driver.execute_script("arguments[0].click();", add_btn)
        time.sleep(1)
        
        # Wait for page to navigate and load completely (it's a link redirect)
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # Then wait for the form to be ready
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "name"))
        )

    def is_product_displayed(self, name):
        # Nếu có search input, dùng filter nhanh
        try:
            search_input = self.driver.find_element(By.XPATH, "//input[@name='keyword']")
            search_input.clear()
            search_input.send_keys(name)
            search_input.submit()  # submit form
            time.sleep(1)  # đợi bảng load
        except:
            pass  # nếu không có search input, fallback check theo tất cả trang

        # Kiểm tra sản phẩm trong table
        rows = self.driver.find_elements(By.XPATH, f"//td//p[text()='{name}']")
        return len(rows) > 0



# ================= Add Product Page =================
class AddProductPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_product_name(self, name):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "name"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, name)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_category(self, category):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "category"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, category)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_original_price(self, original_price):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "original_price"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, original_price)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_price(self, price):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "price"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, price)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_stock(self, stock):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "stock"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, stock)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_brand(self, brand):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "brand"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, brand)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_sku(self, sku):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "sku"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, sku)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_discount(self, discount):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "discount"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, discount)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_description(self, description):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "description"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, description)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def upload_image(self, path):
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "image"))
        )
        field.send_keys(path)

    def click_submit(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Thêm sản phẩm')]"))
        )
        # Scroll vào view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", button)
        
    def is_error_displayed(self, field_id):
        try:
            error = self.driver.find_element(By.XPATH, f"//input[@id='{field_id}']/following-sibling::small[contains(@class,'text-danger')]")
            return error.is_displayed()
        except:
            return False

    def get_flash_message(self):
        try:
            flash_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".fl-message"))
            )
            return flash_element.text
        except:
            return None