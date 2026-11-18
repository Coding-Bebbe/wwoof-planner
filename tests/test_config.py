"""Tests for src/config.py with invented country sites only.

Valid example files are in tests/fixtures/sites/. Invalid variants are
written as invented YAML text into tmp_path, a temporary folder per test.
No test reads the real files in sites/.
"""

from pathlib import Path

import pytest
import yaml

from src.config import ConfigError, Region, load_site, load_sites, main, site_url_matches

FIXTURE_SITES = Path(__file__).parent / "fixtures" / "sites"

# A minimal valid country site file (6 lines). Tests change one detail each.
VALID_SITE = """\
base_url: "https://example.org"
languages: ["de", "en"]
regions:
  testtal:
    code: "TT"
learning_categories: []
"""


def write_site(folder: Path, site_id: str, text: str) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{site_id}.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def load_text(tmp_path: Path, text: str):
    """Write text as the only country site zz and load it."""
    write_site(tmp_path, "zz", text)
    return load_site("zz", tmp_path)


# ---------------------------------------------------------------- valid files


def test_load_site_reads_fixture():
    site = load_site("zz", FIXTURE_SITES)

    assert site.site_id == "zz"
    assert site.base_url == "https://example.org"
    assert site.host == "example.org"
    assert site.languages == ("de", "en")
    assert site.regions == {
        "testtal": Region(key="testtal", code="TT"),
        "musterland": Region(key="musterland", code="ML"),
    }
    assert site.learning_categories == ("Gemüsebau", "Tierhaltung", "Käseherstellung")


def test_region_without_search_definition_is_accepted():
    # The regions of zz have a key and a code, but no search definition yet:
    # the state between choosing regions and the country check.
    site = load_site("zz", FIXTURE_SITES)

    assert site.regions["testtal"].code == "TT"


def test_load_sites_reads_every_file():
    assert sorted(load_sites(FIXTURE_SITES)) == ["xa", "zz"]


def test_empty_learning_categories_are_accepted():
    site = load_site("xa", FIXTURE_SITES)

    assert site.learning_categories == ()


def test_region_key_with_digits_and_underscore_is_accepted(tmp_path):
    text = VALID_SITE.replace("testtal:", "baden_wuerttemberg2:")

    assert "baden_wuerttemberg2" in load_text(tmp_path, text).regions


def test_file_with_bom_is_accepted(tmp_path):
    # Some Windows editors write a BOM at the start of UTF-8 files.
    (tmp_path / "zz.yaml").write_text(VALID_SITE, encoding="utf-8-sig")

    assert load_site("zz", tmp_path).base_url == "https://example.org"


# ---------------------------------------------------------------- YAML traps


def test_pyyaml_reads_unquoted_no_as_false():
    # Evidence for the rule "codes always in quotes" (Norway: site id "no").
    assert yaml.safe_load("site: no") == {"site": False}
    assert yaml.safe_load('site: "no"') == {"site": "no"}


def test_unquoted_no_as_site_is_rejected_with_hint():
    site = yaml.safe_load("site: no")["site"]

    with pytest.raises(ConfigError, match="site id is false, not text; put codes in quotes"):
        load_site(site, FIXTURE_SITES)


def test_pyyaml_keeps_last_value_of_duplicate_key():
    # Evidence for the note of 17.11.2026: plain PyYAML does not complain.
    assert yaml.safe_load("a: 1\na: 2") == {"a": 2}


def test_duplicate_key_is_rejected_with_line(tmp_path):
    text = VALID_SITE + 'base_url: "https://example.com"\n'

    with pytest.raises(ConfigError, match=r"zz\.yaml: duplicate key 'base_url' \(line 7\)"):
        load_text(tmp_path, text)


def test_duplicate_region_key_is_rejected(tmp_path):
    text = VALID_SITE.replace(
        '  testtal:\n    code: "TT"\n',
        '  testtal:\n    code: "TT"\n  testtal:\n    code: "TU"\n',
    )

    with pytest.raises(ConfigError, match=r"duplicate key 'testtal' \(line 6\)"):
        load_text(tmp_path, text)


def test_yaml_syntax_error_is_reported_with_line(tmp_path):
    text = VALID_SITE.replace('"TT"', '"TT')  # quote not closed

    with pytest.raises(ConfigError, match=r"zz\.yaml: invalid YAML: .*\(line \d+\)"):
        load_text(tmp_path, text)


def test_empty_file_is_rejected(tmp_path):
    with pytest.raises(ConfigError, match="file is empty"):
        load_text(tmp_path, "")


