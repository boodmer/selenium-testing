import time
import logging
from pages.add_employee_page import DashboardPage, EmployeeListPage, AddEmployeePage
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

logger = logging.getLogger(__name__)


# =========================
# TC1 — Thêm nhân viên hợp lệ
# =========================
def test_add_employee_success(logged_in_admin_driver):
    driver = logged_in_admin_driver

    # Mở dashboard -> menu nhân viên -> thêm nhân viên
    dashboard = DashboardPage(driver)
    dashboard.click_employee_menu()

    employee_list = EmployeeListPage(driver)
    employee_list.click_add_employee()

    add_page = AddEmployeePage(driver)

    timestamp = str(int(time.time()))
    employee_name = f"Nguyen Van A {timestamp}"

    add_page.enter_name(employee_name)
    add_page.enter_phone("0912345678")
    add_page.enter_position("Nhân viên bán hàng")
    add_page.enter_address("Hồ Chí Minh")
    add_page.upload_image(str(BASE_DIR / "resources" / "employee.jpg"))

    add_page.click_submit()

    # Kiểm tra nhân viên xuất hiện trên danh sách
    assert employee_list.is_employee_displayed(employee_name)
    logger.info(f"[PASSED] Đã thêm nhân viên thành công: {employee_name}")


# =========================
# TC2 — Thiếu tên nhân viên
# =========================
def test_add_employee_missing_name(logged_in_admin_driver):
    driver = logged_in_admin_driver

    dashboard = DashboardPage(driver)
    dashboard.click_employee_menu()

    EmployeeListPage(driver).click_add_employee()
    add_page = AddEmployeePage(driver)

    add_page.enter_name("")  # bỏ trống
    add_page.enter_phone("0912345678")
    add_page.enter_position("Kế toán")
    add_page.enter_address("Đà Nẵng")

    add_page.click_submit()

    assert add_page.is_error_displayed("name")


# =========================
# TC3 — Số điện thoại sai định dạng
# =========================
def test_add_employee_invalid_phone(logged_in_admin_driver):
    driver = logged_in_admin_driver

    dashboard = DashboardPage(driver)
    dashboard.click_employee_menu()

    EmployeeListPage(driver).click_add_employee()
    add_page = AddEmployeePage(driver)

    add_page.enter_name("Pham Minh Hoang")
    add_page.enter_phone("abc123")  # ❌ invalid
    add_page.enter_position("Thu ngân")
    add_page.enter_address("Cần Thơ")

    add_page.click_submit()

    assert add_page.is_error_displayed("phone")


# =========================
# TC4 — Thiếu vị trí
# =========================
def test_add_employee_missing_position(logged_in_admin_driver):
    driver = logged_in_admin_driver

    dashboard = DashboardPage(driver)
    dashboard.click_employee_menu()

    EmployeeListPage(driver).click_add_employee()
    add_page = AddEmployeePage(driver)

    add_page.enter_name("Tran Hai Yen")
    add_page.enter_phone("0987654321")
    add_page.enter_position("")  # bỏ trống
    add_page.enter_address("Hải Phòng")

    add_page.click_submit()

    assert add_page.is_error_displayed("position")


# =========================
# TC5 — Ảnh upload sai định dạng
# =========================
def test_add_employee_invalid_image(logged_in_admin_driver):
    driver = logged_in_admin_driver

    dashboard = DashboardPage(driver)
    dashboard.click_employee_menu()

    EmployeeListPage(driver).click_add_employee()
    add_page = AddEmployeePage(driver)

    add_page.enter_name("Ngo Minh Duy")
    add_page.enter_phone("0911122233")
    add_page.enter_position("Quản lý")
    add_page.enter_address("Biên Hòa")

    add_page.upload_image(str(BASE_DIR / "resources" / "file.txt"))  # ❌ file sai loại

    add_page.click_submit()

    assert add_page.is_error_displayed("image")

# =========================
# TC6 — Số điện thoại trùng
# =========================
def test_add_employee_duplicate_phone(logged_in_admin_driver):
    driver = logged_in_admin_driver

    dashboard = DashboardPage(driver)
    dashboard.click_employee_menu()

    employee_list = EmployeeListPage(driver)
    employee_list.click_add_employee()

    add_page = AddEmployeePage(driver)

    # Số điện thoại đã tồn tại trong hệ thống
    add_page.enter_name("Le Trung Kien")
    add_page.enter_phone("0327264556")  # ❌ trùng với nhân viên khác
    add_page.enter_position("Nhân viên kho")
    add_page.enter_address("Hà Nội")

    add_page.click_submit()

    # Kiểm tra hiển thị lỗi trùng số điện thoại
    assert add_page.is_error_displayed("phone")

# =========================
# TC7 — Địa chỉ bỏ trống
# =========================
def test_add_employee_address_empty(logged_in_admin_driver):
    driver = logged_in_admin_driver

    dashboard = DashboardPage(driver)
    dashboard.click_employee_menu()

    EmployeeListPage(driver).click_add_employee()
    add_page = AddEmployeePage(driver)

    add_page.enter_name("Vu Minh Quan")
    add_page.enter_phone("0977889900")
    add_page.enter_position("Bảo vệ")
    add_page.enter_address("")  # ❌ bỏ trống

    add_page.click_submit()

    assert add_page.is_error_displayed("address")