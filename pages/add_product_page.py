from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
        add_btn.click()

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
        self.driver.find_element(By.ID, "name").send_keys(name)

    def enter_category(self, category):
        self.driver.find_element(By.ID, "category").send_keys(category)

    def enter_original_price(self, original_price):
        self.driver.find_element(By.ID, "original_price").send_keys(original_price)

    def enter_price(self, price):
        self.driver.find_element(By.ID, "price").send_keys(price)

    def enter_stock(self, stock):
        self.driver.find_element(By.ID, "stock").send_keys(stock)

    def enter_brand(self, brand):
        self.driver.find_element(By.ID, "brand").send_keys(brand)

    def enter_sku(self, sku):
        self.driver.find_element(By.ID, "sku").send_keys(sku)

    def enter_discount(self, discount):
        self.driver.find_element(By.ID, "discount").send_keys(discount)

    def enter_description(self, description):
        self.driver.find_element(By.ID, "description").send_keys(description)

    def upload_image(self, path):
        self.driver.find_element(By.ID, "image").send_keys(path)

    def click_submit(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Thêm sản phẩm')]"))
        )
        # Scroll vào view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        # Click bằng ActionChains
        ActionChains(self.driver).move_to_element(button).click().perform()
        
    def is_error_displayed(self, field_id):
        try:
            error = self.driver.find_element(By.XPATH, f"//input[@id='{field_id}']/following-sibling::small[contains(@class,'text-danger')]")
            return error.is_displayed()
        except:
            return False