def test_list_at_top_level_is_rejected(tmp_path):
    with pytest.raises(ConfigError, match="at the top level"):
        load_text(tmp_path, "- base_url\n- languages\n")


# ---------------------------------------------------------------- site id and files


@pytest.mark.parametrize("site", ["DE", "deu", "d", "", "d1", "d-", 49, None])
def test_invalid_site_ids_are_rejected(site):
    with pytest.raises(ConfigError, match="site id"):
        load_site(site, FIXTURE_SITES)


def test_missing_site_file_is_rejected():
    with pytest.raises(ConfigError, match=r"yy\.yaml: file not found"):
        load_site("yy", FIXTURE_SITES)


def test_missing_sites_folder_is_rejected(tmp_path):
    with pytest.raises(ConfigError, match="folder not found"):
        load_site("zz", tmp_path / "missing")


def test_file_name_that_is_no_site_id_is_rejected(tmp_path):
    write_site(tmp_path, "zz", VALID_SITE)
    write_site(tmp_path, "germany", VALID_SITE.replace("testtal", "musterland"))

    with pytest.raises(ConfigError, match=r"germany\.yaml: the file name must be a site id"):
        load_site("zz", tmp_path)


def test_broken_file_of_another_site_is_reported(tmp_path):
    # All files are checked on every call (region keys must be unique).
    write_site(tmp_path, "zz", VALID_SITE)
    write_site(tmp_path, "xa", "")

    with pytest.raises(ConfigError, match=r"xa\.yaml: file is empty"):
        load_site("zz", tmp_path)


# ---------------------------------------------------------------- keys


def test_unknown_top_level_key_is_rejected(tmp_path):
    text = VALID_SITE + "max_profiles_per_run: 30\n"  # belongs to config.yaml, not here

    with pytest.raises(ConfigError, match="unknown key 'max_profiles_per_run' in the top level"):
        load_text(tmp_path, text)


def test_missing_top_level_key_is_rejected(tmp_path):
    text = VALID_SITE.replace("learning_categories: []\n", "")

    with pytest.raises(ConfigError, match="missing key 'learning_categories'"):
        load_text(tmp_path, text)


def test_unknown_region_key_is_rejected(tmp_path):
    text = VALID_SITE.replace('    code: "TT"\n', '    code: "TT"\n    serach: "x"\n')

    with pytest.raises(ConfigError, match="unknown key 'serach' in regions.testtal; allowed: code"):
        load_text(tmp_path, text)


def test_region_without_code_is_rejected(tmp_path):
    text = VALID_SITE.replace('    code: "TT"\n', "")

    with pytest.raises(ConfigError, match=r'regions\.testtal must contain code: "XY"'):
        load_text(tmp_path, text)


# ---------------------------------------------------------------- base_url


@pytest.mark.parametrize(
    "base_url",
    [
        '"http://example.org"',
        '"https://example.org/"',
        '"https://example.org/de"',
        '"https://example.org:8443"',
        '"https://Example.org"',
        '"example.org"',
        '"https://user@example.org"',
        '"https://example.org?x=1"',
        '"https://example.org#top"',
        '"https://exa mple.org"',
        '"https://localhost"',
        "42",
    ],
)
def test_invalid_base_url_is_rejected(tmp_path, base_url):
    text = VALID_SITE.replace('"https://example.org"', base_url)

    with pytest.raises(ConfigError, match="base_url must be"):
        load_text(tmp_path, text)


# ---------------------------------------------------------------- languages


@pytest.mark.parametrize(
    ("languages", "message"),
    [
        ("[no]", "is false, not text; put codes in quotes"),
        ('["DE"]', "must look like"),
        ('["deu"]', "must look like"),
        ("[]", "non-empty list"),
        ('"de"', "non-empty list"),
        ('["de", "de"]', "de appears twice"),
    ],
)
def test_invalid_languages_are_rejected(tmp_path, languages, message):
    text = VALID_SITE.replace('["de", "en"]', languages)

    with pytest.raises(ConfigError, match=message):
        load_text(tmp_path, text)


# ---------------------------------------------------------------- regions


@pytest.mark.parametrize(
    ("code", "message"),
    [
        ("NO", "regions.testtal.code is false, not text; put codes in quotes"),
        ('"tt"', "must look like"),
        ('"T"', "must look like"),
        ('"TTTT"', "must look like"),
        ('"T1"', "must look like"),
        ("12", "must be text"),
    ],
)
def test_invalid_region_codes_are_rejected(tmp_path, code, message):
    text = VALID_SITE.replace('"TT"', code)

    with pytest.raises(ConfigError, match=message):
        load_text(tmp_path, text)


