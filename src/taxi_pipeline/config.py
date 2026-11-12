"""All settings in one place, so every stage agrees on paths and months."""

from pathlib import Path

# Where the files live online. Each month is one Parquet file.
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
FILENAME_TEMPLATE = "green_tripdata_{month}.parquet"
MONTHS = ("2025-01", "2025-02", "2025-03")

# Paths are built from this file's location, so the pipeline works no matter
# which folder you run it from. parents[2] = the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
