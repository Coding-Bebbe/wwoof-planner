"""Phase 1: check whether a spreadsheet program keeps the CSV format.

Usage (from the repository folder):
    python -m src.table_roundtrip prepare
        Copy the invented test table to out/roundtrip/ (two identical files).
        Open farms_edit.csv in Excel or LibreOffice, make the expected change
        (see EXPECTED_CHANGE) and save.
    python -m src.table_roundtrip compare
        Compare the saved file with the untouched copy.

Output contains farm codes, column names, numbers and status only, never
field values (hard rule 5 in CLAUDE.md), even though the test data is invented.
"""

import argparse
import shutil
import sys
from pathlib import Path

from src.farm_table import CSV_DELIMITER, FARM_COLUMNS, read_farms

FIXTURE_PATH = Path("tests/fixtures/farms_sample.csv")
ROUNDTRIP_DIR = Path("out") / "roundtrip"
ORIGINAL_PATH = ROUNDTRIP_DIR / "farms_original.csv"
EDIT_PATH = ROUNDTRIP_DIR / "farms_edit.csv"

UTF8_BOM = b"\xef\xbb\xbf"

# The one change the user makes in the spreadsheet program:
# (farm_code, column, old value, new value)
EXPECTED_CHANGE = ("DE-SN-002", "guestbook_count", "3", "4")


class RoundTripError(Exception):
    """A file could not be read or compared; the message says why."""


# ---------------------------------------------------------------- prepare


def prepare() -> None:
    """Copy the fixture byte for byte into out/roundtrip/."""
    try:
        ROUNDTRIP_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURE_PATH, ORIGINAL_PATH)
        shutil.copyfile(FIXTURE_PATH, EDIT_PATH)
    except FileNotFoundError:
        raise RoundTripError(f"File not found: {FIXTURE_PATH}")
    except OSError as error:
        # e.g. PermissionError while the file is still open in Excel
        raise RoundTripError(f"Could not copy into {ROUNDTRIP_DIR}: {error}")

    code, column, old, new = EXPECTED_CHANGE
    print(f"Copied {FIXTURE_PATH} to {ORIGINAL_PATH} and {EDIT_PATH}")
    print()
    print("Next:")
    print(f"  1. Open {EDIT_PATH} in Excel or LibreOffice.")
    print(f"  2. Farm {code}: change {column} from {old} to {new}. Change nothing else.")
    print("  3. Save in CSV format and close the program.")
    print("  4. Run: python -m src.table_roundtrip compare")


# ---------------------------------------------------------------- compare


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        raise RoundTripError(f"File not found: {path}")
    except OSError as error:
        raise RoundTripError(f"Could not read {path}: {error}")


def count_line_endings(data: bytes) -> tuple[int, int]:
    """Return (number of CRLF, number of LF without a CR before it)."""
    crlf = data.count(b"\r\n")
    bare_lf = data.count(b"\n") - crlf
    return crlf, bare_lf


def detect_delimiter(header: str) -> str:
    """Name the delimiter used in a header line, as far as it can be told."""
    for delimiter, name in ((";", "';'"), (",", "','"), ("\t", "tab")):
        if header == delimiter.join(FARM_COLUMNS):
            return name
    return "unknown"


