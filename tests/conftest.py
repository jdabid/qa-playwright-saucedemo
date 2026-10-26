"""Shared pytest fixtures for the SauceDemo test suite.

Provides isolated Page Object instances and pre-authenticated sessions per test.
pytest-playwright automatically supplies an isolated browser context per test function.
"""

import pytest
from playwright.sync_api import Page, expect

from data.test_data import TestUsers
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Fixture providing an initialized LoginPage navigated to base_url."""
    login = LoginPage(page)
    login.navigate("/")
    return login


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """Fixture providing an initialized InventoryPage instance."""
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """Fixture providing an initialized CartPage instance."""
    return CartPage(page)


@pytest.fixture
def checkout_info_page(page: Page) -> CheckoutInfoPage:
    """Fixture providing an initialized CheckoutInfoPage instance."""
    return CheckoutInfoPage(page)


@pytest.fixture
def checkout_overview_page(page: Page) -> CheckoutOverviewPage:
    """Fixture providing an initialized CheckoutOverviewPage instance."""
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    """Fixture providing an initialized CheckoutCompletePage instance."""
    return CheckoutCompletePage(page)


@pytest.fixture
def logged_in_inventory(
    page: Page,
    login_page: LoginPage,
    inventory_page: InventoryPage,
) -> InventoryPage:
    """Fixture that logs in with standard_user and yields the ready InventoryPage."""
    login_page.login(
        username=TestUsers.STANDARD_USER.username,
        password=TestUsers.STANDARD_USER.password,
    )
    # Ensure inventory page is rendered before handing over to test
    expect(inventory_page.header_title).to_be_visible()
    expect(inventory_page.header_title).to_have_text("Products")
    return inventory_page
