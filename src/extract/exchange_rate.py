import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def extract_exchange_rate() -> list[dict]:
    """
    Extracts the exchange rate CSV from the raw data folder.
    Standardizes the date format and handles encoding issues.
    """
    # Resolve the path relative to this script's location
    # This script is in extract/, so we go up one level to the project root.
    project_root = Path(__file__).resolve().parent.parent.parent
    csv_path = project_root / "data" / "raw" / "exchange_rate_khr_usd_2003_2023.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Exchange rate file not found at {csv_path}")

    logger.info(f"Reading exchange rate data from {csv_path}")

    # 1. Read the CSV
    # encoding='utf-8-sig' handles the hidden BOM (Byte Order Mark) we found in Day 2.
    # If we don't use this, the first column name becomes '\ufeffdate' and breaks code.
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    # 2. Standardize field names (remove spaces, lowercase)
    # The original column is 'spread_market_day_x-1_over_oer_day_x_midpoint'
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    # 3. Parse the date column
    # The source format is M/D/YYYY (e.g., 4/1/2003 is April 1st).
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')

    # 4. Filter for our analysis window (2019-2023) to save space
    df = df[(df['date'] >= '2019-01-01') & (df['date'] <= '2023-12-31')]

    # 5. Convert the DataFrame into a list of dictionaries for easy database insertion
    records = df.to_dict(orient='records')

    logger.info(f"Extracted {len(records)} exchange rate records.")
    return records
