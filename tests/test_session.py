"""Tests for src/session.py that need no browser: error descriptions without URLs."""

import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.session import describe_browser_error

URL = "https://example.org/farms/1001"


@pytest.mark.parametrize(
    ("error", "description"),
    [
        (PlaywrightTimeoutError(f'Timeout 30000ms exceeded navigating to "{URL}"'),
         "page did not load within 30 seconds"),
        (PlaywrightError(f"net::ERR_NAME_NOT_RESOLVED at {URL}"),
         "browser error net::ERR_NAME_NOT_RESOLVED"),
        (PlaywrightError(f"Page.goto: Target page, context or browser has been closed\n  navigating to {URL}"),
         "browser window was closed"),
        (PlaywrightError("Failed to create a ProcessSingleton for your profile directory"),
         "browser profile is in use (is another run still open?)"),
        (PlaywrightError(f"Something unexpected while loading {URL}"),
         "browser error (Error)"),
    ],
)
def test_browser_errors_are_described_without_url(error, description):
    text = describe_browser_error(error)

    assert text == description
    assert "example.org" not in text
