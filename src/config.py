"""Load and check the country site files (sites/<site_id>.yaml).

A country site file holds only country data (03_programmierprojekt.md,
section 5.4). config.yaml with limits, pauses and paths follows in phase 3.

Usage (from the repository folder):
    python -m src.config de
    python -m src.config --sites-dir tests/fixtures/sites zz

Every call checks all files in the sites folder, because region keys must
be unique across all country sites. Messages name files, keys and codes,
never farm data.
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

import yaml

from src.farm_table import LIST_SEPARATOR

SITES_DIR = Path("sites")

# Keys allowed in a country site file and in each region. All are required.
SITE_KEYS = ("base_url", "languages", "regions", "learning_categories")
REGION_KEYS = ("code",)  # "search" follows once its format is known (phase 2, step 2.4)

# fullmatch() is used with these patterns: the whole value must match.
SITE_ID_PATTERN = re.compile(r"[a-z]{2}")
LANGUAGE_PATTERN = re.compile(r"[a-z]{2}")
REGION_KEY_PATTERN = re.compile(r"[a-z][a-z0-9_]*")
REGION_CODE_PATTERN = re.compile(r"[A-Z]{2,3}")
# "https://" plus a host name in lower case with at least one dot. This also
# rules out a path, a slash at the end, a port, a user name, "?" and "#".
BASE_URL_PATTERN = re.compile(r"https://[a-z0-9-]+(\.[a-z0-9-]+)+")

QUOTE_HINT = "put codes in quotes; YAML reads unquoted no, yes, on and off as false or true"


class ConfigError(Exception):
    """A configuration file is missing or invalid; the message says where and why."""


# frozen=True: the objects cannot be changed after they have been checked.
@dataclass(frozen=True)
class Region:
    key: str  # region key, e.g. "voralpenland"
    code: str  # region code in the farm code, e.g. "VA"


@dataclass(frozen=True)
class Site:
    site_id: str  # e.g. "de"; upper case it is the country part of the farm code
    base_url: str  # e.g. "https://example.org", without slash at the end
    languages: tuple[str, ...]
    regions: dict[str, Region]
    learning_categories: tuple[str, ...]

    @property
    def host(self) -> str:
        return self.base_url.removeprefix("https://")


# ---------------------------------------------------------------- reading YAML


class DuplicateKeyError(yaml.MarkedYAMLError):
    """A key appears twice in the same mapping."""


class StrictLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate keys.

    Plain PyYAML silently keeps the last value of a duplicate key
    (shown in tests/test_config.py), so a typo could go unnoticed.
    """


def construct_mapping_without_duplicates(loader, node, deep=False):
    loader.flatten_mapping(node)  # resolve YAML merge keys (<<) first
    seen = set()
    for key_node, _value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            is_duplicate = key in seen
        except TypeError:  # unhashable key; construct_mapping reports it
            continue
        if is_duplicate:
            raise DuplicateKeyError(None, None, f"duplicate key '{key}'", key_node.start_mark)
        seen.add(key)
    return loader.construct_mapping(node, deep=deep)


StrictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping_without_duplicates
)


def read_yaml(path: Path) -> object:
    """Read a YAML file with StrictLoader. Errors become ConfigError."""
    try:
        # utf-8-sig also accepts a BOM, which some Windows editors write
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        raise ConfigError(f"{path}: file not found") from None
    except UnicodeDecodeError:
        raise ConfigError(f"{path}: not UTF-8 text") from None
    except OSError as error:
        raise ConfigError(f"{path}: could not be read ({error.strerror})") from None

    try:
        return yaml.load(text, Loader=StrictLoader)
    except yaml.YAMLError as error:
        # from None: show only our message, not the chain of internal errors
        raise ConfigError(f"{path}: {describe_yaml_error(error)}") from None


