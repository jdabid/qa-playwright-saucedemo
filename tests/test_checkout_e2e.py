"""End-to-End (E2E) purchase journey test suite for SauceDemo.

Validates the full checkout flow from catalog to order confirmation,
including dynamic mathematical validation of item subtotals, tax, and final totals
using Python Decimal.
"""

import re
import pytest
from playwright.sync_api import Page, expect

from data.test_data import Products, CustomerData, ExpectedMessages
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage


@pytest.mark.e2e
@pytest.mark.smoke
class TestCheckoutE2E:
    """Full End-to-End purchase lifecycle validation."""

    def test_complete_purchase_journey_with_totals_validation(
        self,
        page: Page,
        logged_in_inventory: InventoryPage,
        cart_page: CartPage,
        checkout_info_page: CheckoutInfoPage,
        checkout_overview_page: CheckoutOverviewPage,
        checkout_complete_page: CheckoutCompletePage,
    ) -> None:
        """Executes a complete e-commerce purchase and dynamically verifies arithmetic totals.
        
        Flow:
        1. Select 2 items and add them to the cart.
        2. Assert cart badge updates to 2.
        3. Navigate to shopping cart and assert 2 items listed.
        4. Proceed to checkout step one and supply shipping details.
        5. In checkout step two, dynamically sum unit prices and assert against subtotal.
        6. Validate subtotal + tax == final total.
        7. Complete the purchase and verify the confirmation banner.
        """
        inventory_page = logged_in_inventory

        # Step 1: Add products to cart
        for product in Products.E2E_SELECTED_PRODUCTS:
            inventory_page.add_product_to_cart(product)

        # Step 2: Assert shopping cart badge reflects the added count
        expect(inventory_page.cart_badge).to_have_text(str(len(Products.E2E_SELECTED_PRODUCTS)))

        # Step 3: Open cart and verify items
        inventory_page.open_cart()
        expect(page).to_have_url(re.compile(r".*/cart\.html$"))
        expect(cart_page.cart_items).to_have_count(len(Products.E2E_SELECTED_PRODUCTS))

        # Step 4: Proceed to Checkout Step One
        cart_page.proceed_to_checkout()
        expect(page).to_have_url(re.compile(r".*/checkout-step-one\.html$"))

        # Step 5: Fill customer information and continue
        customer = CustomerData.DEFAULT_CUSTOMER
        checkout_info_page.fill_shipping_info(
            first_name=customer.first_name,
            last_name=customer.last_name,
            postal_code=customer.postal_code,
        )
        checkout_info_page.continue_to_overview()

        # Step 6: Step Two - Dynamic Mathematical Totals Verification
        expect(page).to_have_url(re.compile(r".*/checkout-step-two\.html$"))

        # Extract unit prices dynamically from overview
        unit_prices = checkout_overview_page.get_item_prices()
        assert len(unit_prices) == len(Products.E2E_SELECTED_PRODUCTS), (
            f"Expected {len(Products.E2E_SELECTED_PRODUCTS)} item prices, found {len(unit_prices)}"
        )

        calculated_subtotal = sum(unit_prices)
        ui_subtotal = checkout_overview_page.get_subtotal()
        assert ui_subtotal == calculated_subtotal, (
            f"Subtotal calculation mismatch: UI says {ui_subtotal}, but items sum to {calculated_subtotal}"
        )

        ui_tax = checkout_overview_page.get_tax()
        ui_total = checkout_overview_page.get_total()
        expected_total = calculated_subtotal + ui_tax
        assert ui_total == expected_total, (
            f"Final total mismatch: UI says {ui_total}, but Subtotal ({calculated_subtotal}) + Tax ({ui_tax}) = {expected_total}"
        )

        # Step 7: Finish order and assert final confirmation
        checkout_overview_page.finish_checkout()
        expect(page).to_have_url(re.compile(r".*/checkout-complete\.html$"))

        expect(checkout_complete_page.complete_header).to_be_visible()
        expect(checkout_complete_page.complete_header).to_have_text(
            ExpectedMessages.ORDER_COMPLETE_HEADER
        )
        expect(checkout_complete_page.complete_text).to_contain_text(
            ExpectedMessages.ORDER_COMPLETE_TEXT
        )
