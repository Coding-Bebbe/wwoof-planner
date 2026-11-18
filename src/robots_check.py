"""Check the robots.txt of a country site before every run (guard rail 7).

Usage (from the repository folder; for a real country site only in your
own PowerShell window, never by Claude Code):
    python -m src.robots_check de [URL ...]
    python -m src.robots_check --sites-dir tests/fixtures/practice_sites xt

The check fetches <base_url>/robots.txt once and reports for the start page
and for every given URL whether the general rules (user agent "*") allow it.
Output contains the site id, numbers and status only, never URLs: profile
URLs count as farm data (hard rule 5 in CLAUDE.md).

The rules are evaluated by urllib.robotparser, which follows RFC 9309 in the
Python version used here (checked by ensure_rfc9309_parser). Fetching is done
here instead of RobotFileParser.read(), because read() has no timeout, turns
"access denied" and server errors silently into "everything disallowed",
reads an HTML page as "everything allowed" and follows redirects silently.
"""

import argparse
import sys
from dataclasses import dataclass
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from urllib.robotparser import RobotFileParser

from src.config import SITES_DIR, ConfigError, Site, load_site, site_url_matches

# Our scripts have no name of their own in robots.txt files,
# so the rules for all user agents ("*") apply.
USER_AGENT = "*"
TIMEOUT_SECONDS = 15
# RFC 9309: if there is no robots.txt, no rules apply.
NO_ROBOTS_STATUSES = (404, 410)
# Access denied or too many requests: stop instead of retrying (guard rail 8).
ACCESS_DENIED_STATUSES = (401, 403, 429)

# Self-test: three cases that an older robotparser (first matching rule wins,
# no wildcards) gets wrong. Invented rules on a reserved domain.
SELF_TEST_RULES = ["User-agent: *", "Allow: /", "Disallow: /private", "Disallow: /*?filter="]
SELF_TEST_CASES = (
    ("https://example.org/private/page", False),  # longest rule wins over "Allow: /"
    ("https://example.org/hosts?filter=1", False),  # wildcard * in the rule
    ("https://example.org/hosts", True),
)


class RobotsError(Exception):
    """robots.txt could not be checked or forbids the run; the message says why."""


@dataclass(frozen=True)
class RobotsRules:
    parser: RobotFileParser
    found: bool  # False: the site has no robots.txt (status 404 or 410), no rules apply

    def allows(self, url: str) -> bool:
        return self.parser.can_fetch(USER_AGENT, url)

    @property
    def crawl_delay(self) -> float | None:
        """Seconds to wait between two page views, if robots.txt asks for it."""
        delay = self.parser.crawl_delay(USER_AGENT)
        return None if delay is None else float(delay)


def ensure_rfc9309_parser() -> None:
    """Stop if this Python version still evaluates robots.txt the old way.

    It would then allow too much without any message. Python 3.13.15
    passes (checked on 18.11.2026).
    """
    parser = RobotFileParser()
    parser.parse(SELF_TEST_RULES)
    for url, expected in SELF_TEST_CASES:
        if parser.can_fetch(USER_AGENT, url) != expected:
            raise RobotsError(
                "this Python version evaluates robots.txt rules the old way "
                "(first matching rule, no wildcards); update Python (tested with 3.13.15)"
            )


def parse_rules(text: str, found: bool = True) -> RobotsRules:
    """Evaluate the text of a robots.txt file."""
    ensure_rfc9309_parser()
    parser = RobotFileParser()
    parser.parse(text.splitlines())
    return RobotsRules(parser=parser, found=found)


def robots_url(site: Site) -> str:
    # base_url never ends with a slash (checked in src/config.py)
    return site.base_url + "/robots.txt"


def check_same_site(site: Site, final_url: str) -> None:
    """Stop if fetching robots.txt ended on another host or without https."""
    if not site_url_matches(site, final_url):
        raise RobotsError(
            "robots.txt was redirected to another address; "
            "check base_url in the country site file"
        )


def fetch_rules(site: Site) -> RobotsRules:
    """Fetch and evaluate robots.txt of a country site. One request, no retry."""
    try:
        with urlopen(robots_url(site), timeout=TIMEOUT_SECONDS) as response:
            final_url = response.url  # after redirects
            body = response.read()
    except HTTPError as error:  # a status of 400 or higher; must come before URLError
        error.close()
        check_same_site(site, error.url)
        if error.code in NO_ROBOTS_STATUSES:
            return parse_rules("", found=False)
        if error.code in ACCESS_DENIED_STATUSES:
            raise RobotsError(
                f"robots.txt: access denied or too many requests (status {error.code}); "
                "do not retry now"
            ) from None
        raise RobotsError(f"robots.txt: unexpected status {error.code}") from None
    except (URLError, HTTPException, OSError) as error:
        # no connection, name not found, certificate error, timeout, broken answer
        reason = getattr(error, "reason", None) or error
        raise RobotsError(f"robots.txt could not be fetched ({reason})") from None

    check_same_site(site, final_url)
    # utf-8-sig removes a BOM; invalid bytes become a replacement character.
    text = body.decode("utf-8-sig", errors="replace")
    if text.lstrip().startswith("<"):
        # e.g. a web application that answers every address with its start page
        raise RobotsError("robots.txt is an HTML page, not a robots.txt file; check it by hand")
    return parse_rules(text)


def ensure_allowed(rules: RobotsRules, urls: list[str]) -> None:
    """Stop at the first URL that robots.txt disallows. The message names its number only."""
    for number, url in enumerate(urls, start=1):
        if not rules.allows(url):
            raise RobotsError(f"URL {number} of {len(urls)} is disallowed by robots.txt")


# ---------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Check the robots.txt of a country site.")
    parser.add_argument("site", help="site id, e.g. de")
    parser.add_argument(
        "urls", nargs="*", metavar="URL", help="addresses on this site to check (optional)"
    )
    parser.add_argument(
        "--sites-dir", type=Path, default=SITES_DIR,
        help="folder with the country site files (default: sites)",
    )
    args = parser.parse_args(argv)

    try:
        site = load_site(args.site, args.sites_dir)
    except ConfigError as error:
        sys.exit(f"Configuration error: {error}")

    # Check all URLs before the first request.
    for number, url in enumerate(args.urls, start=1):
        if not site_url_matches(site, url):
            sys.exit(
                f"URL {number} does not belong to site {site.site_id}; "
                "it must start with the base_url of the country site file"
            )

    try:
        rules = fetch_rules(site)
    except RobotsError as error:
        sys.exit(f"Site {site.site_id}: {error}")

    if rules.found:
        print(f"Site {site.site_id}: robots.txt found")
    else:
        print(f"Site {site.site_id}: no robots.txt (status 404 or 410), no rules apply")

    targets = [("start page", site.base_url + "/")]
    targets += [(f"URL {number}", url) for number, url in enumerate(args.urls, start=1)]
    disallowed = 0
    for label, url in targets:
        allowed = rules.allows(url)
        if not allowed:
            disallowed += 1
        print(f"  {label:<12} {'allowed' if allowed else 'DISALLOWED'}")

    delay = rules.crawl_delay
    print(f"  {'crawl delay':<12} {'none' if delay is None else f'{delay:g} seconds'}")
    print(f"Result: {disallowed} of {len(targets)} addresses disallowed")
    if disallowed:
        sys.exit(1)


if __name__ == "__main__":
    main()
