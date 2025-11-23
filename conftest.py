import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.search_page import SearchPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.wait = WebDriverWait(driver, 15)
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("minhchi@gmail.com", "12345678")

    driver.wait.until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    driver.wait.until(
        lambda d: d.execute_script("return document.getElementById('searchInput') !== null;")
    )

    return driver