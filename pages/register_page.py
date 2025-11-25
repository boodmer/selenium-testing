from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RegisterPage:

    def __init__(self, driver, base_url="http://127.0.0.1:8000"):
        self.driver = driver
        self.base_url = base_url

    # Mở trang đăng ký
    def open(self):
        self.driver.get(self.base_url + "/register")

    # Nhập thông tin form đăng ký
    def register(self, name, phone, birthday, address, email, password, password_confirm):
        self.driver.find_element(By.ID, "name").send_keys(name)
        self.driver.find_element(By.ID, "phone").send_keys(phone)
        self.driver.find_element(By.ID, "birthday").send_keys(birthday)
        self.driver.find_element(By.ID, "address").send_keys(address)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "password_confirmation").send_keys(password_confirm)

        # Cuộn đến nút "Submit" trước khi nhấp
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

        # Kiểm tra và xử lý overlay/popup nếu có
        try:
            overlay = self.driver.find_element(By.CSS_SELECTOR, ".overlay")  # Thay ".overlay" bằng selector của overlay nếu có
            if overlay.is_displayed():
                self.driver.execute_script("arguments[0].style.display = 'none';", overlay)
        except:
            pass  # Nếu không có overlay, bỏ qua

        # Chờ nút "Submit" có thể nhấp được
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))

        # Nhấp vào nút "Submit"
        try:
            submit_button.click()
        except Exception as e:
            # Nếu vẫn bị lỗi, thử nhấp bằng JavaScript
            self.driver.execute_script("arguments[0].click();", submit_button)

    # Lấy flash message thành công (nếu có)
    def get_flash_message(self):
        return self.driver.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".fl-message"))
        ).text

    # Lấy message lỗi trả về từ hệ thống
    def get_error_message(self):
        return self.driver.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
        ).text

    # Lấy message validation của trình duyệt khi bỏ trống input
    def get_input_validation(self, input_id):
        return self.driver.find_element(By.ID, input_id).get_attribute("validationMessage")