import pytest
from src.utils.date_utils import get_month_number

# 1. Happy Path Test


def test_get_month_number_valid():
    assert get_month_number("Jan") == 1
    assert get_month_number("Dec") == 12
    assert get_month_number("  sep  ") == 9  # Tests stripping and lowercase

# 2. Error Path Test


def test_get_month_number_invalid():
    with pytest.raises(ValueError, match="Invalid month name: Blah"):
        get_month_number("Blah")

    with pytest.raises(ValueError, match="Month name cannot be empty"):
        get_month_number("")
