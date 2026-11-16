-- Create the Raw schema (for untransformed API/CSV data)
CREATE SCHEMA IF NOT EXISTS raw;

-- Create the Staging schema (for cleaning, casting, and deduplication)
CREATE SCHEMA IF NOT EXISTS staging;

-- Create the Analytics schema (for final dimensional models and reporting)
CREATE SCHEMA IF NOT EXISTS analytics;