import pytest
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from dotenv import load_dotenv


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.wait = WebDriverWait(driver, 15)
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_driver(driver):
    load_dotenv()
    TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "minhchi@gmail.com")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "12345678")
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)

    driver.wait.until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    driver.wait.until(
        lambda d: d.execute_script("return document.getElementById('searchInput') !== null;")
    )

    return driver