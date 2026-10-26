"""Centralized test data module for SauceDemo test suite.

Keeps tests free of magic strings and centralizes credentials, customer info,
product names, and expected assertions.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserCredentials:
    """Credentials model for authentication tests."""
    username: str
    password: str


@dataclass(frozen=True)
class CustomerInfo:
    """Shipping information model for checkout step one."""
    first_name: str
    last_name: str
    postal_code: str


class TestUsers:
    """Pre-configured SauceDemo test user accounts."""
    STANDARD_USER = UserCredentials(
        username="standard_user",
        password="secret_sauce",
    )
    LOCKED_OUT_USER = UserCredentials(
        username="locked_out_user",
        password="secret_sauce",
    )
    PROBLEM_USER = UserCredentials(
        username="problem_user",
        password="secret_sauce",
    )
    PERFORMANCE_GLITCH_USER = UserCredentials(
        username="performance_glitch_user",
        password="secret_sauce",
    )


class CustomerData:
    """Default shipping customer information."""
    DEFAULT_CUSTOMER = CustomerInfo(
        first_name="Cristian",
        last_name="Castro",
        postal_code="110111",
    )


class Products:
    """Standard inventory product names."""
    BACKPACK = "Sauce Labs Backpack"
    BIKE_LIGHT = "Sauce Labs Bike Light"
    BOLT_TSHIRT = "Sauce Labs Bolt T-Shirt"
    FLEECE_JACKET = "Sauce Labs Fleece Jacket"
    ONESIE = "Sauce Labs Onesie"

    E2E_SELECTED_PRODUCTS = [BACKPACK, BIKE_LIGHT]


class ExpectedMessages:
    """Exact copy and assertion strings expected in the UI."""
    LOCKED_OUT_ERROR = "Epic sadface: Sorry, this user has been locked out."
    USERNAME_REQUIRED_ERROR = "Epic sadface: Username is required"
    PASSWORD_REQUIRED_ERROR = "Epic sadface: Password is required"
    INVALID_CREDENTIALS_ERROR = "Epic sadface: Username and password do not match any user in this service"
    ORDER_COMPLETE_HEADER = "Thank you for your order!"
    ORDER_COMPLETE_TEXT = "Your order has been dispatched, and will arrive just as fast as the pony can get there!"


class SortOptions:
    """Inventory dropdown sorting options."""
    NAME_A_TO_Z = "az"
    NAME_Z_TO_A = "za"
    PRICE_LOW_TO_HIGH = "lohi"
    PRICE_HIGH_TO_LOW = "hilo"
