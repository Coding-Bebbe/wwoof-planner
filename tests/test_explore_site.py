"""Tests for src/explore_site.py without browser and without network.

Instead of a browser, a fake fetch_page returns prepared PageResult objects;
a fake clock and sleep make the pauses testable without waiting.
"""

import random
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import pytest

import src.config as config
import src.explore_site as explore_site
from src.config import load_site
from src.explore_site import ExploreError, check_urls, explore, main, same_page
from src.robots_check import parse_rules
from src.session import PageResult, SessionError

FIXTURE_SITES = Path(__file__).parent / "fixtures" / "sites"
SITE = load_site("zz", FIXTURE_SITES)  # base_url https://example.org
START = "https://example.org/"
URLS = [
    "https://example.org/hosts?region=testtal",
    "https://example.org/farms/1001",
    "https://example.org/farms/1002",
]
PAGE_HTML = '<html><head><title>Erika Mustermann</title></head><body><h1 class="name">Beispielhof</h1></body></html>'


def ok(url: str, html: str = PAGE_HTML) -> PageResult:
    return PageResult(status=200, final_url=url, html=html, network_idle=True)


class FakeClock:
    """Time that only moves when sleep() is called or advance() is used."""

    def __init__(self):
        self.now = 1000.0
        self.sleeps: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds

    def advance(self, seconds: float) -> None:
        self.now += seconds


class FakeBrowser:
    """Stands in for load_page: returns or raises what was prepared per URL."""

    def __init__(self, results: dict):
        self.results = results
        self.visited: list[str] = []

    def __call__(self, url: str) -> PageResult:
        self.visited.append(url)
        result = self.results.get(url) or ok(url)
        if isinstance(result, BaseException):
            raise result
        return result


def run(tmp_path, browser=None, clock=None, **options):
    clock = clock or FakeClock()
    browser = browser or FakeBrowser({})
    saved = explore(
        SITE, options.pop("urls", URLS), tmp_path, browser,
        sleep=clock.sleep, clock=clock, rng=random.Random(1),
        now=lambda: datetime(2026, 11, 19, 15, 30, 12), **options,
    )
    return saved, browser, clock


# ---------------------------------------------------------------- URL checks


def test_check_urls_accepts_up_to_five():
    check_urls(SITE, [f"https://example.org/farms/{n}" for n in range(5)])


@pytest.mark.parametrize(
    ("urls", "message"),
    [
        ([], "no URL given"),
        ([f"https://example.org/farms/{n}" for n in range(6)], r"at most 5 pages per run \(hard limit\); 6 URLs given"),
        (["https://example.org/a", "https://example.org.other.example/a"], "URL 2 does not belong to site zz"),
        (["http://example.org/a"], "URL 1 does not belong"),
        (["https://example.org/a", "https://example.org/b", "https://example.org/a"], "URL 3 repeats URL 1"),
    ],
)
def test_check_urls_rejects(urls, message):
    with pytest.raises(ExploreError, match=message):
        check_urls(SITE, urls)


@pytest.mark.parametrize(
    ("final", "expected"),
    [
        ("https://example.org/farms/1001", True),
        ("https://example.org/farms/1001/", True),
        ("https://example.org/farms/1001?tab=info#top", True),
        ("https://example.org/login", False),
        ("https://www.example.org/farms/1001", False),
    ],
)
def test_same_page(final, expected):
    assert same_page("https://example.org/farms/1001", final) is expected


# ---------------------------------------------------------------- a normal run


def test_run_saves_pages_skeletons_and_index(tmp_path, capsys):
    saved, browser, clock = run(tmp_path)

    assert saved == 3
    assert browser.visited == URLS  # without login prompt: no start page
    samples = tmp_path / "local" / "samples" / "zz"
    structure = tmp_path / "local" / "structure" / "zz"
    names = [f"20261119-153012-{n}" for n in (1, 2, 3)]
    for name in names:
        assert (samples / f"{name}.html").read_text(encoding="utf-8") == PAGE_HTML
        skeleton = (structure / f"{name}.txt").read_text(encoding="utf-8")
        assert "h1.name ⟨TEXT:11⟩" in skeleton
        assert "Erika" not in skeleton

    index = (samples / "index.csv").read_bytes()
    assert index.startswith(b"\xef\xbb\xbf")
    lines = index.decode("utf-8-sig").splitlines()
    assert lines[0] == "file;url;status;saved_at"
    assert lines[1] == f"{names[0]}.html;{URLS[0]};200;2026-11-19T15:30:12"
    assert len(lines) == 4


