"""CheckoutInfoPage module for Step One: Customer Information."""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    """Page Object for Checkout Step One: Your Information."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Shipping information inputs and buttons
        self.first_name_input: Locator = page.locator('[data-test="firstName"]')
        self.last_name_input: Locator = page.locator('[data-test="lastName"]')
        self.postal_code_input: Locator = page.locator('[data-test="postalCode"]')
        self.continue_button: Locator = page.locator('[data-test="continue"]')
        self.cancel_button: Locator = page.locator('[data-test="cancel"]')
        self.error_banner: Locator = page.locator('[data-test="error"]')

    def fill_shipping_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Populates all required shipping fields in step one."""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_to_overview(self) -> None:
        """Submits customer information to navigate to checkout step two."""
        self.continue_button.click()

    def cancel(self) -> None:
        """Aborts checkout and returns to the cart."""
        self.cancel_button.click()

    def get_error_message(self) -> str:
        """Returns the validation error banner text if any required field is omitted."""
        return self.error_banner.inner_text().strip()
