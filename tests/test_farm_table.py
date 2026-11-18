"""Tests for src/farm_table.py (phase 1 code) with the invented test table."""

from pathlib import Path

import pytest

from src.farm_table import (
    CSV_ENCODING,
    find_duplicate_profile_urls,
    parse_guestbook_count,
    read_farms,
    split_list,
)

# Path relative to this file, so the tests work from any working directory.
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "farms_sample.csv"


def test_read_farms_reads_all_rows_in_file_order():
    farms = read_farms(FIXTURE_PATH)

    codes = [farm["farm_code"] for farm in farms]
    assert codes == ["DE-VA-001", "DE-VA-002", "DE-SN-001", "DE-SN-002", "DE-VA-003"]


def test_read_farms_keeps_multiline_description():
    farms = read_farms(FIXTURE_PATH)

    assert "\n" in farms[0]["description"]


def test_read_farms_rejects_unexpected_columns(tmp_path):
    # tmp_path: an empty temporary folder that pytest creates for this test.
    path = tmp_path / "wrong_columns.csv"
    path.write_text("farm_code;farm_name\nDE-VA-001;Testhof\n", encoding=CSV_ENCODING)

    with pytest.raises(ValueError, match="Unexpected columns"):
        read_farms(path)


def test_read_farms_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_farms(tmp_path / "missing.csv")


# parametrize: the same test runs once for each pair of values.
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", []),
        ("Gemüsebau", ["Gemüsebau"]),
        ("Tierhaltung|Käseherstellung", ["Tierhaltung", "Käseherstellung"]),
    ],
)
def test_split_list(value, expected):
    assert split_list(value) == expected


@pytest.mark.parametrize(("value", "expected"), [("0", 0), ("12", 12), ("027", 27)])
def test_parse_guestbook_count_accepts_whole_numbers(value, expected):
    farm = {"farm_code": "DE-VA-001", "guestbook_count": value}

    assert parse_guestbook_count(farm) == expected


@pytest.mark.parametrize("value", ["", " 12", "12 ", "+12", "-1", "1_000", "²", "12.0", "zwölf"])
def test_parse_guestbook_count_rejects_other_values(value):
    farm = {"farm_code": "DE-VA-001", "guestbook_count": value}

    with pytest.raises(ValueError) as error:
        parse_guestbook_count(farm)

    message = str(error.value)
    assert "DE-VA-001" in message
    # The faulty value itself must not appear (hard rule 5: no farm data in messages).
    if value.strip():
        assert value.strip() not in message


def test_find_duplicate_profile_urls_in_fixture():
    farms = read_farms(FIXTURE_PATH)

    assert find_duplicate_profile_urls(farms) == [["DE-VA-001", "DE-VA-003"]]


def test_find_duplicate_profile_urls_without_duplicates():
    farms = [
        {"farm_code": "DE-VA-001", "profile_url": "https://example.org/farms/1"},
        {"farm_code": "DE-VA-002", "profile_url": "https://example.org/farms/2"},
    ]

    assert find_duplicate_profile_urls(farms) == []
