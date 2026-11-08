"""Phase 1: read the farm table, filter it by region and write the result."""

import sys
from pathlib import Path

from src.farm_table import read_farms

# Settings for phase 1; from phase 2 on they come from config.yaml.
INPUT_PATH = Path("tests/fixtures/farms_sample.csv")
REGION = "voralpenland"


def main() -> None:
    try:
        farms = read_farms(INPUT_PATH)
    except FileNotFoundError:
        sys.exit(f"File not found: {INPUT_PATH}")
    except ValueError as error:
        sys.exit(f"Invalid farm table {INPUT_PATH}: {error}")

    print(f"Read {len(farms)} farms from {INPUT_PATH}")

    # Step 3 task: print farm_code and region of every farm, one line per farm.
    for i in farms:
        print(f"{i['farm_code']} {i['region']}")

if __name__ == "__main__":
    main()