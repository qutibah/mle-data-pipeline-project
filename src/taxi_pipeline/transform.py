"""Step 3a - Transform: clean the raw trips and add up revenue per day."""

from pathlib import Path

import pandas as pd

DATE_COL = "lpep_pickup_datetime"
AMOUNT_COL = "total_amount"


def read_raw(paths: list[Path]) -> pd.DataFrame:
    """Read the staged Parquet files into one table (only the 2 columns we need)."""
    frames = [pd.read_parquet(path, columns=[DATE_COL, AMOUNT_COL]) for path in paths]
    return pd.concat(frames, ignore_index=True)


def clean(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """Apply the cleaning rules found during exploration (Step 2).

    start is inclusive, end is exclusive, e.g. start="2025-01-01", end="2025-04-01".
    """
    df = df.dropna(subset=[DATE_COL, AMOUNT_COL])                        # 1. no missing values
    df = df[df[DATE_COL].between(start, end, inclusive="left")]          # 2. only our date window
    df = df[df[AMOUNT_COL] >= 0]                                         # 3. no refunds/voids
    return df


def daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Group trips by calendar day and sum the revenue."""
    result = (
        df.assign(date=df[DATE_COL].dt.date)          # 2025-01-05 14:32 -> 2025-01-05
        .groupby("date", as_index=False)
        .agg(trip_count=(AMOUNT_COL, "size"), revenue=(AMOUNT_COL, "sum"))
        .sort_values("date")
    )
    result["revenue"] = result["revenue"].round(2)
    return result