def describe_yaml_error(error: yaml.YAMLError) -> str:
    problem = getattr(error, "problem", None) or str(error)
    mark = getattr(error, "problem_mark", None)
    where = f" (line {mark.line + 1})" if mark is not None else ""
    if isinstance(error, DuplicateKeyError):
        return f"{problem}{where}"
    return f"invalid YAML: {problem}{where}"


# ---------------------------------------------------------------- checking values


def require_text(value: object, what: str) -> str:
    """Return value if it is a string. YAML true/false get a hint about quotes."""
    if isinstance(value, bool):
        raise ConfigError(f"{what} is {str(value).lower()}, not text; {QUOTE_HINT}")
    if not isinstance(value, str):
        raise ConfigError(f"{what} must be text")
    return value


def check_code(value: object, pattern: re.Pattern, what: str, example: str) -> str:
    code = require_text(value, what)
    if not pattern.fullmatch(code):
        raise ConfigError(f"{what} must look like {example}")
    return code


def check_site_id(site: object) -> str:
    """Return the site id if it consists of exactly two lower-case letters.

    Checked before any file is opened: Windows would open sites/de.yaml for
    "DE" as well, Linux (GitHub Actions) would not.
    """
    return check_code(site, SITE_ID_PATTERN, "site id", '"de" (two lower-case letters)')


def check_keys(mapping: dict, allowed: tuple[str, ...], where: str) -> None:
    for key in mapping:
        if key not in allowed:
            raise ConfigError(f"unknown key '{key}' in {where}; allowed: {', '.join(allowed)}")
    for key in allowed:
        if key not in mapping:
            raise ConfigError(f"missing key '{key}' in {where}")


def check_base_url(value: object) -> str:
    base_url = require_text(value, "base_url")
    if not BASE_URL_PATTERN.fullmatch(base_url):
        raise ConfigError(
            'base_url must be "https://" plus the host name in lower case, '
            'without path, port or slash at the end, e.g. "https://example.org"'
        )
    return base_url


def check_languages(value: object) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ConfigError('languages must be a non-empty list, e.g. ["de", "en"]')
    languages: list[str] = []
    for number, item in enumerate(value, start=1):
        code = check_code(
            item, LANGUAGE_PATTERN, f"languages, entry {number},", '"de" (two lower-case letters)'
        )
        if code in languages:
            raise ConfigError(f"languages: {code} appears twice")
        languages.append(code)
    return tuple(languages)


def check_regions(value: object) -> dict[str, Region]:
    if not isinstance(value, dict) or not value:
        raise ConfigError("regions must contain at least one region key with a code")
    regions: dict[str, Region] = {}
    keys_by_code: dict[str, str] = {}
    for key, settings in value.items():
        what = f"region key '{key}'" if isinstance(key, str) else "a region key"
        check_code(key, REGION_KEY_PATTERN, what, '"voralpenland" (a-z, 0-9 and _, starting with a letter)')
        where = f"regions.{key}"
        if not isinstance(settings, dict):
            raise ConfigError(f'{where} must contain code: "XY"')
        check_keys(settings, REGION_KEYS, where)
        code = check_code(
            settings["code"], REGION_CODE_PATTERN, f"{where}.code", '"VA" (two or three capital letters)'
        )
        if code in keys_by_code:
            raise ConfigError(f"region code {code} is used by {keys_by_code[code]} and {key}")
        keys_by_code[code] = key
        regions[key] = Region(key=key, code=code)
    return regions


def check_learning_categories(value: object) -> tuple[str, ...]:
    # May be empty until the country check; the export self-test requires it (phase 4).
    if not isinstance(value, list):
        raise ConfigError("learning_categories must be a list; it may be empty: []")
    categories: list[str] = []
    for number, item in enumerate(value, start=1):
        where = f"learning_categories, entry {number},"
        category = require_text(item, where)
        if not category.strip():
            raise ConfigError(f"{where} is empty")
        if category != category.strip():
            raise ConfigError(f"{where} has spaces at the start or end")
        if LIST_SEPARATOR in category:
            # The CSV files separate list entries with this character.
            raise ConfigError(f"{where} contains '{LIST_SEPARATOR}', the list separator of the CSV files")
        if category in categories:
            raise ConfigError(f"{where} appears twice")
        categories.append(category)
    return tuple(categories)


