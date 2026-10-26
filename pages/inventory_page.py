"""InventoryPage module encapsulating the product catalog and sorting interactions."""

import re
from decimal import Decimal
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page Object for the SauceDemo Inventory / Products Catalog Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Inventory catalog locators
        self.inventory_container: Locator = page.locator('[data-test="inventory-container"]')
        self.inventory_items: Locator = page.locator('[data-test="inventory-item"]')
        self.item_names: Locator = page.locator('[data-test="inventory-item-name"]')
        self.item_prices: Locator = page.locator('[data-test="inventory-item-price"]')
        self.sort_select: Locator = page.locator('[data-test="product-sort-container"]')
        self.active_sort_option: Locator = page.locator('[data-test="active-option"]')

    def add_product_to_cart(self, product_name: str) -> None:
        """Finds an inventory card matching `product_name` and clicks 'Add to cart'."""
        item = self.inventory_items.filter(has_text=product_name)
        item.get_by_role("button", name="Add to cart").click()

    def remove_product_from_cart(self, product_name: str) -> None:
        """Finds an inventory card matching `product_name` and clicks 'Remove'."""
        item = self.inventory_items.filter(has_text=product_name)
        item.get_by_role("button", name="Remove").click()

    def select_sort_option(self, option_value: str) -> None:
        """Selects a sorting option from the dropdown (e.g., 'lohi', 'hilo', 'az', 'za')."""
        self.sort_select.select_option(option_value)

    def get_all_prices(self) -> list[Decimal]:
        """Returns the list of visible item prices as Decimals to avoid floating-point issues."""
        raw_texts = self.item_prices.all_inner_texts()
        cleaned_prices: list[Decimal] = []
        for text in raw_texts:
            # Extract number from format like '$29.99'
            match = re.search(r"\d+\.\d{2}", text)
            if match:
                cleaned_prices.append(Decimal(match.group(0)))
        return cleaned_prices

    def get_all_product_names(self) -> list[str]:
        """Returns the list of product titles currently rendered on the page."""
        return [name.strip() for name in self.item_names.all_inner_texts()]
