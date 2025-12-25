from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ForgotPasswordPage:

    def __init__(self, driver, base_url="http://127.0.0.1:8000"):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    # Mở trang quên mật khẩu
    def open(self):
        self.driver.get(self.base_url + "/forgot-password")

    # Nhập email
    def enter_email(self, email):
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys(email)

    # Nhập số điện thoại
    def enter_phone(self, phone):
        self.driver.find_element(By.ID, "phone").clear()
        self.driver.find_element(By.ID, "phone").send_keys(phone)

    # Submit form
    def submit(self):
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        submit_button.click()

    # Thao tác gộp
    def submit_forgot_password(self, email, phone):
        self.enter_email(email)
        self.enter_phone(phone)
        self.submit()

    # Lấy message lỗi backend (Email hoặc SĐT sai)
    def get_backend_error(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
        ).text

    # Lấy validation message HTML5
    def get_input_validation(self, input_id):
        return self.driver.find_element(By.ID, input_id).get_attribute("validationMessage")
