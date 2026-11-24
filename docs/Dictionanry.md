# What does mount mean!
In the context of software development, Docker, and data pipelines (like your project setup on Day 5 shown in your roadmap), mounting (or a volume mount) means linking a folder or file from your physical computer (the host machine) directly into a running Docker container.

How It Works
Normally, everything inside a Docker container is isolated—it lives inside its own virtual file system. If you write code on your computer, the container cannot see it by default.

When you mount a folder (like your dags/ or include/ folders):

You create a bridge between your local Windows machine and the Linux container.

Any changes you save on your local machine instantly appear inside the container without needing to rebuild or restart the whole Docker image.

Why It Matters for Airflow (Day 5)
In your project roadmap, mounting the dags/ folder means Airflow can automatically read and execute the Python DAG files you write in your local code editor (like Visual Studio Code) without you having to manually copy-paste them into the container every time.


# "How do you manage database credentials in your DAGs?"
"I never hardcode them. I store the host, port, and password in an Airflow Connection. In the code, I just pass the conn_id to a PostgresHook, and Airflow handles the authentication securely."

# "How does Airflow talk to your database?"
"Via Provider Packages. I use apache-airflow-providers-postgres which gives me the PostgresHook and PostgresOperator."

# "What is the difference between the Airflow metadata DB and the warehouse DB?"

"Metadata DB stores DAG run history and connections (e.g., postgres-metadata). The Warehouse DB stores the actual analytical data (e.g., postgres-warehouse)."

# "Why did you mount an include/ folder?"

"To keep the dags/ folder clean. dags/ should only contain DAG files. Complex SQL queries, CSV lookup tables, or Python helper scripts go in include/ so Airflow doesn't waste time parsing them as DAGs."


# Why do we use schemas?
In PostgreSQL, a "schema" is like a folder inside your database. Instead of throwing all tables into the default public schema, we organize them by their data maturity:

raw: Exact copies of the source data (API responses, CSVs). No transformations.

staging: Intermediate tables where we clean, cast types, and handle nulls.

analytics: Final, business-ready tables (facts and dimensions) that Power BI or data scientists will query.

# what ingestion refering:
In data engineering, ingestion is the process of pulling raw data from external sources (like APIs, CSV files, or external databases) and loading it into your own storage system or data warehouse (like your PostgreSQL database) so your pipeline can work with it.

# what data warehouse refer to:
A data warehouse is a central database designed specifically for storing, organizing, and analyzing historical data collected from multiple different sources (like APIs, CSV files, and business apps).

# How do you test your data pipelines?"

I write unit tests for isolated transformation logic using pytest, such as date-parsing utilities. For integration tests, I verify idempotency by running the loader twice against a local database to ensure row counts remain identical."

# Why use --dev when installing pytest?"

To separate development dependencies from production dependencies. When deploying to a server, you only want to install what's needed to run the pipeline, not the testing frameworks."


# What is validation mean?

Data validation is the process of checking that data is accurate, complete, and meets defined rules before it is stored, processed, or used for analysis. Think of it as a quality-control gatekeeper that catches bad data at the door before it corrupts downstream tables, dashboards, or models.