def test_output_contains_no_url(tmp_path, capsys):
    run(tmp_path)

    output = capsys.readouterr().out
    assert "Page 3 of 3: status 200, saved 20261119-153012-3.html, skeleton" in output
    assert "example" not in output
    assert "1001" not in output


def test_pauses_between_pages_are_10_to_20_seconds(tmp_path):
    _saved, _browser, clock = run(tmp_path)

    assert len(clock.sleeps) == 2  # before page 2 and 3, not before page 1
    assert all(10 <= seconds <= 20 for seconds in clock.sleeps)


def test_crawl_delay_raises_the_pause(tmp_path):
    _saved, _browser, clock = run(tmp_path, minimum_pause=25)

    assert clock.sleeps and all(seconds >= 25 for seconds in clock.sleeps)


def test_index_of_a_second_run_gets_no_second_bom(tmp_path):
    run(tmp_path)
    clock = FakeClock()
    explore(
        SITE, URLS[:1], tmp_path, FakeBrowser({}), sleep=clock.sleep, clock=clock,
        now=lambda: datetime(2026, 11, 19, 16, 0, 0),
    )

    index = (tmp_path / "local" / "samples" / "zz" / "index.csv").read_bytes()
    assert index.count(b"\xef\xbb\xbf") == 1
    assert len(index.decode("utf-8-sig").splitlines()) == 5


def test_existing_files_are_not_overwritten(tmp_path):
    run(tmp_path)

    with pytest.raises(ExploreError, match="stopped after 0 of 3 pages: file 20261119-153012-1 exists already"):
        run(tmp_path)


def test_network_busy_is_reported(tmp_path, capsys):
    busy = PageResult(status=200, final_url=URLS[0], html=PAGE_HTML, network_idle=False)

    run(tmp_path, browser=FakeBrowser({URLS[0]: busy}))

    assert "network busy" in capsys.readouterr().out


# ---------------------------------------------------------------- login prompt


def test_login_prompt_opens_start_page_first(tmp_path):
    calls = []

    saved, browser, _clock = run(tmp_path, login_prompt=lambda: calls.append("login"))

    assert saved == 3
    assert browser.visited == [START, *URLS]
    assert calls == ["login"]


def test_time_spent_logging_in_counts_as_pause(tmp_path):
    clock = FakeClock()

    _saved, _browser, clock = run(tmp_path, clock=clock, login_prompt=lambda: clock.advance(60))

    assert len(clock.sleeps) == 2  # no extra pause before page 1


def test_quick_enter_after_start_page_still_gets_a_pause(tmp_path):
    _saved, _browser, clock = run(tmp_path, login_prompt=lambda: None)

    assert len(clock.sleeps) == 3
    assert all(10 <= seconds <= 20 for seconds in clock.sleeps)


def test_failing_start_page_stops_before_login(tmp_path):
    calls = []
    browser = FakeBrowser({START: PageResult(403, START, "", True)})

    with pytest.raises(ExploreError, match="stopped after 0 of 3 pages: start page: status 403"):
        run(tmp_path, browser=browser, login_prompt=lambda: calls.append("login"))

    assert calls == []


# ---------------------------------------------------------------- stopping


@pytest.mark.parametrize(
    ("result", "message"),
    [
        (PageResult(404, URLS[1], "", True), "status 404"),
        (PageResult(None, URLS[1], "", True), "no answer from the site"),
        (PageResult(200, "https://login.other.example/", "", True), "redirected to another site"),
        (PageResult(200, "https://example.org/login?next=x", "", True), "redirected to another page"),
    ],
)
def test_bad_page_stops_and_keeps_earlier_pages(tmp_path, result, message):
    browser = FakeBrowser({URLS[1]: result})

    with pytest.raises(ExploreError) as error:
        run(tmp_path, browser=browser)

    text = str(error.value)
    assert text.startswith("stopped after 1 of 3 pages: page 2 of 3: ")
    assert message in text
    assert "1001" not in text and "example.org" not in text
    assert browser.visited == URLS[:2]  # no further page after the stop
    assert (tmp_path / "local" / "samples" / "zz" / "20261119-153012-1.html").exists()
    assert not (tmp_path / "local" / "samples" / "zz" / "20261119-153012-2.html").exists()


