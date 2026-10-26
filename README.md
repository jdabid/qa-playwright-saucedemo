# SauceDemo E2E Test Automation Framework

![E2E Tests](https://github.com/jdabid/qa-playwright-saucedemo/actions/workflows/e2e-tests.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.14-blue.svg)
![Playwright](https://img.shields.io/badge/playwright-1.63%2B-green.svg)
![Pytest](https://img.shields.io/badge/pytest-9.1%2B-orange.svg)
![Quality Gate](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-purple.svg)

A production-grade, maintainable End-to-End (E2E) UI test automation framework built for [SauceDemo (Swag Labs)](https://www.saucedemo.com/) using **Python 3**, **Playwright**, and **Pytest**, structured strictly according to the **Page Object Model (POM)** pattern and integrated into automated CI/CD quality gates.

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Architecture & Design Principles](#-architecture--design-principles)
- [Directory Structure](#-directory-structure)
- [Automated Test Scenarios](#-automated-test-scenarios)
- [Prerequisites & Getting Started](#-prerequisites--getting-started)
- [Running Tests](#-running-tests)
- [Reporting & Debugging Artifacts](#-reporting--debugging-artifacts)
- [Engineering & Design Decisions](#-engineering--design-decisions)
- [CI/CD Pipeline (GitHub Actions)](#-cicd-pipeline-github-actions)
- [Future Improvements](#-future-improvements)

---

## 🎯 Project Overview

This repository demonstrates industry-standard quality engineering practices for web UI test automation:
- **Clean Architecture:** Strict separation between UI locators/actions (Page Objects) and test assertions (Test Suite).
- **Zero Flakiness Policy:** Elimination of arbitrary `sleep` timeouts; relies exclusively on Playwright's auto-waiting and web-first asynchronous assertions (`expect`).
- **Mathematical Accuracy:** Financial total verification using Python's `decimal.Decimal` module to prevent IEEE 754 floating-point inaccuracies.
- **Continuous Quality Gate:** Automated headless execution in GitHub Actions on every push and pull request with downloadable diagnostic artifacts.

---

## 🏛️ Architecture & Design Principles

```
┌────────────────────────────────────────────────────────┐
│                   Test Scenarios                       │
│        (tests/test_*.py with pytest assertions)        │
└───────────┬────────────────────────────────┬───────────┘
            │ calls actions                  │ verifies
            ▼                                ▼
┌────────────────────────┐      ┌────────────────────────┐
│   Page Object Model    │      │  Centralized Test Data │
│   (pages/*_page.py)    │      │  (data/test_data.py)   │
│  - Locators            │      │  - User credentials    │
│  - Element actions     │      │  - Customer profiles   │
│  - Data extraction     │      │  - Expected copy       │
└───────────┬────────────┘      └────────────────────────┘
            │ interacts with DOM
            ▼
┌────────────────────────────────────────────────────────┐
│             Playwright Browser Context                 │
│              (SauceDemo Web Application)               │
└────────────────────────────────────────────────────────┘
```

1. **Single Responsibility Principle (SRP):** Page Objects provide services and actions offered by the UI; they do **not** assert business outcomes. Asserts live entirely within the test layer.
2. **DRY (Don't Repeat Yourself):** Reusable page fixtures and pre-authenticated session fixtures are managed in `tests/conftest.py`.
3. **Resilient Selectors:** Locators target stable test attributes (`[data-test="..."]`), guarding the suite against brittle CSS class changes.

---

## 📂 Directory Structure

```
qa-playwright-saucedemo/
├── .github/
│   └── workflows/
│       └── e2e-tests.yml          # GitHub Actions CI workflow (push & PR to main)
├── data/
│   ├── __init__.py
│   └── test_data.py               # Immutable data classes for users, customers, copy
├── pages/                         # Page Object Model Layer
│   ├── __init__.py
│   ├── base_page.py               # Shared header navigation, cart badge, base methods
│   ├── login_page.py              # Authentication inputs and actions
│   ├── inventory_page.py          # Catalog cards, item addition, dropdown sorting
│   ├── cart_page.py               # Cart items overview and checkout trigger
│   ├── checkout_info_page.py      # Step One: First name, last name, postal code
│   ├── checkout_overview_page.py  # Step Two: Dynamic item prices, subtotal, tax, total
│   └── checkout_complete_page.py  # Order confirmation banner and back navigation
├── tests/                         # Test Execution Layer
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures (isolated page objects & auth sessions)
│   ├── test_authentication.py     # Scenario 1: Valid & locked-out user validations
│   ├── test_checkout_e2e.py       # Scenario 2: E2E purchase journey with arithmetic checks
│   └── test_inventory_sorting.py  # Scenario 3: Inventory sorting (price & name)
├── .gitignore
├── pytest.ini                     # Pytest runners, markers, base URL, reporting flags
├── requirements.txt               # Pinned dependencies
└── README.md                      # Framework documentation
```

---

## 🧪 Automated Test Scenarios

| Scenario | File | Markers | Description |
|---|---|---|---|
| **Authentication: Valid Login** | `tests/test_authentication.py` | `@pytest.mark.smoke` | Validates successful login with `standard_user` and redirect to `/inventory.html`. |
| **Authentication: Locked Out** | `tests/test_authentication.py` | `@pytest.mark.smoke` | Asserts error banner copy for `locked_out_user` and checks URL remains on login. |
| **Authentication: Negative Form** | `tests/test_authentication.py` | `@pytest.mark.smoke` | Parameterized test for missing username, missing password, and invalid credentials. |
| **E2E Purchase Journey** | `tests/test_checkout_e2e.py` | `@pytest.mark.e2e`, `@pytest.mark.smoke` | Adds 2 items, validates cart badge, fills shipping info, dynamically calculates Subtotal + Tax = Total via `Decimal`, and asserts confirmation. |
| **Inventory: Low-to-High Price** | `tests/test_inventory_sorting.py` | `@pytest.mark.regression` | Selects `Price (low to high)` and validates ascending numerical order. |
| **Inventory: High-to-Low Price** | `tests/test_inventory_sorting.py` | `@pytest.mark.regression` | Selects `Price (high to low)` and validates descending numerical order. |
| **Inventory: Alphabetical Sorting** | `tests/test_inventory_sorting.py` | `@pytest.mark.regression` | Parameterized test checking `A-to-Z` and `Z-to-A` product name ordering. |

---

## 🚀 Prerequisites & Getting Started

### Prerequisites
- **Python 3.12+** (compatible with Python 3.12 up to Python 3.14)
- **Git**

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/cristiandavidcastro/qa-playwright-saucedemo.git
   cd qa-playwright-saucedemo
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # On Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browser binaries:
   ```bash
   playwright install chromium
   ```

---

## 🏃 Running Tests

Run the full suite in default headless mode:
```bash
pytest
```

Run tests with visual browser execution and slowed execution for local debugging:
```bash
pytest --headed --slowmo 500
```

Run specific test markers:
```bash
# Run only critical smoke tests
pytest -m smoke

# Run only the end-to-end checkout flow
pytest -m e2e

# Run inventory regression suite
pytest -m regression
```

Run a specific test file:
```bash
pytest tests/test_checkout_e2e.py -v
```

---

## 📊 Reporting & Debugging Artifacts

- **HTML Report:** Each run automatically outputs a standalone, self-contained HTML report at `reports/report.html`. Open it in any browser:
  ```bash
  open reports/report.html      # On macOS
  xdg-open reports/report.html  # On Linux
  start reports/report.html     # On Windows
  ```
- **Screenshots, Videos & Traces:** As configured in `pytest.ini`, failed tests automatically produce screenshots, videos, and full execution traces in the `test-results/` directory (`--tracing retain-on-failure`).
- **Inspecting Playwright Traces:**
  ```bash
  playwright show-trace test-results/<test-run-folder>/trace.zip
  ```

---

## 💡 Engineering & Design Decisions

1. **No `time.sleep()` / Anti-Flakiness Guarantee:**  
   Playwright natively auto-waits for actionability (visible, stable DOM, enabled, receiving events). Combined with `expect(locator).to_be_visible()`, the test runner polls automatically until conditions pass or timeouts expire.
2. **Dynamic Currency Arithmetic via `Decimal`:**  
   In `test_checkout_e2e.py`, rather than hardcoding static totals (e.g. `$43.18`), the test reads individual unit prices from the DOM, calculates `sum(prices)`, and compares it against the displayed subtotal. Calculations utilize Python's `Decimal` type to prevent float rounding glitches (`0.1 + 0.2 != 0.3`).
3. **Context Isolation per Test:**  
   `pytest-playwright` boots each test inside a fresh `BrowserContext`. This guarantees pristine browser cache, cookies, and local storage per test with zero state leak.
4. **Resilient Selectors:**  
   All page interactions use SauceDemo's dedicated `data-test` attributes (e.g., `[data-test="username"]`, `[data-test="inventory-item"]`) rather than brittle DOM hierarchy or changing CSS styling classes.

---

## 🔄 CI/CD Pipeline (GitHub Actions)

A dedicated workflow is configured at [`.github/workflows/e2e-tests.yml`](.github/workflows/e2e-tests.yml):
- **Triggers:** Automatically on every `push` and `pull_request` targeting `main`, plus manual runs via `workflow_dispatch`.
- **Environment:** Clean `ubuntu-latest` runner with Python 3.12 and pip dependency caching.
- **Artifacts:** Generates and uploads `reports/` and `test-results/` under the `if: always()` condition, ensuring diagnostic evidence is preserved for 14 days even when tests fail.

---

## 🔮 Future Improvements

- **Cross-Browser Matrix:** Extend the GitHub Actions matrix to run Chromium, Firefox, and WebKit in parallel.
- **Parallel Test Execution:** Integrate `pytest-xdist` (`pytest -n auto`) for multi-core test acceleration.
- **Rich Reporting:** Add Allure Framework report generation for enterprise executive dashboards.
- **API Pre-seeding:** Use direct API calls (`playwright.request`) to pre-seed cart sessions, optimizing UI tests to only cover presentation logic.
