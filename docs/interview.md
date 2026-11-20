 # connection database by using Airflow's PostgresHook:
"I tested the database connectivity by using Airflow's PostgresHook inside the container. This bypasses local browser restrictions and proves that the Airflow executor can successfully authenticate and run SQL against the warehouse."


# Why? (Interview Gold): In modern Data Engineering (like the Medallion Architecture), this is the difference between Bronze, Silver, and Gold layers.

Raw (Bronze): Data exactly as it came from the API/CSV (often all text strings or messy JSON).

Staging (Silver): Cleaned data. Types are cast (e.g., text "596241" becomes integer 596241, text "Jan" becomes date 2018-01-01), nulls are handled, and deduplication happens.

Analytics (Gold): The final aggregated tables, joined together, ready for BI tools.


# "Why make every column in the raw layer TEXT?"
"To ensure the ingestion pipeline never fails. If a CSV has a missing value or a typo in a date, inserting into a DATE column will crash the pipeline. By loading everything as TEXT, we can safely capture the bad data in the raw layer and handle/filter it during the Staging transform."


# "How did you organize your database schemas?"
"I used a three-tier architecture: raw (immutable string data), staging (typed, deduplicated data), and analytics (dimensional models ready for BI). This separates concerns and makes debugging much easier."

# Why do we need a Date Dimension? (Interview Gold)
If you just store 2023-11-17 as a date in a fact table, every time an analyst wants to know "How many tourists arrived on weekends?", they have to write complex date math in their SQL. By creating a dim_date table, we pre-calculate attributes like year, month, day_of_week, and is_weekend. Analysts can just do a simple JOIN and WHERE is_weekend = TRUE.


# Why do we do confirm the base tables exist in PostgreSQL? (Interview Focus)

In a real data pipeline, you never assume the database state. A previous script might have failed silently, or you might be connected to the wrong environment. Always write verification queries to confirm your DDL (Data Definition Language) actually applied.


# "Why do we create a Date Dimension instead of just storing the date in the fact table?"

"To avoid complex date math in queries. If an analyst wants weekend data, they just join to dim_date and filter WHERE is_weekend = TRUE. It also provides a centralized, consistent calendar for all reporting."

# Why build the dimensions before the Fact tables?"

"Because Fact tables rely on the dimensions. A Fact table needs date_id and location_id as Foreign Keys. If the dimension tables don't exist yet, you can't enforce referential integrity on the Fact tables."


# What does ON CONFLICT DO NOTHING do?"

"It makes the SQL script idempotent. If the pipeline runs twice, it won't fail trying to insert duplicate cities or dates. It just skips them."


# How do you handle a dirty CSV with encoding issues?"

"If a file has a UTF-8 BOM (Byte Order Mark), it adds an invisible character to the first column name. I always read CSVs with encoding='utf-8-sig' in pandas to strip it out automatically."

# Explain how your HTTP client handles API failures."

"I use urllib3.Retry mounted to a requests.Session. It automatically retries on 429 and 5xx errors with exponential backoff (1s, 2s, 4s) to handle temporary network blips and rate limits. I also enforce a 10-second timeout to prevent hanging."

# How do you handle file paths in Python?"

"I never hardcode absolute paths. I use pathlib.Path(__file__).resolve().parent to dynamically resolve the project root, making the code portable across any environment."

# "What is an Upsert and why use it?"

"Upsert means Update or Insert. It's used to make a pipeline idempotent. Instead of risking duplicate rows when a pipeline reruns, the ON CONFLICT DO UPDATE clause checks if the row exists and updates it, or inserts it if it's new."

# How do you load 100,000 rows into PostgreSQL efficiently in Python?"

I would not use a for loop with individual INSERT statements, as that causes massive network overhead. I use psycopg2.extras.execute_values to batch the rows into a single bulk insert command."

# How do you handle database secrets in your code?"

"I use python-dotenv. Credentials are stored in a local .env file which is included in .gitignore, so they are never pushed to version control."


