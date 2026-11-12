"""Tests for the transform stage, using a tiny hand-made table (no downloads needed)."""

import pandas as pd

from taxi_pipeline.transform import AMOUNT_COL, DATE_COL, clean, daily_revenue


def make_trips() -> pd.DataFrame:
    return pd.DataFrame(
        {
            DATE_COL: pd.to_datetime(
                [
                    "2025-01-01 08:00",  # ok
                    "2025-01-01 20:00",  # ok, same day
                    "2025-01-02 09:00",  # ok
                    "2025-01-02 10:00",  # negative -> dropped
                    "2024-12-31 23:00",  # before window -> dropped
                    "2025-04-01 00:00",  # end is exclusive -> dropped
                    None,                # missing date -> dropped
                ]
            ),
            AMOUNT_COL: [10.0, 5.5, 20.0, -7.0, 99.0, 99.0, 99.0],
        }
    )


def test_clean_drops_bad_rows():
    cleaned = clean(make_trips(), "2025-01-01", "2025-04-01")
    assert len(cleaned) == 3
    assert (cleaned[AMOUNT_COL] >= 0).all()


def test_daily_revenue_sums_per_day():
    daily = daily_revenue(clean(make_trips(), "2025-01-01", "2025-04-01"))
    assert daily["revenue"].tolist() == [15.5, 20.0]
    assert daily["trip_count"].tolist() == [2, 1]
