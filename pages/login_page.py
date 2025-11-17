from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    def __init__(self, driver, base_url = "http://127.0.0.1:8000"):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + "/login")

    def login(self, username, password):
        self.driver.find_element(By.ID, "email").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def get_flash_message(self):
        return self.driver.wait.until(
            EC.visibility_of_element_located((By.ID, ".fl-message"))
        ).text
    
    def get_error_message(self):
         return self.driver.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
        ).text     