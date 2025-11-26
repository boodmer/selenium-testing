from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Thêm nhân viên')]"))
        )
        add_btn.click()

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
        self.driver.find_element(By.ID, "name").send_keys(name)

    def enter_phone(self, phone):
        self.driver.find_element(By.ID, "phone").send_keys(phone)

    def enter_position(self, position):
        self.driver.find_element(By.ID, "position").send_keys(position)

    def enter_address(self, address):
        self.driver.find_element(By.ID, "address").send_keys(address)

    def upload_image(self, path):
        self.driver.find_element(By.ID, "image").send_keys(path)

    def click_submit(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Thêm nhân viên')]"))
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        ActionChains(self.driver).move_to_element(button).click().perform()

    def is_error_displayed(self, field_id):
        try:
            error = self.driver.find_element(
                By.XPATH,
                f"//input[@id='{field_id}']/following-sibling::small[contains(@class,'text-danger')]"
            )
            return error.is_displayed()
        except:
            return False
