from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class SearchPage:
    def __init__(self, driver):
        self.driver = driver

    # =========================
    # WAIT UTILITIES
    # =========================

    def wait_dom_ready(self):
        """Đợi DOM tải hoàn tất."""
        self.driver.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def wait_search_ready(self):
        """Đợi searchInput xuất hiện trong DOM."""
        self.wait_dom_ready()
        self.driver.wait.until(
            lambda d: d.execute_script(
                "return document.getElementById('searchInput') !== null;"
            )
        )

    def wait_for_result_page(self):
        """Đợi redirect sang trang kết quả /find."""
        self.driver.wait.until(
            lambda d: "/find" in d.current_url
        )

    # =========================
    # ACTION
    # =========================

    def search(self, keyword: str):
        """
        Nhập từ khóa và submit tìm kiếm.
        Dùng cho cả trường hợp hợp lệ và không hợp lệ.
        """
        self.wait_search_ready()

        search_input = self.driver.find_element(By.ID, "searchInput")
        search_input.clear()
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.ENTER)

    # =========================
    # VALIDATION ERROR
    # =========================

    def get_error_message(self) -> str:
        """
        Lấy thông báo lỗi validate từ #searchError.
        Dùng cho các test không redirect (input không hợp lệ).
        """
        error = self.driver.wait.until(
            EC.visibility_of_element_located((By.ID, "searchError"))
        )
        return error.text.strip()

    # =========================
    # RESULT CHECK
    # =========================

    def is_on_result_page(self) -> bool:
        """Kiểm tra đang ở trang kết quả (/find?search=...)."""
        return "/find" in self.driver.current_url

    def has_results(self) -> bool:
        """
        Kiểm tra có sản phẩm trong trang kết quả.
        Mỗi sản phẩm có class = 'product-item'.
        """
        items = self.driver.find_elements(By.CLASS_NAME, "product-item")
        return len(items) > 0

    def has_no_products_message(self) -> bool:
        """
        Kiểm tra thông báo "không có sản phẩm" với id = 'noProductsMessage'.
        Dùng cho test 'không có kết quả'.
        """
        message = self.driver.wait.until(
            EC.visibility_of_element_located((By.ID, "noProductsMessage"))
        )
        return message.is_displayed()

    def get_first_product_name(self) -> str:
        """
        Lấy tên sản phẩm đầu tiên trong danh sách kết quả.
        - Mỗi sản phẩm có class: product-item
        - Tên sản phẩm nằm trong class: product-name
        """

        # Lấy product-item đầu tiên
        first_item = self.driver.find_element(By.CSS_SELECTOR, ".product-item")

        return first_item.text.strip()