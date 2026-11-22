def get_month_number(month_name: str) -> int:
    """
    Converts a 3-letter month abbreviation (e.g., 'Jan') to an integer (1-12).
    Raises ValueError if the month is invalid.
    """
    if not month_name:
        raise ValueError("Month name cannot be empty")

    months = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
    }

    clean_name = month_name.strip().lower()[:3]
    # [:3]: Slices only the first 3 characters ("january" $\rightarrow$ "jan"), meaning full month names work
    if clean_name not in months:
        raise ValueError(f"Invalid month name: {month_name}")

    return months[clean_name]
