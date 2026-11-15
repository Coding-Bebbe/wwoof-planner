"""Phase 1: show simple statistics of the farm table.

Output contains only farm codes, numbers and category names.
"""

import sys
from collections import Counter
from pathlib import Path

from src.farm_table import (
    find_duplicate_profile_urls,
    parse_guestbook_count,
    read_farms,
    split_list,
)

# Settings for phase 1
INPUT_PATH = Path("tests/fixtures/farms_sample.csv")


def sort_by_guestbook_count(farms: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return the farms sorted by guestbook entries, most entries first.

    sorted() is stable, also with reverse=True: farms with the same count
    keep their order from the file.
    """
    return sorted(farms, key=parse_guestbook_count, reverse=True)


def count_learning_categories(farms: list[dict[str, str]]) -> Counter[str]:
    """Count how many farms offer each learning category."""
    counts: Counter[str] = Counter()
    for farm in farms:
        counts.update(split_list(farm["learning_categories"]))
    return counts


def main() -> None:
    try:
        farms = read_farms(INPUT_PATH)
        sorted_farms = sort_by_guestbook_count(farms)
    except FileNotFoundError:
        sys.exit(f"File not found: {INPUT_PATH}")
    except ValueError as error:
        sys.exit(f"Invalid farm table {INPUT_PATH}: {error}")

    print(f"Read {len(farms)} farms from {INPUT_PATH}")

    print("\nGuestbook entries per farm:")
    for farm in sorted_farms:
        print(f"  {farm['farm_code']}  {parse_guestbook_count(farm):>4}")

    print("\nFarms per learning category:")
    for category, count in count_learning_categories(farms).most_common():
        print(f"  {count:>4}  {category}")

    duplicates = find_duplicate_profile_urls(farms)
    if not duplicates:
        print("\nDuplicate profile URLs: none")
    else:
        word = "group" if len(duplicates) == 1 else "groups"
        print(f"\nDuplicate profile URLs: {len(duplicates)} {word}")
        for codes in duplicates:
            print(f"  {', '.join(codes)}")


if __name__ == "__main__":
    main()
