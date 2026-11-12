"""Step 4 - The same pipeline, orchestrated by Prefect.

Run with:  uv run python -m taxi_pipeline.flow
"""

from pathlib import Path

import pandas as pd
from prefect import flow, task

from .config import MONTHS
from .extract import download_month
from .load import load
from .pipeline import END, START
from .transform import clean, daily_revenue, read_raw


# Downloads talk to the internet, so they are the step most likely to fail.
# Prefect retries them 3 times, waiting 10 seconds between attempts.
@task(retries=3, retry_delay_seconds=10)
def extract_task(month: str) -> Path:
    return download_month(month)


@task
def transform_task(paths: list[Path]) -> pd.DataFrame:
    return daily_revenue(clean(read_raw(paths), START, END))


@task
def load_task(daily: pd.DataFrame) -> Path:
    return load(daily)


@flow(name="green-taxi-daily-revenue", log_prints=True)
def taxi_flow(months: tuple[str, ...] = MONTHS) -> Path:
    paths = [extract_task(month) for month in months]
    daily = transform_task(paths)
    return load_task(daily)


if __name__ == "__main__":
    taxi_flow()
