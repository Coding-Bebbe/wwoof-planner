"""Phase 1: repeat the evaluations of steps 4-6 with pandas and compare.

Each evaluation is computed twice, once with the csv-based functions
and once with pandas. Output contains only evaluation names, regions
and "same"/"DIFFERENT", no farm data.
"""

import sys
from pathlib import Path

import pandas as pd

from src.farm_stats import count_learning_categories, sort_by_guestbook_count
from src.farm_table import (
    CSV_DELIMITER,
    CSV_ENCODING,
    FARM_COLUMNS,
    LIST_SEPARATOR,
    find_duplicate_profile_urls,
    parse_guestbook_count,
    read_farms,
)
from src.filter_region import filter_by_region

# Settings for phase 1
INPUT_PATH = Path("tests/fixtures/farms_sample.csv")
OUTPUT_DIR = Path("out")


def read_farms_df(path: Path) -> pd.DataFrame:
    """Read a farm table into a DataFrame with all values as text.

    dtype=str: pandas would otherwise turn guestbook_count into numbers.
    keep_default_na=False: pandas would otherwise turn empty fields and
    texts like "NA" or "null" into NaN ("not a number", i.e. missing).
    """
    df = pd.read_csv(
        path,
        sep=CSV_DELIMITER,
        encoding=CSV_ENCODING,
        dtype=str,
        keep_default_na=False,
    )
    if list(df.columns) != FARM_COLUMNS:
        raise ValueError(f"Unexpected columns: {list(df.columns)}")
    return df


def filter_by_region_df(df: pd.DataFrame, region: str) -> pd.DataFrame:
    """Return the rows whose region equals the given region."""
    # df["region"] == region gives a column of True/False (a "mask");
    # df[mask] keeps the rows where the mask is True.
    return df[df["region"] == region]


def parse_guestbook_counts_df(df: pd.DataFrame) -> pd.Series:
    """Return guestbook_count as whole numbers >= 0, as strict as parse_guestbook_count.

    pd.to_numeric would also accept " 12" or "+12", so a regular expression
    checks that the value consists of the digits 0-9 only.
    """
    valid = df["guestbook_count"].str.fullmatch(r"[0-9]+")
    if not valid.all():
        # ~ negates the mask: rows that are NOT valid.
        codes = ", ".join(df.loc[~valid, "farm_code"])
        raise ValueError(f"{codes}: guestbook_count is not a whole number >= 0")
    return df["guestbook_count"].astype(int)


def sort_by_guestbook_count_df(df: pd.DataFrame) -> pd.DataFrame:
    """Return the rows sorted by guestbook entries, most entries first.

    kind="stable" is needed: the default "quicksort" is not stable, so rows
    with the same count could change their order from the file.
    """
    counts = parse_guestbook_counts_df(df)
    return df.assign(guestbook_number=counts).sort_values(
        "guestbook_number", ascending=False, kind="stable"
    )


def count_learning_categories_df(df: pd.DataFrame) -> pd.Series:
    """Count how many farms offer each learning category."""
    # split turns each field into a list, explode gives one row per list entry.
    categories = df["learning_categories"].str.split(LIST_SEPARATOR, regex=False).explode()
    # An empty field splits into [''], the same trap as in split_list.
    categories = categories[categories != ""]
    return categories.value_counts()


def find_duplicate_profile_urls_df(df: pd.DataFrame) -> list[list[str]]:
    """Return groups of farm codes that share the same profile_url, in file order."""
    # keep=False marks every member of a group, not only the later ones.
    duplicated = df[df.duplicated("profile_url", keep=False)]
    # sort=False keeps the groups in the order of their first row.
    groups = duplicated.groupby("profile_url", sort=False)["farm_code"].agg(list)
    return groups.tolist()


def compare(path: Path, out_dir: Path) -> list[tuple[str, bool]]:
    """Compute every evaluation with csv and pandas; return (name, same) pairs."""
    farms = read_farms(path)
    df = read_farms_df(path)
    results = []

    # Step 4: filter by region, for every region in the table.
    regions = sorted(df["region"].unique())
    if len({region.lower() for region in regions}) != len(regions):
        # Windows does not distinguish file names by case (see 06_fortschritt.md).
        raise ValueError("Region names differ only in case; output files would collide")

    for region in regions:
        expected = filter_by_region(farms, region)
        selected = filter_by_region_df(df, region)
        results.append((f"filter region '{region}'", selected.to_dict("records") == expected))

        # Write with pandas and read back with the csv-based function.
        output_path = out_dir / f"farms_{region}_pandas.csv"
        out_dir.mkdir(parents=True, exist_ok=True)
        selected.to_csv(output_path, sep=CSV_DELIMITER, encoding=CSV_ENCODING, index=False)
        results.append((f"write region '{region}'", read_farms(output_path) == expected))

    # Step 5: sort by guestbook entries.
    expected_order = [
        (farm["farm_code"], parse_guestbook_count(farm)) for farm in sort_by_guestbook_count(farms)
    ]
    sorted_df = sort_by_guestbook_count_df(df)
    pandas_order = [
        (code, int(number))
        for code, number in zip(sorted_df["farm_code"], sorted_df["guestbook_number"])
    ]
    results.append(("sort by guestbook count", pandas_order == expected_order))

    # Step 5: count learning categories. Compared without order, because
    # categories with the same count may be listed in a different order.
    expected_counts = dict(count_learning_categories(farms))
    pandas_counts = {
        category: int(count) for category, count in count_learning_categories_df(df).items()
    }
    results.append(("count learning categories", pandas_counts == expected_counts))

    # Step 6: duplicate profile URLs.
    results.append((
        "duplicate profile URLs",
        find_duplicate_profile_urls_df(df) == find_duplicate_profile_urls(farms),
    ))

    return results


def main() -> None:
    try:
        results = compare(INPUT_PATH, OUTPUT_DIR)
    except FileNotFoundError:
        sys.exit(f"File not found: {INPUT_PATH}")
    except ValueError as error:
        sys.exit(f"Invalid farm table {INPUT_PATH}: {error}")
    except OSError as error:
        sys.exit(f"Could not write to {OUTPUT_DIR}: {error}")

    print(f"Compared csv and pandas results for {INPUT_PATH}:")
    for name, same in results:
        print(f"  {'same' if same else 'DIFFERENT':<9}  {name}")

    differences = sum(1 for _, same in results if not same)
    if differences:
        sys.exit(f"{differences} evaluation(s) differ")
    print("All evaluations match.")


if __name__ == "__main__":
    main()
