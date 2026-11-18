"""Explore a country site: save a few pages locally and write their skeletons.

Usage (only you, in your own PowerShell window with the virtual environment
active; see docs/07_bedienung.md, A.0):
    python -m src.explore_site --site de --data-dir ..\\wwoof-data <URL> [<URL> ...]

Claude Code runs it only on the practice site, without a window:
    python -m src.explore_site --sites-dir tests/fixtures/practice_sites --site xt
        --data-dir out/explore_test --headless <URL> [<URL> ...]

Guard rails (03_programmierprojekt.md, phase 2):
- at most 5 pages per run, fixed in the code;
- every URL must belong to the site; robots.txt is checked before the first page;
- one page after the other, with a random pause of 10-20 seconds between two
  page views (at least the crawl delay of robots.txt);
- stop instead of retrying: status 400 or higher, redirect to another site or
  another page, browser error, Ctrl+C;
- saved pages stay in the data folder; the terminal shows counters, file
  names and status only, never URLs.
"""

import argparse
import csv
import random
import sys
import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

from src.config import SITES_DIR, ConfigError, Site, check_data_dir, load_site, site_url_matches
from src.farm_table import CSV_DELIMITER, CSV_ENCODING
from src.page_skeleton import build_skeleton
from src.robots_check import RobotsError, ensure_allowed, fetch_rules
from src.session import PageResult, SessionError, load_page, open_browser

MAX_PAGES_PER_RUN = 5  # hard limit, deliberately not configurable
PAUSE_SECONDS = (10.0, 20.0)
INDEX_COLUMNS = ["file", "url", "status", "saved_at"]


class ExploreError(Exception):
    """The run cannot start or has to stop; the message contains no URL."""


# ---------------------------------------------------------------- checks before the run


def check_urls(site: Site, urls: list[str]) -> None:
    """Stop before any request if the URLs do not fit the rules."""
    if not urls:
        raise ExploreError("no URL given")
    if len(urls) > MAX_PAGES_PER_RUN:
        raise ExploreError(
            f"at most {MAX_PAGES_PER_RUN} pages per run (hard limit); {len(urls)} URLs given"
        )
    for number, url in enumerate(urls, start=1):
        if not site_url_matches(site, url):
            raise ExploreError(
                f"URL {number} does not belong to site {site.site_id}; "
                "it must start with the base_url of the country site file"
            )
        if url in urls[: number - 1]:
            raise ExploreError(f"URL {number} repeats URL {urls.index(url) + 1}")


def same_page(requested: str, final: str) -> bool:
    """True if final is the requested page: same host and path.

    A slash at the end, the query and the fragment are ignored, so that small
    changes by the web application do not count as a redirect.
    """
    a, b = urlsplit(requested), urlsplit(final)
    return a.netloc.lower() == b.netloc.lower() and a.path.rstrip("/") == b.path.rstrip("/")


def check_result(site: Site, url: str, result: PageResult) -> None:
    if result.status is None:
        raise ExploreError("no answer from the site")
    if result.status >= 400:
        raise ExploreError(f"status {result.status}")
    if not site_url_matches(site, result.final_url):
        raise ExploreError("redirected to another site (e.g. a login or captcha service)")
    if not same_page(url, result.final_url):
        raise ExploreError("redirected to another page (e.g. the login page); check the login and the URL")


# ---------------------------------------------------------------- pauses


class Pacer:
    """Keeps a random pause between two page views.

    The time since the last page view counts, e.g. the time you needed to
    log in. Clock, sleep and random numbers are passed in, so that tests
    can run without waiting.
    """

    def __init__(self, minimum: float, sleep: Callable[[float], None],
                 clock: Callable[[], float], rng: random.Random):
        self.minimum = minimum
        self.sleep = sleep
        self.clock = clock
        self.rng = rng
        self.last_page_view: float | None = None

    def wait(self) -> None:
        if self.last_page_view is None:
            return  # first page view of the run
        pause = max(self.rng.uniform(*PAUSE_SECONDS), self.minimum)
        remaining = pause - (self.clock() - self.last_page_view)
        if remaining > 0:
            print(f"Pause {remaining:.0f} s")
            self.sleep(remaining)

    def page_viewed(self) -> None:
        self.last_page_view = self.clock()


# ---------------------------------------------------------------- saving


def append_index(index_path: Path, row: list[str]) -> None:
    """Add a row to index.csv (local only: it contains URLs)."""
    is_new = not index_path.exists()
    # The BOM belongs only at the start of the file, so only a new file gets it.
    encoding = CSV_ENCODING if is_new else "utf-8"
    with open(index_path, "a", encoding=encoding, newline="") as file:
        writer = csv.writer(file, delimiter=CSV_DELIMITER)
        if is_new:
            writer.writerow(INDEX_COLUMNS)
        writer.writerow(row)


def save_page(samples_dir: Path, structure_dir: Path, name: str, html: str) -> int:
    """Write the page and its skeleton; never overwrite. Returns the skeleton's line count."""
    skeleton = build_skeleton(html)
    try:
        # mode "x": create a new file, fail if it exists already
        with open(samples_dir / f"{name}.html", "x", encoding="utf-8", newline="") as file:
            file.write(html)
        with open(structure_dir / f"{name}.txt", "x", encoding="utf-8", newline="") as file:
            file.write(skeleton.text)
    except FileExistsError:
        raise ExploreError(f"file {name} exists already; nothing overwritten") from None
    except OSError as error:
        raise ExploreError(f"could not write file {name} ({error.strerror})") from None
    return skeleton.lines


# ---------------------------------------------------------------- the run


