"""Phase 1: read the farm table, filter it by region and write the result."""

import sys
from pathlib import Path

from src.farm_table import read_farms, write_farms

# Settings for phase 1; from phase 2 on they come from config.yaml.
INPUT_PATH = Path("tests/fixtures/farms_sample.csv")
REGION = "voralpenland"
OUTPUT_PATH = Path("out") / f"farms_{REGION}.csv"


def filter_by_region(farms: list[dict[str, str]], region: str) -> list[dict[str, str]]:
    """Return the farms whose region equals the given region."""
    # Step 4 task: build and return a new list with the matching farms.
    matching_farms = []
    for i in farms:
        if i["region"] == region:
            matching_farms.append(i)

    return matching_farms


def main() -> None:
    try:
        farms = read_farms(INPUT_PATH)
    except FileNotFoundError:
        sys.exit(f"File not found: {INPUT_PATH}")
    except ValueError as error:
        sys.exit(f"Invalid farm table {INPUT_PATH}: {error}")

    print(f"Read {len(farms)} farms from {INPUT_PATH}")

    selected = filter_by_region(farms, REGION)

    try:
        write_farms(OUTPUT_PATH, selected)
    except OSError as error:
        sys.exit(f"Could not write {OUTPUT_PATH}: {error}")

    print(f"Wrote {len(selected)} farms of region '{REGION}' to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()