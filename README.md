# Selenium Testing

A compact pytest + Selenium test suite for a web application. Tests live in `tests/`, page objects in `pages/`, and test fixtures in `conftest.py`.

**Quick Overview**
- **Tests:** `tests/` (`test_login.py`, `test_search.py`)
- **Page objects:** `pages/` (`login_page.py`, `search_page.py`)
- **Fixtures:** `conftest.py` (provides `driver` and `logged_in_driver` fixtures)

**Prerequisites**
- Python 3.8+ installed
- Chrome browser installed (matching ChromeDriver)
- (Recommended) Create a virtual environment

**Install dependencies**
Open PowerShell and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Notes:
- `requirements.txt` includes `selenium`, `pytest`, and `python-dotenv`.
- If you prefer automatic driver management, install `webdriver-manager` and update the fixture to use it.

**Environment variables (.env)**
This project reads test credentials from environment variables. A template is provided in `.env.example`.

- Copy `.env.example` to `.env` and set real credentials (do NOT commit `.env`):

```powershell
copy .env.example .env
# then edit .env and fill values
```

Keys used:
- `TEST_USER_EMAIL` — login email used by `logged_in_driver`
- `TEST_USER_PASSWORD` — login password

`conftest.py` calls `load_dotenv()` if `python-dotenv` is available, so values from `.env` are loaded into `os.getenv()`.

**Running tests**
Run the full test suite:

```powershell
pytest -q
```

Run a single test file or test:

```powershell
pytest tests/test_search.py -q
pytest tests/test_search.py::test_search_success -q
```

**What the fixtures do**
- `driver`: creates `webdriver.Chrome()` and attaches a `WebDriverWait` instance on `driver.wait` for convenient waiting in page objects.
- `logged_in_driver`: logs in using the `LoginPage` page object, waits for a clear success indicator (`id="userMenuButton"`) and then waits for the landing page search input to appear. This prevents tests from trying to interact with elements before the page fully loads.

**Page object notes**
- `LoginPage` now provides `wait_for_login_success()` and `wait_for_login_failure()` to explicitly assert login result.
- `SearchPage` has a robust `_find_search_input()` helper which waits for the search input using several common locators. Tests should rely on the `logged_in_driver` fixture to ensure the search input is present before interacting.

**Troubleshooting**
- If you see `NoSuchElementException` for `searchInput`, increase waits or check network/redirect behavior. You can change the wait time in `conftest.py` or the page object helpers.
- To run headless Chrome during CI, modify the `driver` fixture to add ChromeOptions with `--headless=new` (or `--headless` depending on Chrome version).
- If `python-dotenv` isn't installed you will still use OS environment variables (the import is wrapped in a try/except). Installing `python-dotenv` is recommended for local development.

**Optional improvements**
- Add `.env` to `.gitignore` (if not already ignored).
- Use `webdriver-manager` to avoid managing ChromeDriver manually.
- Extend page objects with more explicit wait helpers for your application's common flows.

**Contact / Next steps**
If you'd like, I can:
- Add `.gitignore` entries for `.env` and virtualenv folders.
- Run the test suite here and report results (if you want me to run `pytest -q`).

Enjoy testing!