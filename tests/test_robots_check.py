"""Tests for src/robots_check.py with invented robots.txt texts, without network.

Fetching is tested with a fake urlopen that returns prepared answers.
The fixture no_network in conftest.py would stop any real request.
"""

import urllib.request
from http.client import IncompleteRead
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.robotparser import RobotFileParser

import pytest

import src.robots_check as robots_check
from src.config import load_site
from src.robots_check import (
    RobotsError,
    ensure_allowed,
    ensure_rfc9309_parser,
    fetch_rules,
    main,
    parse_rules,
)

FIXTURE_SITES = Path(__file__).parent / "fixtures" / "sites"
SITE = load_site("zz", FIXTURE_SITES)  # base_url https://example.org
ROBOTS_URL = "https://example.org/robots.txt"


def allowed(robots_txt: str, path: str) -> bool:
    return parse_rules(robots_txt).allows("https://example.org" + path)


# ---------------------------------------------------------------- rules (RFC 9309)

# pytest.param(..., id=...) gives each case a readable name in the test report.
RULE_CASES = [
    pytest.param("", "/hosts", True, id="empty file"),
    pytest.param("User-agent: *\nDisallow: /", "/hosts", False, id="disallow all"),
    pytest.param("User-agent: *\nDisallow:", "/hosts", True, id="empty disallow"),
    pytest.param("User-agent: OtherBot\nDisallow: /", "/hosts", True, id="other bot only"),
    pytest.param("User-agent: *\nDisallow: /", "/robots.txt", True, id="robots.txt itself"),
    pytest.param(
        "User-agent: *\nAllow: /\nDisallow: /private", "/private/page", False,
        id="longest rule wins over earlier allow",
    ),
    pytest.param(
        "User-agent: *\nAllow: /\nDisallow: /private", "/public", True, id="allow where no disallow"
    ),
    pytest.param(
        "User-agent: *\nDisallow: /\nAllow: /public", "/public/page", True,
        id="longest rule wins over earlier disallow",
    ),
    pytest.param(
        "User-agent: *\nDisallow: /*?filter=", "/hosts?filter=1", False, id="wildcard matches"
    ),
    pytest.param(
        "User-agent: *\nDisallow: /*?filter=", "/hosts", True, id="wildcard does not match"
    ),
    pytest.param("User-agent: *\nDisallow: /*.pdf$", "/files/plan.pdf", False, id="end anchor"),
    pytest.param(
        "User-agent: *\nDisallow: /*.pdf$", "/files/plan.pdf?page=2", True, id="end anchor, more text"
    ),
    pytest.param(
        "User-agent: *\nDisallow: /page\nAllow: /page", "/page", True, id="tie: allow wins"
    ),
    pytest.param(
        "user-agent: * # everyone\r\ndisallow: /x # not x\r\n", "/x/1", False,
        id="lower case, comments, CRLF",
    ),
    pytest.param(
        "User-agent: *\nDisallow: /a\n\nUser-agent: *\nDisallow: /b", "/b", False,
        id="groups for * are merged",
    ),
    pytest.param(
        "User-agent: OtherBot\nUser-agent: *\nDisallow: /x", "/x", False, id="group with two agents"
    ),
    pytest.param(
        "Disallow: /x\nUser-agent: *\nAllow: /", "/x", True, id="rules before user-agent ignored"
    ),
    pytest.param(
        "User-agent: *\nDisallow: /h%C3%B6fe", "/höfe", False, id="percent-encoding normalised"
    ),
]


@pytest.mark.parametrize(("robots_txt", "path", "expected"), RULE_CASES)
def test_rules_follow_rfc_9309(robots_txt, path, expected):
    assert allowed(robots_txt, path) is expected


def test_crawl_delay_is_read():
    rules = parse_rules("User-agent: *\nCrawl-delay: 15\nDisallow: /a")

    assert rules.crawl_delay == 15.0


@pytest.mark.parametrize(
    "robots_txt",
    ["", "User-agent: *\nDisallow: /a", "User-agent: OtherBot\nCrawl-delay: 30"],
)
def test_crawl_delay_is_none_without_rule_for_us(robots_txt):
    assert parse_rules(robots_txt).crawl_delay is None


