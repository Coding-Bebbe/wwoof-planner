"""Read and write farm tables in the project's CSV format."""

import csv
from pathlib import Path

CSV_DELIMITER = ";"
CSV_ENCODING = "utf-8-sig"
LIST_SEPARATOR = "|"

# Columns of farms.csv in their fixed order (03_programmierprojekt.md, section 5.3)
FARM_COLUMNS = [
    "farm_code",
    "profile_url",
    "farm_name",
    "location",
    "region",
    "description",
    "learning_categories",
    "guestbook_count",
    "available_windows",
    "displayed_names",
    "retrieved_on",
]


def read_farms(path: Path) -> list[dict[str, str]]:
    """Read a farm table and return one dictionary per farm."""
    with open(path, encoding=CSV_ENCODING, newline="") as file:
        reader = csv.DictReader(file, delimiter=CSV_DELIMITER)

        if reader.fieldnames != FARM_COLUMNS:
            raise ValueError(f"Unexpected columns: {reader.fieldnames}")

        farms = []
        for row in reader:
            # Too many fields end up under the key None,
            # missing fields get the value None.
            if None in row or None in row.values():
                raise ValueError(
                    f"Wrong number of fields in the record ending at line {reader.line_num}"
                )
            farms.append(row)

    return farms


def write_farms(path: Path, farms: list[dict[str, str]]) -> None:
    """Write farms to a farm table. An existing file is replaced."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding=CSV_ENCODING, newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FARM_COLUMNS, delimiter=CSV_DELIMITER)
        writer.writeheader()
        writer.writerows(farms)