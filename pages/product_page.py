# pages/product_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time


class ProductPage:
    """
    Page Object cho trang chi tiết sản phẩm - chức năng Thêm vào giỏ hàng.

    Logic dữ liệu test đang dùng:
    - /details/1  -> Xe đạp địa hình (còn hàng, dùng cho case hợp lệ)
    - /details/2  -> Xe đạp trẻ em (hết hàng)
    - /details/999999 -> Sản phẩm không tồn tại (trả về 404, title = "Not Found")
    """

    def __init__(self, driver, base_url="http://127.0.0.1:8000"):
        self.driver = driver
        self.base_url = base_url

    # =========================
    # OPEN PRODUCT PAGES
    # =========================

    def open_product_by_id(self, product_id: int):
        """
        Mở trang chi tiết sản phẩm theo id.

        Ví dụ:
        - 1: Xe đạp địa hình (còn hàng)
        - 2: Xe đạp trẻ em (hết hàng)
        """
        self.driver.get(f"{self.base_url}/details/{product_id}")
        self.wait_page_loaded()

    def open_non_existing_product(self):
        """
        Mở 1 sản phẩm không tồn tại để test 404.

        ID 999999 được dùng làm sản phẩm "ảo" để ép 404.
        """
        self.driver.get(f"{self.base_url}/details/999999")
        self.wait_page_loaded()

    # =========================
    # WAIT
    # =========================

    def wait_page_loaded(self):
        self.driver.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    # =========================
    # QUANTITY INPUT
    # =========================

    def set_quantity(self, value: str):
        """
        Nhập số lượng vào input id="quantity".

        - Hệ thống chỉ cho phép số (type=number), nên khi gửi "abc"
          browser sẽ tự block, dùng get_quantity_value() để kiểm tra lại.
        """
        qty_input = self.driver.find_element(By.ID, "quantity")
        qty_input.clear()
        qty_input.send_keys(value)

    def get_quantity_value(self) -> str:
        """
        Lấy giá trị hiện tại của input quantity
        (dùng cho test 'không phải số' để xem browser đã chặn chưa).
        """
        qty_input = self.driver.find_element(By.ID, "quantity")
        return qty_input.get_attribute("value")

    # =========================
    # ADD TO CART BUTTON
    # =========================

    def click_add_to_cart(self):
        """
        Click nút thêm vào giỏ hàng id="addToCartBtn".
        """
        btn = self.driver.find_element(By.ID, "addToCartBtn")
        try:
            # Chờ phần tử có thể click được
            self.driver.wait.until(EC.element_to_be_clickable((By.ID, "addToCartBtn")))
            btn.click()
        except ElementClickInterceptedException:
            # Nếu bị che phủ, scroll vào view rồi click bằng JS làm fallback
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(0.2)
            self.driver.execute_script("arguments[0].click();", btn)

    def is_add_to_cart_enabled(self) -> bool:
        """
        Trả về True nếu nút KHÔNG bị disabled.

        Logic hệ thống:
        - Số lượng âm / vượt tồn kho / để trống -> disabled
        - Hợp lệ (1..tồn kho) -> enabled
        """
        btn = self.driver.find_element(By.ID, "addToCartBtn")
        disabled = btn.get_attribute("disabled")
        return disabled is None

    # =========================
    # OUT OF STOCK
    # =========================

    def is_out_of_stock_displayed(self) -> bool:
        """
        Kiểm tra hiển thị chữ 'Hết hàng' trên trang sản phẩm.
        Dùng cho sản phẩm: Xe đạp trẻ em (/details/2).
        """
        return "Hết hàng" in self.driver.page_source

    # =========================
    # 404 PAGE CHECK
    # =========================

    def is_404_page(self) -> bool:
        """
        Kiểm tra trang 404.

        Logic: trang 404 có title = "Not Found".
        Dùng cho sản phẩm không tồn tại: /details/999999.
        """
        title = self.driver.title.strip()
        return title.lower() == "not found"