def test_self_test_passes_on_this_python():
    ensure_rfc9309_parser()  # raises RobotsError if not


def test_self_test_stops_old_parser(monkeypatch):
    # Simulate an old robotparser that allows everything here.
    monkeypatch.setattr(RobotFileParser, "can_fetch", lambda self, agent, url: True)

    with pytest.raises(RobotsError, match="old way"):
        parse_rules("User-agent: *\nDisallow: /")


# ---------------------------------------------------------------- fetching


class FakeResponse:
    """Stands in for the answer of urlopen: url after redirects and the body."""

    def __init__(self, body: bytes, url: str = ROBOTS_URL):
        self.url = url
        self._body = body

    def read(self) -> bytes:
        return self._body

    # "with urlopen(...) as response" needs these two methods.
    def __enter__(self):
        return self

    def __exit__(self, *exception):
        return False


def use_fake_urlopen(monkeypatch, result):
    """Replace urlopen in src.robots_check; result is returned or raised. Returns the call log."""
    calls = []

    def fake_urlopen(url, timeout):
        calls.append((url, timeout))
        if isinstance(result, BaseException):
            raise result
        return result

    monkeypatch.setattr(robots_check, "urlopen", fake_urlopen)
    return calls


def http_error(code: int, url: str = ROBOTS_URL) -> HTTPError:
    return HTTPError(url, code, "status from fake server", None, None)


def test_fetch_reads_rules_once_with_timeout(monkeypatch):
    calls = use_fake_urlopen(monkeypatch, FakeResponse(b"User-agent: *\nDisallow: /private\n"))

    rules = fetch_rules(SITE)

    assert calls == [(ROBOTS_URL, 15)]
    assert rules.found is True
    assert rules.allows("https://example.org/hosts") is True
    assert rules.allows("https://example.org/private/page") is False


def test_fetch_accepts_bom(monkeypatch):
    use_fake_urlopen(monkeypatch, FakeResponse(b"\xef\xbb\xbfUser-agent: *\nDisallow: /\n"))

    assert fetch_rules(SITE).allows("https://example.org/hosts") is False


def test_fetch_accepts_redirect_on_same_host(monkeypatch):
    use_fake_urlopen(monkeypatch, FakeResponse(b"", url="https://example.org/robots.txt?v=2"))

    assert fetch_rules(SITE).found is True


@pytest.mark.parametrize("code", [404, 410])
def test_missing_robots_txt_means_no_rules(monkeypatch, code):
    use_fake_urlopen(monkeypatch, http_error(code))

    rules = fetch_rules(SITE)

    assert rules.found is False
    assert rules.allows("https://example.org/anything") is True


@pytest.mark.parametrize("code", [401, 403, 429])
def test_access_denied_stops(monkeypatch, code):
    use_fake_urlopen(monkeypatch, http_error(code))

    with pytest.raises(RobotsError, match=f"access denied or too many requests \\(status {code}\\)"):
        fetch_rules(SITE)


@pytest.mark.parametrize("code", [400, 500, 503])
def test_other_status_stops(monkeypatch, code):
    use_fake_urlopen(monkeypatch, http_error(code))

    with pytest.raises(RobotsError, match=f"unexpected status {code}"):
        fetch_rules(SITE)


@pytest.mark.parametrize(
    "error",
    [
        URLError("name not found"),
        TimeoutError("timed out"),
        ConnectionResetError("connection reset"),
        IncompleteRead(b""),
    ],
    ids=["URLError", "timeout", "connection reset", "incomplete answer"],
)
def test_network_problems_stop(monkeypatch, error):
    use_fake_urlopen(monkeypatch, error)

    with pytest.raises(RobotsError, match="could not be fetched"):
        fetch_rules(SITE)


@pytest.mark.parametrize(
    "body",
    [b"<!DOCTYPE html><html><body>App</body></html>", b"\n  <html></html>"],
    ids=["doctype", "leading whitespace"],
)
def test_html_page_instead_of_robots_txt_stops(monkeypatch, body):
    use_fake_urlopen(monkeypatch, FakeResponse(body))

    with pytest.raises(RobotsError, match="HTML page"):
        fetch_rules(SITE)