def ask_for_login() -> None:
    print("The browser shows the start page. Log in by hand if needed.")
    try:
        input("Then press Enter here to continue (Ctrl+C stops): ")
    except EOFError:
        raise ExploreError("no input possible; start the run in your own PowerShell window") from None


def explore(
    site: Site,
    urls: list[str],
    data_dir: Path,
    fetch_page: Callable[[str], PageResult],
    *,
    minimum_pause: float = 0.0,
    login_prompt: Callable[[], None] | None = None,
    sleep: Callable[[float], None] | None = None,
    clock: Callable[[], float] | None = None,
    rng: random.Random | None = None,
    now: Callable[[], datetime] | None = None,
) -> int:
    """Visit the URLs one after the other and save each page. Returns the number saved.

    With login_prompt, the start page is opened first and login_prompt is
    called (you log in by hand); without it, the first URL is opened directly.
    sleep, clock, rng and now are only passed by tests.
    """
    # Defaults are looked up here, not in the parameter list: a default there
    # is fixed when Python reads the function, and tests could not replace it.
    sleep = sleep or time.sleep
    clock = clock or time.monotonic
    now = now or datetime.now
    samples_dir = data_dir / "local" / "samples" / site.site_id
    structure_dir = data_dir / "local" / "structure" / site.site_id
    samples_dir.mkdir(parents=True, exist_ok=True)
    structure_dir.mkdir(parents=True, exist_ok=True)

    pacer = Pacer(minimum_pause, sleep, clock, rng or random.Random())
    run_id = now().strftime("%Y%m%d-%H%M%S")
    total = len(urls)
    saved = 0
    try:
        if login_prompt is not None:
            start_page = site.base_url + "/"
            result = fetch_page(start_page)
            pacer.page_viewed()
            try:
                check_result(site, start_page, result)
            except ExploreError as error:
                raise ExploreError(f"start page: {error}") from None
            login_prompt()

        for number, url in enumerate(urls, start=1):
            pacer.wait()
            result = fetch_page(url)
            pacer.page_viewed()
            try:
                check_result(site, url, result)
            except ExploreError as error:
                raise ExploreError(f"page {number} of {total}: {error}") from None

            name = f"{run_id}-{number}"
            lines = save_page(samples_dir, structure_dir, name, result.html)
            append_index(
                samples_dir / "index.csv",
                [f"{name}.html", url, str(result.status), now().isoformat(timespec="seconds")],
            )
            saved += 1
            note = "" if result.network_idle else ", network busy (content may be incomplete)"
            print(f"Page {number} of {total}: status {result.status}, saved {name}.html, "
                  f"skeleton {lines} lines{note}")
    except KeyboardInterrupt:
        raise ExploreError(f"stopped by Ctrl+C after {saved} of {total} pages") from None
    except (ExploreError, SessionError) as error:
        raise ExploreError(f"stopped after {saved} of {total} pages: {error}") from None
    return saved


# ---------------------------------------------------------------- main


def stop(message: str) -> None:
    """End with message and exit code 1, after everything printed so far."""
    sys.stdout.flush()  # otherwise the message can appear before earlier lines
    sys.exit(message)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Save a few pages of a country site locally and write their skeletons."
    )
    parser.add_argument("--site", required=True, help="site id, e.g. de")
    parser.add_argument("--data-dir", required=True, type=Path, help="data folder, e.g. ..\\wwoof-data")
    parser.add_argument("urls", nargs="+", metavar="URL", help=f"1 to {MAX_PAGES_PER_RUN} addresses on the site")
    parser.add_argument("--sites-dir", type=Path, default=SITES_DIR, help="folder with the country site files")
    parser.add_argument(
        "--headless", action="store_true",
        help="no window, no login pause, no start page (test runs on the practice site only)",
    )
    args = parser.parse_args(argv)

    # Checks without any request
    try:
        site = load_site(args.site, args.sites_dir)
        check_urls(site, args.urls)
        data_dir = check_data_dir(args.data_dir)
    except (ConfigError, ExploreError) as error:
        stop(f"Not started: {error}")

    # robots.txt: one request, before the browser opens
    try:
        rules = fetch_rules(site)
        if not rules.allows(site.base_url + "/"):
            raise RobotsError("the start page is disallowed by robots.txt")
        ensure_allowed(rules, args.urls)  # numbers as in your command
    except RobotsError as error:
        stop(f"Not started: site {site.site_id}: {error}")
    delay = rules.crawl_delay
    print(f"Site {site.site_id}: robots.txt {'found' if rules.found else 'not present'}, "
          f"{len(args.urls)} addresses allowed, crawl delay {'none' if delay is None else f'{delay:g} s'}")

    profile_dir = data_dir / "browser_profile" / site.site_id
    try:
        profile_dir.mkdir(parents=True, exist_ok=True)
        with open_browser(profile_dir, headless=args.headless) as page:
            saved = explore(
                site, args.urls, data_dir, lambda url: load_page(page, url),
                minimum_pause=delay or 0.0,
                login_prompt=None if args.headless else ask_for_login,
            )
    except KeyboardInterrupt:
        stop("Run stopped by Ctrl+C")
    except ExploreError as error:  # already says "stopped after N of M pages"
        stop(f"Run {error}")
    except SessionError as error:  # browser could not start
        stop(f"Run stopped: {error}")
    except OSError as error:
        stop(f"Run stopped: could not create a folder in the data folder ({error.strerror})")

    print(f"Done: {saved} pages saved in {data_dir / 'local' / 'samples' / site.site_id}, "
          f"skeletons in {data_dir / 'local' / 'structure' / site.site_id}")


if __name__ == "__main__":
    main()
