import pandas as pd
import pytest
from src.utils.validation_utils import (
    check_required_columns,
    check_row_count,
    check_nulls,
    check_duplicates
)

# 1. Create a valid dummy DataFrame for testing


@pytest.fixture
def valid_df():
    return pd.DataFrame({
        "city": ["Phnom Penh", "Siem Reap"],
        "date": ["2023-01-01", "2023-01-02"],
        "temp": [25.5, 26.0]
    })

# --- Test Task 1: Required Columns ---


def test_required_columns_passes(valid_df):
    check_required_columns(valid_df, ["city", "date", "temp"])


def test_required_columns_fails(valid_df):
    with pytest.raises(ValueError, match="Missing required columns"):
        check_required_columns(valid_df, ["city", "date", "humidity"])

# --- Test Task 2: Row Count ---


def test_row_count_passes(valid_df):
    check_row_count(valid_df, min_rows=2)


def test_row_count_fails(valid_df):
    with pytest.raises(ValueError, match="Row count check failed"):
        check_row_count(valid_df, min_rows=5)

# --- Test Task 3: Nulls and Duplicates ---


def test_nulls_pass(valid_df):
    check_nulls(valid_df, ["city", "date"])


def test_nulls_fail(valid_df):
    valid_df.loc[0, "city"] = None
    with pytest.raises(ValueError, match="Null check failed"):
        check_nulls(valid_df, ["city", "date"])


def test_duplicates_pass(valid_df):
    check_duplicates(valid_df, ["city", "date"])


def test_duplicates_fail(valid_df):
    # Add a duplicate row
    new_row = pd.DataFrame({"city": ["Phnom Penh"], "date": [
                           "2023-01-01"], "temp": [30.0]})
    valid_df = pd.concat([valid_df, new_row], ignore_index=True)

    with pytest.raises(ValueError, match="Duplicate check failed"):
        check_duplicates(valid_df, ["city", "date"])
