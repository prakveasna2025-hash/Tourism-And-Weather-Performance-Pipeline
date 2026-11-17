-- Create the Date Dimension
CREATE TABLE IF NOT EXISTS analytics.dim_date (
    date_id SERIAL PRIMARY KEY,       -- Surrogate key for fast joins
    full_date DATE NOT NULL UNIQUE,   -- The actual date (e.g., 2023-01-01)
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name TEXT NOT NULL,
    day_of_month INT NOT NULL,
    day_of_week INT NOT NULL,         -- 1 = Monday, 7 = Sunday
    day_name TEXT NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

-- Populate the table from 2019-01-01 to 2023-12-31
INSERT INTO analytics.dim_date (
    full_date, year, quarter, month, month_name, 
    day_of_month, day_of_week, day_name, is_weekend
)
SELECT 
    d::date AS full_date,
    EXTRACT(YEAR FROM d)::int AS year,
    EXTRACT(QUARTER FROM d)::int AS quarter,
    EXTRACT(MONTH FROM d)::int AS month,
    TRIM(TO_CHAR(d, 'Month')) AS month_name,
    EXTRACT(DAY FROM d)::int AS day_of_month,
    EXTRACT(ISODOW FROM d)::int AS day_of_week,
    TRIM(TO_CHAR(d, 'Day')) AS day_name,
    CASE WHEN EXTRACT(ISODOW FROM d) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM generate_series(
    '2019-01-01'::timestamp, 
    '2023-12-31'::timestamp, 
    '1 day'::interval
) d
ON CONFLICT (full_date) DO NOTHING;