# tests/test_cart.py

import logging
from pages.product_page import ProductPage

logger = logging.getLogger(__name__)

# Ghi chú chung cho file test:
# - /details/1 -> Xe đạp địa hình (còn hàng, dùng test hợp lệ & input số lượng)
# - /details/2 -> Xe đạp trẻ em (hết hàng, test case out of stock)
# - /details/999999 -> sản phẩm không tồn tại (trả về 404, title = "Not Found")


# =========================
# TC1 - Thêm hợp lệ
# =========================
def test_add_valid_product_to_cart(logged_in_driver):
    logger.info("[TC1] Thêm xe đạp địa hình hợp lệ vào giỏ hàng")

    page = ProductPage(logged_in_driver)
    page.open_product_by_id(1)  # 1 = Xe đạp địa hình (còn hàng)
    page.set_quantity("1")
    assert page.is_add_to_cart_enabled() is True

    page.click_add_to_cart()

    # Tuỳ UI: ở đây chỉ đảm bảo không lỗi, vẫn ở trang chi tiết /details/1
    assert "/details/1" in logged_in_driver.current_url


# =========================
# TC2 - Số lượng = 0 -> disabled
# =========================
def test_quantity_zero_disabled(logged_in_driver):
    logger.info("[TC2] Nhập số lượng = 0 → Nút bị disable")

    page = ProductPage(logged_in_driver)
    page.open_product_by_id(1)

    page.set_quantity("0")

    # Logic: số lượng = 0 => nút phải bị disable
    assert page.is_add_to_cart_enabled() is False


# =========================
# TC3 - Số lượng âm -> disabled
# =========================
def test_negative_quantity_disabled(logged_in_driver):
    logger.info("[TC3] Số lượng âm → Nút bị disable")

    page = ProductPage(logged_in_driver)
    page.open_product_by_id(1)

    page.set_quantity("-1")

    assert page.is_add_to_cart_enabled() is False


# =========================
# TC4 - Vượt tồn kho -> disabled
# =========================
def test_quantity_over_stock_disabled(logged_in_driver):
    logger.info("[TC4] Số lượng vượt tồn kho → Nút bị disable")

    page = ProductPage(logged_in_driver)
    page.open_product_by_id(1)

    # Ví dụ tồn kho thật là 10, mình test với 100
    page.set_quantity("100")

    assert page.is_add_to_cart_enabled() is False


# =========================
# TC5 - Nhập không phải số
# =========================
def test_non_numeric_input(logged_in_driver):
    logger.info("[TC5] Nhập ký tự không phải số (abc)")

    page = ProductPage(logged_in_driver)
    page.open_product_by_id(1)

    page.set_quantity("abc")

    # Do input type="number", browser sẽ không nhận chuỗi "abc"
    value = page.get_quantity_value()

    # Chỉ cần đảm bảo không giữ nguyên 'abc'
    assert value == "" or not value.isalpha()


# =========================
# TC6 - Để trống -> disabled
# =========================
def test_empty_quantity_disabled(logged_in_driver):
    logger.info("[TC6] Để trống số lượng → Nút bị disable")

    page = ProductPage(logged_in_driver)
    page.open_product_by_id(1)

    page.set_quantity("")

    assert page.is_add_to_cart_enabled() is False


# =========================
# TC7 - Thêm khi chưa đăng nhập
# =========================
def test_add_to_cart_without_login(driver):
    logger.info("[TC7] Thêm vào giỏ khi chưa đăng nhập")

    page = ProductPage(driver)
    page.open_product_by_id(1)

    # Logic hệ thống: nếu chưa login → chuyển sang trang đăng nhập
    assert "/login" in driver.current_url or "dang-nhap" in driver.current_url


# =========================
# TC8 - Sản phẩm hết hàng
# =========================
def test_out_of_stock_product(logged_in_driver):
    logger.info("[TC8] Thử thêm xe đạp trẻ em (hết hàng)")

    page = ProductPage(logged_in_driver)
    page.open_product_by_id(2)  # 2 = Xe đạp trẻ em (hết hàng)

    # Logic: phải hiển thị 'Hết hàng' trên giao diện
    assert page.is_out_of_stock_displayed() is True


# =========================
# TC9 - Sản phẩm không tồn tại -> 404
# =========================
def test_non_existing_product(logged_in_driver):
    logger.info("[TC9] Sản phẩm không tồn tại → 404 (Not Found)")

    page = ProductPage(logged_in_driver)
    page.open_non_existing_product()

    # Logic: 404 được nhận diện bằng title = "Not Found"
    assert page.is_404_page() is True
