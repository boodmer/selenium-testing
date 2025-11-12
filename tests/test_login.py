from pages.login_page import LoginPage
from selenium.webdriver.chrome.webdriver import WebDriver

def test_login_success(driver: WebDriver):
    login = LoginPage(driver)
    login.open()
    login.login("tomsmith", "SuperSecretPassword!")
    
    flash_text = login.get_message()
    assert "You logged into a secure area!" in flash_text
