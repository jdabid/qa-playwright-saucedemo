"""Page Object Model package for SauceDemo."""

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage

__all__ = [
    "BasePage",
    "LoginPage",
    "InventoryPage",
    "CartPage",
    "CheckoutInfoPage",
    "CheckoutOverviewPage",
    "CheckoutCompletePage",
]
