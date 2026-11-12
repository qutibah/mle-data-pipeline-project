"""Entry point: run Extract -> Transform -> Load in order.

Run with:  uv run python -m taxi_pipeline.pipeline
"""

from .config import MONTHS
from .extract import extract
from .load import load
from .transform import clean, daily_revenue, read_raw

START, END = "2025-01-01", "2025-04-01"  # first three months of 2025 (end is exclusive)


def main() -> None:
    paths = extract(MONTHS)                   # E: download into data/raw/

    raw = read_raw(paths)                     # T: read + clean + aggregate
    cleaned = clean(raw, START, END)
    daily = daily_revenue(cleaned)

    output = load(daily)                      # L: write to data/processed/

    # Compare row counts before and after cleaning, as the brief asks.
    dropped = len(raw) - len(cleaned)
    print(f"[transform] rows read:     {len(raw):,}")
    print(f"[transform] rows kept:     {len(cleaned):,}")
    print(f"[transform] rows dropped:  {dropped:,} ({dropped / len(raw):.2%})")
    print(f"[load] {len(daily)} days, total revenue ${daily['revenue'].sum():,.2f}")
    print(f"[load] written to {output}")


if __name__ == "__main__":
    main()
