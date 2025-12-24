from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class LoginPage:

    def __init__(self, driver, base_url="http://127.0.0.1:8000"):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + "/login")

    def login(self, username, password):
        self.driver.find_element(By.ID, "email").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def _wait(self, timeout=10):
        return getattr(self.driver, "wait", WebDriverWait(self.driver, timeout))

    def wait_for_login_success(self, timeout=10) -> bool:
        """Wait until an element that indicates a successful login is visible.

        Returns True when success indicator is visible, False on timeout.
        """
        wait = self._wait(timeout)
        try:
            wait.until(EC.visibility_of_element_located((By.ID, "userMenuButton")))
            return True
        except TimeoutException:
            return False

    def wait_for_login_failure(self, timeout=10) -> str | None:
        """Wait until a failure/flash message is visible and return its text.

        Returns the message text, or None on timeout.
        """
        wait = self._wait(timeout)
        try:
            el = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "fl-message")))
            return el.text
        except TimeoutException:
            return None

    def get_flash_message(self):
        return self._wait().until(
            EC.visibility_of_element_located((By.CLASS_NAME, "fl-message"))
        ).text
    
    def get_error_message(self):
        return self._wait().until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
        ).text
    
    def get_second_error_message(self):
        """
        Lấy error-message thứ 2 (thường là lỗi mật khẩu).
        """
        self._wait().until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "error-message"))
        )

        error_elements = self.driver.find_elements(By.CLASS_NAME, "error-message")

        if len(error_elements) >= 2:
            return error_elements[1].text.strip()
        return ""


