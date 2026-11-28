import pandas as pd
import logging

logger = logging.getLogger(__name__)


def check_required_columns(df: pd.DataFrame, required_cols: list[str]):
    """Ensures all required columns exist in the DataFrame."""
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    logger.info(
        f"Schema check passed: All {len(required_cols)} required columns present.")


def check_row_count(df: pd.DataFrame, min_rows: int = 1):
    """Ensures the DataFrame has a minimum number of rows."""
    if len(df) < min_rows:
        raise ValueError(
            f"Row count check failed: Expected at least {min_rows} rows, got {len(df)}")
    logger.info(f"Row count check passed: {len(df)} rows found.")


def check_nulls(df: pd.DataFrame, critical_cols: list[str]):
    """Ensures no null values exist in critical columns."""
    null_counts = df[critical_cols].isnull().sum()
    nulls_found = null_counts[null_counts > 0]
    if not nulls_found.empty:
        raise ValueError(f"Null check failed. Nulls found in:\n{nulls_found}")
    logger.info("Null check passed: No nulls found in critical columns.")


def check_duplicates(df: pd.DataFrame, unique_cols: list[str]):
    """Ensures no duplicate rows exist based on unique identifier columns."""
    duplicates = df.duplicated(subset=unique_cols).sum()
    if duplicates > 0:
        raise ValueError(
            f"Duplicate check failed: Found {duplicates} duplicate rows based on {unique_cols}.")
    logger.info(
        f"Duplicate check passed: No duplicates found on {unique_cols}.")
