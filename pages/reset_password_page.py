from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ResetPasswordPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Nhập mật khẩu mới
    def enter_password(self, password):
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(password)

    # Nhập xác nhận mật khẩu
    def enter_password_confirmation(self, password_confirm):
        self.driver.find_element(By.ID, "password_confirmation").clear()
        self.driver.find_element(By.ID, "password_confirmation").send_keys(password_confirm)

    # Submit form
    def submit(self):
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        submit_button.click()

    # Gộp thao tác
    def reset_password(self, password, password_confirm):
        self.enter_password(password)
        self.enter_password_confirmation(password_confirm)
        self.submit()

    # Lấy thông báo thành công
    def get_success_message(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-success"))
        ).text

    # Lấy lỗi validation
    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
        ).text
