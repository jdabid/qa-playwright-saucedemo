"""CartPage module representing the user shopping cart screen."""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object for the SauceDemo Shopping Cart Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Cart elements
        self.cart_items: Locator = page.locator('[data-test="inventory-item"]')
        self.item_names: Locator = page.locator('[data-test="inventory-item-name"]')
        self.checkout_button: Locator = page.locator('[data-test="checkout"]')
        self.continue_shopping_button: Locator = page.locator('[data-test="continue-shopping"]')

    def get_items_count(self) -> int:
        """Returns the number of products listed in the shopping cart."""
        return self.cart_items.count()

    def get_item_names(self) -> list[str]:
        """Returns the list of product names currently present in the cart."""
        return [name.strip() for name in self.item_names.all_inner_texts()]

    def proceed_to_checkout(self) -> None:
        """Clicks the Checkout button to begin the purchase process."""
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        """Clicks Continue Shopping to return to the inventory catalog."""
        self.continue_shopping_button.click()
