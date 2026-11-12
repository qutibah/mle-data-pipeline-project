"""Step 3b - Load: write the final table to data/processed/."""

from pathlib import Path

import pandas as pd

from .config import PROCESSED_DIR


def load(daily: pd.DataFrame, output_dir: Path = PROCESSED_DIR) -> Path:
    """Save the result as Parquet (for machines) and CSV (easy to open in Excel)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = output_dir / "daily_revenue.parquet"
    daily.to_parquet(parquet_path, index=False)
    daily.to_csv(output_dir / "daily_revenue.csv", index=False)
    return parquet_path
