import logging
from pages.search_page import SearchPage

# Khởi tạo logger cho file này
logger = logging.getLogger(__name__)


# ======================================
# TC1: Tìm kiếm sản phẩm tồn tại
# ======================================
def test_search_success(logged_in_driver):
    logger.info("[TC1] Tìm kiếm sản phẩm tồn tại")

    driver = logged_in_driver
    page = SearchPage(driver)

    keyword = "s"  # Chỉnh theo dữ liệu thật
    page.search(keyword)
    page.wait_for_result_page()

    assert page.is_on_result_page()
    assert page.has_results() is True


# ======================================
# TC2: Tìm kiếm sản phẩm không tồn tại
# ======================================
def test_search_no_result(logged_in_driver):
    logger.info("[TC2] Tìm kiếm sản phẩm không tồn tại")

    driver = logged_in_driver
    page = SearchPage(driver)

    keyword = "xyzkhongtontai_123456"
    page.search(keyword)
    page.wait_for_result_page()

    assert page.is_on_result_page()
    assert page.has_results() is False
    assert page.has_no_products_message() is True


# ======================================
# TC3: Tìm kiếm từ khóa rỗng
# ======================================
def test_search_empty_keyword(logged_in_driver):
    logger.info("[TC3] Tìm kiếm với từ khóa rỗng")

    driver = logged_in_driver
    page = SearchPage(driver)

    page.search("")

    assert "/find" not in driver.current_url
    error = page.get_error_message()
    assert error != ""


# ======================================
# TC4: Tìm kiếm với ký tự đặc biệt
# ======================================
def test_search_special_characters(logged_in_driver):
    logger.info("[TC4] Tìm kiếm với ký tự đặc biệt")

    driver = logged_in_driver
    page = SearchPage(driver)

    page.search("@@@###")

    assert "/find" not in driver.current_url
    error = page.get_error_message()
    assert error != ""


# ======================================
# TC5: Tìm kiếm với khoảng trắng
# ======================================
def test_search_whitespace_only(logged_in_driver):
    logger.info("[TC5] Tìm kiếm với chuỗi khoảng trắng")

    driver = logged_in_driver
    page = SearchPage(driver)

    page.search("     ")

    assert "/find" not in driver.current_url
    error = page.get_error_message()
    assert error != ""


# ======================================
# TC6: Giá trị biên 1 ký tự
# ======================================
def test_search_min_length(logged_in_driver):
    logger.info("[TC6] Tìm kiếm với 1 ký tự")

    driver = logged_in_driver
    page = SearchPage(driver)

    page.search("a")
    page.wait_for_result_page()

    assert page.is_on_result_page()


# ======================================
# TC7: Giá trị biên tối đa hợp lệ (50 ký tự)
# ======================================
def test_search_max_valid_length(logged_in_driver):
    logger.info("[TC7] Tìm kiếm với 50 ký tự")

    driver = logged_in_driver
    page = SearchPage(driver)

    keyword = "a" * 50
    page.search(keyword)
    page.wait_for_result_page()

    assert page.is_on_result_page()


# ======================================
# TC8: Giá trị vượt biên (51 ký tự)
# ======================================
def test_search_over_max_length(logged_in_driver):
    logger.info("[TC8] Tìm kiếm với 51 ký tự")

    driver = logged_in_driver
    page = SearchPage(driver)

    keyword = "a" * 51
    page.search(keyword)

    assert "/find" not in driver.current_url
    error = page.get_error_message()
    assert error != ""


# ======================================
# TC9: Không phân biệt hoa thường
# ======================================
def test_search_case_insensitive(logged_in_driver):
    logger.info("[TC9] Tìm kiếm không phân biệt hoa thường - so sánh sản phẩm đầu tiên")

    driver = logged_in_driver
    page = SearchPage(driver)

    # Lần 1: tìm với chữ hoa
    page.search("XE")
    page.wait_for_result_page()

    name_upper = page.get_first_product_name()

    # Lần 2: tìm với chữ thường
    page.search("xe")
    page.wait_for_result_page()

    name_lower = page.get_first_product_name()

    # So sánh kết quả
    assert name_upper.lower() == name_lower.lower()
