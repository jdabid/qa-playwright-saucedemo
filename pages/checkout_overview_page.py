"""CheckoutOverviewPage module for Step Two: Order Overview & Totals."""

import re
from decimal import Decimal
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    """Page Object for Checkout Step Two: Overview & Price Summary."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Overview items and price labels
        self.item_prices: Locator = page.locator('[data-test="inventory-item-price"]')
        self.subtotal_label: Locator = page.locator('[data-test="subtotal-label"]')
        self.tax_label: Locator = page.locator('[data-test="tax-label"]')
        self.total_label: Locator = page.locator('[data-test="total-label"]')
        self.finish_button: Locator = page.locator('[data-test="finish"]')
        self.cancel_button: Locator = page.locator('[data-test="cancel"]')

    @staticmethod
    def _extract_amount(label_text: str) -> Decimal:
        """Helper to extract a currency number like '$39.98' into a Decimal."""
        match = re.search(r"(\d+\.\d{2})", label_text)
        if not match:
            raise ValueError(f"Could not extract monetary value from: '{label_text}'")
        return Decimal(match.group(1))

    def get_item_prices(self) -> list[Decimal]:
        """Returns the list of unit prices for all items in the overview."""
        raw_texts = self.item_prices.all_inner_texts()
        return [self._extract_amount(text) for text in raw_texts]

    def get_subtotal(self) -> Decimal:
        """Parses and returns the 'Item total: $XX.XX' label as Decimal."""
        return self._extract_amount(self.subtotal_label.inner_text())

    def get_tax(self) -> Decimal:
        """Parses and returns the 'Tax: $XX.XX' label as Decimal."""
        return self._extract_amount(self.tax_label.inner_text())

    def get_total(self) -> Decimal:
        """Parses and returns the final 'Total: $XX.XX' label as Decimal."""
        return self._extract_amount(self.total_label.inner_text())

    def finish_checkout(self) -> None:
        """Clicks Finish to place the order and navigate to confirmation."""
        self.finish_button.click()

    def cancel(self) -> None:
        """Cancels and returns to the inventory catalog."""
        self.cancel_button.click()