def test_browser_error_stops(tmp_path):
    browser = FakeBrowser({URLS[0]: SessionError("browser error net::ERR_NAME_NOT_RESOLVED")})

    with pytest.raises(ExploreError, match="stopped after 0 of 3 pages: browser error net::ERR_NAME_NOT_RESOLVED"):
        run(tmp_path, browser=browser)


def test_ctrl_c_stops_cleanly(tmp_path):
    browser = FakeBrowser({URLS[2]: KeyboardInterrupt()})

    with pytest.raises(ExploreError, match="stopped by Ctrl\\+C after 2 of 3 pages"):
        run(tmp_path, browser=browser)


# ---------------------------------------------------------------- main: nothing starts if a check fails


@pytest.fixture
def no_browser(monkeypatch):
    """Fail the test if main would open a browser or fetch robots.txt."""

    def forbidden(*args, **kwargs):
        raise AssertionError("must not be called")

    monkeypatch.setattr(explore_site, "open_browser", forbidden)
    monkeypatch.setattr(explore_site, "fetch_rules", forbidden)


def main_args(data_dir: Path, urls: list[str]) -> list[str]:
    return ["--site", "zz", "--sites-dir", str(FIXTURE_SITES), "--data-dir", str(data_dir), *urls]


def test_main_rejects_too_many_urls_before_any_request(tmp_path, no_browser):
    urls = [f"https://example.org/farms/{n}" for n in range(6)]

    with pytest.raises(SystemExit) as error:
        main(main_args(tmp_path, urls))

    assert str(error.value.code) == "Not started: at most 5 pages per run (hard limit); 6 URLs given"


def test_main_rejects_missing_data_dir(tmp_path, no_browser):
    with pytest.raises(SystemExit) as error:
        main(main_args(tmp_path / "wwoof-dta", URLS))

    assert "Not started:" in str(error.value.code)
    assert "data folder not found" in str(error.value.code)


def test_main_rejects_data_dir_inside_repository(no_browser):
    with pytest.raises(SystemExit) as error:
        main(main_args(config.REPOSITORY_DIR / "src", URLS))

    assert "must be outside the repository" in str(error.value.code)


def test_main_stops_before_browser_if_robots_txt_disallows(tmp_path, monkeypatch):
    monkeypatch.setattr(explore_site, "fetch_rules", lambda site: parse_rules("User-agent: *\nDisallow: /farms/"))
    monkeypatch.setattr(explore_site, "open_browser", lambda *a, **k: pytest.fail("browser opened"))

    with pytest.raises(SystemExit) as error:
        main(main_args(tmp_path, URLS))

    assert str(error.value.code) == "Not started: site zz: URL 2 of 3 is disallowed by robots.txt"


@pytest.fixture
def fake_run(monkeypatch):
    """Let main run with fake robots.txt, browser and pages; returns the prepared results."""
    results: dict = {}

    @contextmanager
    def fake_open_browser(profile_dir, headless):
        assert headless is True
        yield "fake page"

    monkeypatch.setattr(explore_site, "fetch_rules", lambda site: parse_rules(""))
    monkeypatch.setattr(explore_site, "open_browser", fake_open_browser)
    monkeypatch.setattr(explore_site, "load_page", lambda page, url: FakeBrowser(results)(url))
    monkeypatch.setattr(explore_site.time, "sleep", lambda seconds: None)
    return results


def test_main_runs_and_reports(tmp_path, fake_run, capsys):
    main([*main_args(tmp_path, URLS), "--headless"])

    output = capsys.readouterr().out
    assert "Site zz: robots.txt found, 3 addresses allowed, crawl delay none" in output
    assert "Done: 3 pages saved in" in output
    assert (tmp_path / "browser_profile" / "zz").is_dir()
    assert "example.org" not in output


def test_main_reports_stop(tmp_path, fake_run):
    fake_run[URLS[1]] = PageResult(404, URLS[1], "", True)

    with pytest.raises(SystemExit) as error:
        main([*main_args(tmp_path, URLS), "--headless"])

    assert str(error.value.code) == "Run stopped after 1 of 3 pages: page 2 of 3: status 404"


def test_main_stops_if_start_page_is_disallowed(tmp_path, monkeypatch):
    monkeypatch.setattr(explore_site, "fetch_rules", lambda site: parse_rules("User-agent: *\nDisallow: /$"))
    monkeypatch.setattr(explore_site, "open_browser", lambda *a, **k: pytest.fail("browser opened"))

    with pytest.raises(SystemExit) as error:
        main(main_args(tmp_path, URLS))

    assert str(error.value.code) == "Not started: site zz: the start page is disallowed by robots.txt"
