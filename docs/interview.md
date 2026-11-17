# connection database by using Airflow's PostgresHook:
"I tested the database connectivity by using Airflow's PostgresHook inside the container. This bypasses local browser restrictions and proves that the Airflow executor can successfully authenticate and run SQL against the warehouse."


# Why? (Interview Gold): In modern Data Engineering (like the Medallion Architecture), this is the difference between Bronze, Silver, and Gold layers.

Raw (Bronze): Data exactly as it came from the API/CSV (often all text strings or messy JSON).

Staging (Silver): Cleaned data. Types are cast (e.g., text "596241" becomes integer 596241, text "Jan" becomes date 2018-01-01), nulls are handled, and deduplication happens.

Analytics (Gold): The final aggregated tables, joined together, ready for BI tools.