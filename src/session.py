"""Start a real browser with a persistent profile and load pages (Playwright).

Each country site has its own profile folder (browser_profile/<site_id>/ in
the data folder); it keeps the login between runs. Used by the exploration
script (phase 2) and later by the collector (phase 3).

Error messages never contain URLs: Playwright's own messages do, and profile
URLs count as farm data (hard rule 5 in CLAUDE.md).
"""

import re
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# Fixed window size: pages may arrange their content differently on small
# screens, and the selectors of phase 3 should see the same layout.
VIEWPORT = {"width": 1366, "height": 900}
PAGE_TIMEOUT_MS = 30_000
# After loading, the web application keeps fetching content; wait at most
# this long until the network is quiet.
NETWORK_IDLE_TIMEOUT_MS = 10_000

NET_ERROR = re.compile(r"net::ERR_[A-Z_]+")


class SessionError(Exception):
    """The browser could not load a page; the message contains no URL."""


@dataclass(frozen=True)
class PageResult:
    status: int | None  # HTTP status of the page, None if there was no answer
    final_url: str  # address after redirects
    html: str  # the page as rendered by the browser
    network_idle: bool  # False: content may still have been loading


def describe_browser_error(error: Exception) -> str:
    """A short description of a Playwright error, without the URL it contains."""
    if isinstance(error, PlaywrightTimeoutError):
        return f"page did not load within {PAGE_TIMEOUT_MS // 1000} seconds"
    message = str(error)
    match = NET_ERROR.search(message)
    if match:
        return f"browser error {match[0]}"
    lowered = message.lower()
    if "has been closed" in lowered or "target closed" in lowered:
        return "browser window was closed"
    if "processsingleton" in lowered or "already in use" in lowered or "already running" in lowered:
        return "browser profile is in use (is another run still open?)"
    return f"browser error ({type(error).__name__})"


@contextmanager
def open_browser(profile_dir: Path, headless: bool) -> Iterator[Page]:
    """Open a browser with the profile in profile_dir and give one page (tab).

    Used with "with"; the browser is closed at the end in any case.
    """
    try:
        playwright = sync_playwright().start()
    except PlaywrightError as error:
        raise SessionError(describe_browser_error(error)) from None
    context = None
    try:
        try:
            context = playwright.chromium.launch_persistent_context(
                str(profile_dir), headless=headless, viewport=VIEWPORT
            )
        except PlaywrightError as error:
            raise SessionError(describe_browser_error(error)) from None
        page = context.pages[0] if context.pages else context.new_page()
        yield page
    finally:
        if context is not None:
            close_quietly(context.close)
        close_quietly(playwright.stop)


def close_quietly(close) -> None:
    """Call close(), ignoring errors.

    Closing can fail if the window was already closed or after Ctrl+C;
    that must not hide the actual reason for stopping.
    """
    try:
        close()
    except Exception:
        pass


def load_page(page: Page, url: str) -> PageResult:
    """Open url in the page, wait for its content and return it."""
    try:
        response = page.goto(url, wait_until="load", timeout=PAGE_TIMEOUT_MS)
        try:
            page.wait_for_load_state("networkidle", timeout=NETWORK_IDLE_TIMEOUT_MS)
            network_idle = True
        except PlaywrightTimeoutError:
            network_idle = False
        html = page.content()
        final_url = page.url
    except PlaywrightError as error:
        raise SessionError(describe_browser_error(error)) from None
    return PageResult(
        status=response.status if response is not None else None,
        final_url=final_url,
        html=html,
        network_idle=network_idle,
    )