@pytest.mark.parametrize(
    ("key", "message"),
    [
        ("no", "a region key is false, not text; put codes in quotes"),
        ("Testtal", "region key 'Testtal' must look like"),
        ('"test tal"', "region key 'test tal' must look like"),
        ("testtäl", "region key 'testtäl' must look like"),
        ("1testtal", "region key '1testtal' must look like"),
    ],
)
def test_invalid_region_keys_are_rejected(tmp_path, key, message):
    text = VALID_SITE.replace("testtal:", f"{key}:")

    with pytest.raises(ConfigError, match=message):
        load_text(tmp_path, text)


@pytest.mark.parametrize("regions", ["regions: {}\n", "regions:\n"])
def test_site_without_regions_is_rejected(tmp_path, regions):
    text = VALID_SITE.replace('regions:\n  testtal:\n    code: "TT"\n', regions)

    with pytest.raises(ConfigError, match="at least one region"):
        load_text(tmp_path, text)


def test_region_code_used_twice_in_one_site_is_rejected(tmp_path):
    text = VALID_SITE.replace(
        '  testtal:\n    code: "TT"\n',
        '  testtal:\n    code: "TT"\n  musterland:\n    code: "TT"\n',
    )

    with pytest.raises(ConfigError, match="region code TT is used by testtal and musterland"):
        load_text(tmp_path, text)


def test_same_region_code_in_two_sites_is_accepted(tmp_path):
    # Codes only need to be unique within a site: the farm code starts with the site id.
    write_site(tmp_path, "zz", VALID_SITE)
    write_site(tmp_path, "xa", VALID_SITE.replace("testtal", "musterland"))

    assert load_site("xa", tmp_path).regions["musterland"].code == "TT"


def test_region_key_in_two_sites_is_rejected(tmp_path):
    write_site(tmp_path, "zz", VALID_SITE)
    write_site(tmp_path, "xa", VALID_SITE.replace('"TT"', '"XT"'))

    with pytest.raises(ConfigError) as error:
        load_site("zz", tmp_path)

    message = str(error.value)
    assert "region key testtal appears in" in message
    assert "xa.yaml" in message
    assert "zz.yaml" in message


# ---------------------------------------------------------------- learning categories


@pytest.mark.parametrize(
    ("categories", "message"),
    [
        ('["Obst|Gemüse"]', r"contains '\|', the list separator"),
        ('["Obst", "Obst"]', "entry 2, appears twice"),
        ("[no]", "is false, not text; put codes in quotes"),
        ("[42]", "must be text"),
        ('[""]', "is empty"),
        ('[" Obst"]', "spaces at the start or end"),
        ('"Obst"', "must be a list"),
    ],
)
def test_invalid_learning_categories_are_rejected(tmp_path, categories, message):
    text = VALID_SITE.replace("learning_categories: []", f"learning_categories: {categories}")

    with pytest.raises(ConfigError, match=message):
        load_text(tmp_path, text)


# ---------------------------------------------------------------- site_url_matches


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://example.org", True),
        ("https://example.org/", True),
        ("https://example.org/hosts?region=testtal", True),
        ("https://EXAMPLE.org/hosts", True),
        ("http://example.org/hosts", False),
        ("https://www.example.org/hosts", False),
        ("https://example.org.other.example/hosts", False),
        ("https://example.org@other.example/hosts", False),
        ("https://other.example/https://example.org", False),
        ("https://example.org:8443/hosts", False),
        ("example.org/hosts", False),
        ("https://[example.org/hosts", False),
        ("", False),
    ],
)
def test_site_url_matches(url, expected):
    site = load_site("zz", FIXTURE_SITES)

    assert site_url_matches(site, url) is expected


# ---------------------------------------------------------------- command line


def test_main_prints_summary(capsys):
    # capsys captures what the code prints.
    main(["zz", "--sites-dir", str(FIXTURE_SITES)])

    output = capsys.readouterr().out
    assert "zz.yaml: ok" in output
    assert "testtal (TT), musterland (ML)" in output
    assert "learning categories  3" in output


def test_main_exits_with_message_on_error():
    # sys.exit("text") raises SystemExit; Python prints the text and exits with code 1.
    with pytest.raises(SystemExit) as error:
        main(["yy", "--sites-dir", str(FIXTURE_SITES)])

    assert str(error.value.code).startswith("Configuration error: ")
    assert "yy.yaml: file not found" in str(error.value.code)
