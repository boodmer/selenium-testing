from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MaintenanceRequestPage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ========== LOCATORS ==========

    CUSTOMER_NAME_INPUT = (By.NAME, "customer_name")
    PHONE_INPUT = (By.NAME, "phone")
    EMAIL_INPUT = (By.NAME, "email")
    PRODUCT_SKU_INPUT = (By.NAME, "product_sku")
    PREFERRED_DATE_INPUT = (By.NAME, "preferred_date")
    ADDRESS_INPUT = (By.NAME, "address")
    ISSUE_DESCRIPTION_TEXTAREA = (By.NAME, "issue_description")

    SUBMIT_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Gửi yêu cầu']"
    )

    # ✅ Bắt SUCCESS kể cả khi redirect nhanh
    SUCCESS_ALERT = (
        By.XPATH,
        "//*[contains(translate(text(),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'thành công') "
        "or contains(text(),'success') "
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

    def fill_maintenance_request(
        self,
        customer_name,
        phone,
        email,
        product_sku,
        preferred_date,
        address,
        issue_description
    ):
        self._type(self.CUSTOMER_NAME_INPUT, customer_name)
        self._type(self.PHONE_INPUT, phone)
        self._type(self.EMAIL_INPUT, email)
        self._type(self.PRODUCT_SKU_INPUT, product_sku)
        self._type(self.PREFERRED_DATE_INPUT, preferred_date)
        self._type(self.ADDRESS_INPUT, address)
        self._type(self.ISSUE_DESCRIPTION_TEXTAREA, issue_description)

    def submit(self):
        btn = self.wait.until(
            EC.presence_of_element_located(self.SUBMIT_BUTTON)
        )

        # Scroll để tránh footer / toast che
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", btn
        )

        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))

        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

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

    # 🔴 HÀM BỊ THIẾU → NGUYÊN NHÂN LỖI
    def _type(self, locator, value):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(value)

    # 🔥 GIỐNG ProfilePage
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
            f"//textarea[@name='{field}']"
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