def check_format(original: bytes, edited: bytes) -> bool:
    """Check BOM, encoding, delimiter and line endings. Return True if all ok."""
    all_ok = True

    def report(label: str, ok: bool, detail: str) -> None:
        nonlocal all_ok  # change the variable of check_format, not a new local one
        all_ok = all_ok and ok
        print(f"  {label:<14} {'ok' if ok else 'CHANGED':<8} {detail}")

    print("Format of the edited file:")
    # Information only: after the expected change the bytes can never be identical.
    print(f"  {'size':<14} {'info':<8} {len(original)} -> {len(edited)} bytes")

    has_bom = edited.startswith(UTF8_BOM)
    report("BOM", has_bom, "present" if has_bom else "missing")

    try:
        text = edited.decode("utf-8")
    except UnicodeDecodeError:
        report("encoding", False, "not UTF-8 (probably ANSI/cp1252)")
        # Decode leniently so the remaining checks can still run.
        text = edited.decode("cp1252", errors="replace")
    else:
        report("encoding", True, "UTF-8")

    header = text.removeprefix("﻿").splitlines()[0] if text else ""
    delimiter = detect_delimiter(header)
    report("delimiter", delimiter == f"'{CSV_DELIMITER}'", delimiter)

    # A line break added at the very end is harmless: Excel adds one if the
    # file ended without it (as the fixture does), and csv.writer always
    # writes one. So both files are compared without a final line break.
    old_crlf, old_lf = count_line_endings(original.removesuffix(b"\r\n"))
    new_crlf, new_lf = count_line_endings(edited.removesuffix(b"\r\n"))
    report(
        "line endings",
        (old_crlf, old_lf) == (new_crlf, new_lf),
        f"CRLF {old_crlf} -> {new_crlf}, LF only {old_lf} -> {new_lf}",
    )
    return all_ok


def describe_difference(old: str, new: str) -> str:
    """Describe a changed field without showing its value."""
    if old.replace("\r\n", "\n") == new.replace("\r\n", "\n"):
        return "line breaks only"
    if old.strip() == new.strip():
        return "spaces at start/end only"
    return f"length {len(old)} -> {len(new)}"


def load(path: Path) -> list[dict[str, str]]:
    try:
        return read_farms(path)
    except FileNotFoundError:
        raise RoundTripError(f"File not found: {path}")
    except UnicodeDecodeError:
        raise RoundTripError(f"{path} is not UTF-8; content not compared")
    except ValueError as error:
        raise RoundTripError(f"Invalid farm table {path}: {error}")


def check_content(original_path: Path, edited_path: Path) -> bool:
    """Compare all fields. Return True if exactly EXPECTED_CHANGE was made."""
    print("Content:")
    # flush: print the heading before a possible error message on stderr
    sys.stdout.flush()
    original_farms = load(original_path)
    edited_farms = load(edited_path)

    if len(original_farms) != len(edited_farms):
        print(f"  UNEXPECTED     rows {len(original_farms)} -> {len(edited_farms)}")
        return False

    expected_code, expected_column, expected_old, expected_new = EXPECTED_CHANGE
    expected_found = False
    unexpected = 0

    # zip pairs the rows by position: 1st with 1st, 2nd with 2nd, ...
    for old_farm, new_farm in zip(original_farms, edited_farms):
        code = old_farm["farm_code"]
        for column in FARM_COLUMNS:
            old, new = old_farm[column], new_farm[column]
            if old == new:
                continue
            if (code, column, old, new) == (
                expected_code, expected_column, expected_old, expected_new
            ):
                expected_found = True
                print(f"  expected       {code} {column}")
            else:
                unexpected += 1
                print(
                    f"  UNEXPECTED     {code} {column}: {describe_difference(old, new)}"
                )

    if not expected_found:
        print(f"  MISSING        expected change {expected_code} {expected_column}")
    print(f"  {len(original_farms)} rows compared, {unexpected} unexpected changes")
    return expected_found and unexpected == 0


def compare(original_path: Path, edited_path: Path) -> bool:
    original = read_bytes(original_path)
    edited = read_bytes(edited_path)
    format_ok = check_format(original, edited)
    print()
    content_ok = check_content(original_path, edited_path)
    print()
    print("Result: format", "ok" if format_ok else "CHANGED",
          "| content", "ok" if content_ok else "NOT OK")
    return format_ok and content_ok


# ---------------------------------------------------------------- main


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    # Subcommands: the first word after the module name picks the action.
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("prepare", help="copy the test table to out/roundtrip/")
    compare_parser = subcommands.add_parser("compare", help="compare after saving")
    compare_parser.add_argument("--original", type=Path, default=ORIGINAL_PATH)
    compare_parser.add_argument("--edited", type=Path, default=EDIT_PATH)
    args = parser.parse_args()

    try:
        if args.command == "prepare":
            prepare()
        elif not compare(args.original, args.edited):
            sys.exit(1)
    except RoundTripError as error:
        sys.exit(str(error))


if __name__ == "__main__":
    main()
