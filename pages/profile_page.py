from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ProfilePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ========== LOCATORS ==========
    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.NAME, "email")
    PHONE_INPUT = (By.NAME, "phone")
    ADDRESS_INPUT = (By.NAME, "address")

    DAY_SELECT = (By.NAME, "day")
    MONTH_SELECT = (By.NAME, "month")
    YEAR_SELECT = (By.NAME, "year")

    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'Lưu thay đổi')]")

    # ✅ Bắt SUCCESS kể cả khi redirect nhanh
    SUCCESS_ALERT = (
        By.XPATH,
        "//*[contains(translate(text(),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'thành công') "
        "or contains(text(),'success') "
        "or contains(text(),'cập nhật') "
        "or contains(@class,'alert-success') "
        "or contains(@class,'text-green')]"
    )

    GENERIC_ERROR = (
        By.XPATH,
        "//*[contains(@class,'alert-danger') "
        "or contains(text(),'Lỗi') "
        "or contains(text(),'thất bại')]"
    )

    # ========== ACTION ==========
    def fill_profile(self, name, email, phone, address, day, month, year):
        self._type(self.NAME_INPUT, name)
        self._type(self.EMAIL_INPUT, email)
        self._type(self.PHONE_INPUT, phone)
        self._type(self.ADDRESS_INPUT, address)

        self._select(self.DAY_SELECT, day)
        self._select(self.MONTH_SELECT, month)
        self._select(self.YEAR_SELECT, year)

    def submit(self):
        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON)).click()

    # ========== VALIDATION ==========
    def is_success_displayed(self, timeout=7):
        return self._is_present(self.SUCCESS_ALERT, timeout)

    def is_error_displayed(self, field_name=None):
        if not field_name:
            return self._is_present(self.GENERIC_ERROR, 5)

        return self._is_present(
            (By.XPATH, self._field_error_xpath(field_name)), 5
        )

    # ========== UTILS ==========
    def _type(self, locator, value):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(value)

    def _select(self, locator, value):
        self.wait.until(EC.presence_of_element_located(locator))
        Select(self.driver.find_element(*locator)).select_by_value(value)

    # 🔥 FIX QUAN TRỌNG (TC1)
    def _is_present(self, locator, timeout):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def _field_error_xpath(self, field):
        base = (
            f"//input[@name='{field}'] | "
            f"//textarea[@name='{field}'] | "
            f"//select[@name='{field}']"
        )

        error = (
            "//*[contains(@class,'text-red') "
            "or contains(@class,'text-danger') "
            "or contains(text(),'không được') "
            "or contains(text(),'phải là')]"
        )

        return (
            f"({base}/ancestor::div[3]{error})[last()] | "
            f"({base}/ancestor::div[2]{error})[last()] | "
            f"({base}/ancestor::div[1]{error})[last()] | "
            f"//div[contains(@class,'text-red') and contains(text(),'{field}')]"
        )
