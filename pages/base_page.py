"""BasePage module providing common layout interactions and page state."""

from playwright.sync_api import Page, Locator


class BasePage:
    """Base Page Object class containing common navigation and header elements.
    
    Adheres strictly to the Page Object Model design pattern:
    - Encapsulates locators and user actions.
    - Contains NO test assertions.
    """

    def __init__(self, page: Page) -> None:
        self.page = page

        # Header elements shared across authenticated pages
        self.header_title: Locator = page.locator('[data-test="title"]')
        self.cart_badge: Locator = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link: Locator = page.locator('[data-test="shopping-cart-link"]')
        self.menu_button: Locator = page.locator("#react-burger-menu-btn")
        self.logout_link: Locator = page.locator('[data-test="logout-sidebar-link"]')

    def navigate(self, path: str = "/") -> None:
        """Navigates to the relative application path."""
        self.page.goto(path)

    def open_cart(self) -> None:
        """Clicks the shopping cart icon from the header."""
        self.cart_link.click()

    def get_cart_count(self) -> int:
        """Returns the integer value of the shopping cart badge or 0 if not present."""
        if self.cart_badge.is_visible():
            text = self.cart_badge.inner_text().strip()
            return int(text) if text.isdigit() else 0
        return 0

    def get_header_title_text(self) -> str:
        """Retrieves the visible header title text (e.g., 'Products', 'Your Cart')."""
        return self.header_title.inner_text().strip()
