import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://the-internet.herokuapp.com/login"

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_successful_login(driver):
    driver.get(LOGIN_URL)

    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    ).text

    assert "You logged into a secure area!" in success_message


def test_wrong_email_login(driver):
    driver.get(LOGIN_URL)

    driver.find_element(By.ID, "username").send_keys("wrong_user")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    ).text

    assert "Your username is invalid!" in error_message
