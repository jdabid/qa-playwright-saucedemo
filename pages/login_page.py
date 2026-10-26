"""LoginPage module encapsulating authentication elements and actions."""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for the SauceDemo Login Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Form locators using reliable data-test attributes
        self.username_input: Locator = page.locator('[data-test="username"]')
        self.password_input: Locator = page.locator('[data-test="password"]')
        self.login_button: Locator = page.locator('[data-test="login-button"]')
        self.error_banner: Locator = page.locator('[data-test="error"]')

    def navigate(self, path: str = "/") -> None:
        """Navigates to the login page."""
        super().navigate(path)

    def fill_username(self, username: str) -> None:
        """Fills the username input field."""
        self.username_input.fill(username)

    def fill_password(self, password: str) -> None:
        """Fills the password input field."""
        self.password_input.fill(password)

    def click_login(self) -> None:
        """Clicks the submit login button."""
        self.login_button.click()

    def login(self, username: str, password: str) -> None:
        """Performs a full login attempt with provided credentials."""
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Returns the text from the login error banner."""
        return self.error_banner.inner_text().strip()
