"""Authentication flow test suite for SauceDemo.

Covers valid login scenarios and negative authentication validations
(locked out account, missing credentials).
"""

import re
import pytest
from playwright.sync_api import Page, expect

from data.test_data import TestUsers, ExpectedMessages
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
class TestAuthentication:
    """Test suite for login functionality and error handling."""

    def test_valid_login_redirects_to_inventory(
        self,
        page: Page,
        login_page: LoginPage,
        inventory_page: InventoryPage,
    ) -> None:
        """Validates that a standard user can successfully log in and is redirected to inventory."""
        login_page.login(
            username=TestUsers.STANDARD_USER.username,
            password=TestUsers.STANDARD_USER.password,
        )

        # Assert navigation to the inventory URL
        expect(page).to_have_url(re.compile(r".*/inventory\.html$"))

        # Assert the catalog header title is visible and displayed
        expect(inventory_page.header_title).to_be_visible()
        expect(inventory_page.header_title).to_have_text("Products")

    def test_locked_out_user_sees_error_banner(
        self,
        page: Page,
        login_page: LoginPage,
    ) -> None:
        """Validates that a locked out user is rejected and sees the exact error banner."""
        login_page.login(
            username=TestUsers.LOCKED_OUT_USER.username,
            password=TestUsers.LOCKED_OUT_USER.password,
        )

        # Assert error banner is rendered with exact expected copy
        expect(login_page.error_banner).to_be_visible()
        expect(login_page.error_banner).to_have_text(ExpectedMessages.LOCKED_OUT_ERROR)

        # Assert the user remained on the login page
        expect(page).not_to_have_url(re.compile(r".*/inventory\.html"))

    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            ("", "secret_sauce", ExpectedMessages.USERNAME_REQUIRED_ERROR),
            ("standard_user", "", ExpectedMessages.PASSWORD_REQUIRED_ERROR),
            ("invalid_user", "invalid_password", ExpectedMessages.INVALID_CREDENTIALS_ERROR),
        ],
        ids=["empty_username", "empty_password", "invalid_credentials"],
    )
    def test_negative_login_validations(
        self,
        login_page: LoginPage,
        username: str,
        password: str,
        expected_error: str,
    ) -> None:
        """Data-driven test verifying validation messages on incomplete or invalid credentials."""
        login_page.login(username=username, password=password)
        expect(login_page.error_banner).to_be_visible()
        expect(login_page.error_banner).to_have_text(expected_error)
