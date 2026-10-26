"""CheckoutCompletePage module for the order confirmation screen."""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    """Page Object for Checkout: Complete! screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Success message locators
        self.complete_header: Locator = page.locator('[data-test="complete-header"]')
        self.complete_text: Locator = page.locator('[data-test="complete-text"]')
        self.back_home_button: Locator = page.locator('[data-test="back-to-products"]')

    def get_complete_header_text(self) -> str:
        """Returns the confirmation header text ('Thank you for your order!')."""
        return self.complete_header.inner_text().strip()

    def get_complete_text(self) -> str:
        """Returns the dispatch notice body text."""
        return self.complete_text.inner_text().strip()

    def back_to_home(self) -> None:
        """Clicks the Back Home button to return to the inventory catalog."""
        self.back_home_button.click()
