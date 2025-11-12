from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    def __init__(self, driver, base_url = "https://the-internet.herokuapp.com"):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + "/login")

    def login(self, username, password):
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def get_message(self):
        return self.driver.wait.until(
            EC.visibility_of_element_located((By.ID, "flash"))
        ).text