import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

LOGIN_URL = "http://localhost:8000/login"

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# def test_successful_login(driver):
#     logger.info("Opening login page...")
#     driver.get(LOGIN_URL)

#     driver.find_element(By.ID, "email").send_keys("minhchi@gmail.com")
#     driver.find_element(By.ID, "password").send_keys("12345678")
#     driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

#     # ✅ Wait for redirected page & success message
#     WebDriverWait(driver, 10).until(
#         EC.any_of(
#             EC.visibility_of_element_located((By.ID, "userMenuButton")),
#             EC.visibility_of_element_located((By.CSS_SELECTOR, ".fl-message"))
#         )
#     )

#     message = driver.find_element(By.CSS_SELECTOR, ".fl-message").text
#     logger.info(message)
#     assert "Đăng nhập thành công" in message


def test_wrong_email_login(driver):
    driver.get(LOGIN_URL)

    driver.find_element(By.ID, "email").send_keys("wrong_email")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # ✅ Wait for error message to appear
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message"))
    )

    message = driver.find_element(By.CSS_SELECTOR, ".error-message").text
    assert "định dạng email" in message
