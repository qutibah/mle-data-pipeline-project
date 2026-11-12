"""Step 1 - Extract: download the raw monthly files into data/raw/."""

from pathlib import Path

import requests

from .config import BASE_URL, FILENAME_TEMPLATE, MONTHS, RAW_DIR


def build_url(month: str) -> str:
    """Build the download link for one month, e.g. .../green_tripdata_2025-01.parquet."""
    return f"{BASE_URL}/{FILENAME_TEMPLATE.format(month=month)}"


def download_month(month: str, raw_dir: Path = RAW_DIR) -> Path:
    """Download one month. Skip it if it is already on disk (safe to re-run)."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / FILENAME_TEMPLATE.format(month=month)

    if target.exists():
        print(f"[extract] {target.name} already exists, skipping")
        return target

    url = build_url(month)
    print(f"[extract] downloading {url}")
    response = requests.get(url, timeout=120)
    response.raise_for_status()  # stop with an error on 403/404/500 instead of saving junk

    # Write to a temporary name first and rename at the end. If the download
    # crashes halfway we never leave a half-written file that looks finished.
    tmp = target.with_suffix(".part")
    tmp.write_bytes(response.content)
    tmp.replace(target)
    return target


def extract(months: tuple[str, ...] = MONTHS, raw_dir: Path = RAW_DIR) -> list[Path]:
    """Download every requested month and return the local file paths."""
    return [download_month(month, raw_dir) for month in months]


if __name__ == "__main__":
    extract()