@pytest.mark.parametrize(
    "final_url",
    ["https://www.example.org/robots.txt", "http://example.org/robots.txt", "https://other.example/robots.txt"],
)
def test_redirect_to_other_address_stops(monkeypatch, final_url):
    use_fake_urlopen(monkeypatch, FakeResponse(b"User-agent: *\nAllow: /\n", url=final_url))

    with pytest.raises(RobotsError, match="redirected to another address"):
        fetch_rules(SITE)


def test_missing_robots_txt_on_other_host_stops(monkeypatch):
    use_fake_urlopen(monkeypatch, http_error(404, url="https://other.example/robots.txt"))

    with pytest.raises(RobotsError, match="redirected to another address"):
        fetch_rules(SITE)


def test_tests_cannot_reach_the_network():
    # Without the fake, the fixture no_network in conftest.py stops the request,
    # and fetch_rules must not hide that as an ordinary network problem.
    with pytest.raises(RuntimeError, match="must not access the network"):
        fetch_rules(SITE)
    with pytest.raises(RuntimeError, match="must not access the network"):
        urllib.request.urlopen(ROBOTS_URL, timeout=1)


# ---------------------------------------------------------------- ensure_allowed


def test_ensure_allowed_names_number_but_not_url():
    rules = parse_rules("User-agent: *\nDisallow: /private")
    urls = ["https://example.org/hosts", "https://example.org/private/farm-1001"]

    with pytest.raises(RobotsError) as error:
        ensure_allowed(rules, urls)

    assert str(error.value) == "URL 2 of 2 is disallowed by robots.txt"


def test_ensure_allowed_accepts_allowed_urls():
    rules = parse_rules("User-agent: *\nDisallow: /private")

    ensure_allowed(rules, ["https://example.org/hosts", "https://example.org/farms/1001"])


# ---------------------------------------------------------------- command line


def run_main(args: list[str]) -> list[str]:
    return ["zz", "--sites-dir", str(FIXTURE_SITES), *args]


def test_main_reports_without_urls(monkeypatch, capsys):
    use_fake_urlopen(monkeypatch, FakeResponse(b"User-agent: *\nCrawl-delay: 12\nDisallow: /private\n"))

    with pytest.raises(SystemExit) as error:
        main(run_main(["https://example.org/hosts", "https://example.org/private/farm-1001"]))

    assert error.value.code == 1  # one address disallowed
    output = capsys.readouterr().out
    assert "Site zz: robots.txt found" in output
    assert "start page   allowed" in output
    assert "URL 1        allowed" in output
    assert "URL 2        DISALLOWED" in output
    assert "crawl delay  12 seconds" in output
    assert "Result: 1 of 3 addresses disallowed" in output
    assert "example.org" not in output
    assert "private" not in output


def test_main_without_urls_checks_start_page(monkeypatch, capsys):
    use_fake_urlopen(monkeypatch, http_error(404))

    main(run_main([]))  # returns normally: exit code 0

    output = capsys.readouterr().out
    assert "no robots.txt (status 404 or 410), no rules apply" in output
    assert "crawl delay  none" in output
    assert "Result: 0 of 1 addresses disallowed" in output


def test_main_rejects_url_of_other_site_before_any_request(monkeypatch):
    calls = use_fake_urlopen(monkeypatch, FakeResponse(b""))

    with pytest.raises(SystemExit) as error:
        main(run_main(["https://example.org/hosts", "https://example.org.other.example/hosts"]))

    assert str(error.value.code).startswith("URL 2 does not belong to site zz")
    assert calls == []


def test_main_reports_robots_error(monkeypatch):
    use_fake_urlopen(monkeypatch, http_error(403))

    with pytest.raises(SystemExit) as error:
        main(run_main([]))

    assert str(error.value.code).startswith("Site zz: robots.txt: access denied")


def test_main_reports_configuration_error():
    with pytest.raises(SystemExit) as error:
        main(["DE", "--sites-dir", str(FIXTURE_SITES)])

    assert str(error.value.code).startswith("Configuration error: site id must look like")
