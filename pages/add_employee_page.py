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

    def click_employee_menu(self):
        menu = self.driver.find_element(By.XPATH, "//span[text()='Nhân viên']")
        menu.click()


# ================= Employee List Page =================
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EmployeeListPage:
    def __init__(self, driver):
        self.driver = driver

    def click_add_employee(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add_employee_btn"))
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

    def is_employee_displayed(self, name, timeout=10):
        # Nếu có search input
        try:
            search_input = self.driver.find_element(By.XPATH, "//input[@name='keyword']")
            search_input.clear()
            search_input.send_keys(name)
            search_input.submit()
        except:
            pass

        try:
            # Wait employee xuất hiện, dùng contains để tránh lỗi HTML
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//td[contains(., '{name}')]")
                )
            )
            return True
        except:
            return False



# ================= Add Employee Page =================
class AddEmployeePage:
    def __init__(self, driver):
        self.driver = driver

    def enter_name(self, name):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "name"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, name)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_phone(self, phone):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "phone"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, phone)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_position(self, position):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "position"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, position)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def enter_address(self, address):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "address"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", field, address)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)

    def upload_image(self, path):
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "image"))
        )
        field.send_keys(path)

    def click_submit(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Thêm nhân viên')]"))
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", button)

    def is_error_displayed(self, field_id):
        try:
            error = self.driver.find_element(
                By.XPATH,
                f"//input[@id='{field_id}']/following-sibling::small[contains(@class,'text-danger')]"
            )
            return error.is_displayed()
        except:
            return False
