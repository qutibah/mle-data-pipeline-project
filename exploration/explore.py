"""Step 2 - Explore one month of data. Not part of the pipeline; just for learning."""

import pandas as pd

from taxi_pipeline.config import RAW_DIR

df = pd.read_parquet(RAW_DIR / "green_tripdata_2025-01.parquet")

print("Shape:", df.shape)
print("\nColumns and types:\n", df.dtypes)

# The two columns we need: WHEN the trip happened, and WHAT was paid.
date_col, amount_col = "lpep_pickup_datetime", "total_amount"

print("\nMissing values:")
print(df[[date_col, amount_col]].isna().sum())

print("\nPickup date range:", df[date_col].min(), "->", df[date_col].max())
outside = ~df[date_col].between("2025-01-01", "2025-02-01", inclusive="left")
print("Trips with pickup outside January:", outside.sum())
print(df.loc[outside, date_col].sort_values().to_string()[:600])

print("\ntotal_amount stats:\n", df[amount_col].describe())
print("Negative amounts:", (df[amount_col] < 0).sum())
print("Zero amounts:", (df[amount_col] == 0).sum())
print("Amounts > 1000:", (df[amount_col] > 1000).sum())
print(df.nlargest(5, amount_col)[[date_col, "trip_distance", "fare_amount", amount_col]])