def parse_site(site_id: str, data: object, path: Path) -> Site:
    """Check the content of one country site file and return it as a Site."""
    try:
        if data is None:
            raise ConfigError("file is empty")
        if not isinstance(data, dict):
            raise ConfigError("expected keys such as base_url: at the top level")
        check_keys(data, SITE_KEYS, "the top level")
        return Site(
            site_id=site_id,
            base_url=check_base_url(data["base_url"]),
            languages=check_languages(data["languages"]),
            regions=check_regions(data["regions"]),
            learning_categories=check_learning_categories(data["learning_categories"]),
        )
    except ConfigError as error:
        raise ConfigError(f"{path}: {error}") from None


# ---------------------------------------------------------------- loading sites


def load_sites(sites_dir: Path = SITES_DIR) -> dict[str, Site]:
    """Load and check every country site file in sites_dir."""
    if not sites_dir.is_dir():
        raise ConfigError(f"{sites_dir}: folder not found")

    sites: dict[str, Site] = {}
    paths: dict[str, Path] = {}
    # case_sensitive=False: the same files on Windows and Linux
    for path in sorted(sites_dir.glob("*.yaml", case_sensitive=False)):
        site_id = path.stem
        if not SITE_ID_PATTERN.fullmatch(site_id):
            raise ConfigError(f"{path}: the file name must be a site id in lower case, e.g. de.yaml")
        sites[site_id] = parse_site(site_id, read_yaml(path), path)
        paths[site_id] = path

    # Region keys must be unique across all sites: the column region in
    # farms.csv contains no country.
    site_by_region: dict[str, str] = {}
    for site in sites.values():
        for key in site.regions:
            if key in site_by_region:
                first = paths[site_by_region[key]]
                raise ConfigError(
                    f"region key {key} appears in {first} and {paths[site.site_id]}; "
                    "region keys must be unique across all country sites"
                )
            site_by_region[key] = site.site_id
    return sites


def load_site(site: object, sites_dir: Path = SITES_DIR) -> Site:
    """Check all country site files and return the one for the given site id."""
    site_id = check_site_id(site)
    sites = load_sites(sites_dir)
    if site_id not in sites:
        raise ConfigError(f"{sites_dir / (site_id + '.yaml')}: file not found (site id {site_id})")
    return sites[site_id]


def site_url_matches(site: Site, url: str) -> bool:
    """True if url is an https address on the host of the site's base_url.

    Compares the whole host instead of the beginning of the text, so that
    https://example.org.other.example/ or https://example.org@other.example/
    do not count as addresses of https://example.org.
    """
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    return parts.scheme == "https" and parts.netloc.lower() == site.host


# ---------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Check the country site files and show one of them.")
    parser.add_argument("site", help="site id, e.g. de")
    parser.add_argument(
        "--sites-dir", type=Path, default=SITES_DIR,
        help="folder with the country site files (default: sites)",
    )
    args = parser.parse_args(argv)  # argv=None: use the command line

    try:
        site = load_site(args.site, args.sites_dir)
    except ConfigError as error:
        sys.exit(f"Configuration error: {error}")

    regions = ", ".join(f"{region.key} ({region.code})" for region in site.regions.values())
    print(f"{args.sites_dir / (site.site_id + '.yaml')}: ok")
    print(f"  base_url             {site.base_url}")
    print(f"  languages            {', '.join(site.languages)}")
    print(f"  regions              {regions}")
    print(f"  learning categories  {len(site.learning_categories)}")


if __name__ == "__main__":
    main()
