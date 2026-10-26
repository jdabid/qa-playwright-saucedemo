"""Inventory sorting and business logic test suite for SauceDemo.

Validates that catalog sorting options (price low-to-high, high-to-low, name A-Z/Z-A)
correctly sort items as expected.
"""

import pytest
from data.test_data import SortOptions
from pages.inventory_page import InventoryPage


@pytest.mark.regression
class TestInventorySorting:
    """Validation of inventory filtering and sorting logic."""

    def test_sort_by_price_low_to_high(
        self,
        logged_in_inventory: InventoryPage,
    ) -> None:
        """Validates that selecting 'Price (low to high)' sorts prices in ascending numerical order."""
        inventory_page = logged_in_inventory

        inventory_page.select_sort_option(SortOptions.PRICE_LOW_TO_HIGH)
        prices = inventory_page.get_all_prices()

        assert len(prices) > 0, "No prices were retrieved from the inventory page"
        assert prices == sorted(prices), (
            f"Expected prices sorted in ascending order. Received: {prices}, expected: {sorted(prices)}"
        )

    def test_sort_by_price_high_to_low(
        self,
        logged_in_inventory: InventoryPage,
    ) -> None:
        """Validates that selecting 'Price (high to low)' sorts prices in descending numerical order."""
        inventory_page = logged_in_inventory

        inventory_page.select_sort_option(SortOptions.PRICE_HIGH_TO_LOW)
        prices = inventory_page.get_all_prices()

        assert len(prices) > 0, "No prices were retrieved from the inventory page"
        assert prices == sorted(prices, reverse=True), (
            f"Expected prices sorted in descending order. Received: {prices}, expected: {sorted(prices, reverse=True)}"
        )

    @pytest.mark.parametrize(
        "sort_option,is_reversed",
        [
            (SortOptions.NAME_A_TO_Z, False),
            (SortOptions.NAME_Z_TO_A, True),
        ],
        ids=["name_a_to_z", "name_z_to_a"],
    )
    def test_sort_by_product_name(
        self,
        logged_in_inventory: InventoryPage,
        sort_option: str,
        is_reversed: bool,
    ) -> None:
        """Validates that alphabetical sorting correctly arranges product titles."""
        inventory_page = logged_in_inventory

        inventory_page.select_sort_option(sort_option)
        names = inventory_page.get_all_product_names()

        assert len(names) > 0, "No product names were retrieved from the inventory page"
        expected_names = sorted(names, reverse=is_reversed)
        assert names == expected_names, (
            f"Alphabetical sorting mismatch for option '{sort_option}'"
        )
