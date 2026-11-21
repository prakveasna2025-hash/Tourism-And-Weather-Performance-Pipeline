import logging

logger = logging.getLogger(__name__)

VALID_MONTHS = {"Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}


def validate_tourism_data(data: list[dict]) -> list[dict]:
    """
    Validates tourism data for integrity (nulls, negatives, bad formats).
    Intentionally skips statistical outlier detection to preserve COVID-era swings.
    """
    if not data:
        raise ValueError("No tourism data to validate!")

    logger.info(f"Starting validation for {len(data)} tourism records...")

    validated_data = []
    missing_months = []

    # 1. Check for Data Integrity
    for row in data:
        year = row.get("year")
        month = row.get("months")
        tourists = row.get("number_of_tourists")

        # Check for nulls
        if not year or not month or tourists is None:
            logger.warning(f"Skipping row due to missing fields: {row}")
            continue

        # Check month validity
        if month not in VALID_MONTHS:
            logger.warning(f"Skipping row with invalid month '{month}': {row}")
            continue

        # Check for negative numbers (impossible in tourism)
        if int(tourists) < 0:
            logger.warning(f"Skipping row with negative tourists: {row}")
            continue

        # ★ TASK 2: Do NOT reject COVID-era swings.
        # We do not use Z-score or IQR because 2020/2021 drops and 2022 spikes are real.

        validated_data.append(row)

    # 2. Check for Missing Months (Task 1)
    # Group the data by year to see how many months we have per year
    months_per_year = {}
    for row in validated_data:
        y = row["year"]
        months_per_year.setdefault(y, set()).add(row["months"])

    for year, months in months_per_year.items():
        # 12 months - actual months = missing months
        missing = VALID_MONTHS - months
        if missing:
            missing_months.append(f"{year}: {', '.join(missing)}")

    if missing_months:
        logger.warning(
            f"Data is missing the following months: {missing_months}")
    else:
        logger.info("All 12 months are present for every year in the dataset.")

    logger.info(
        f"Validation complete. {len(validated_data)} valid records ready for loading.")
    return validated_data
