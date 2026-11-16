-- ==============================================================================
-- RAW LAYER TABLES
-- Best Practice: Raw tables use TEXT for all data columns to prevent ingestion 
-- failures. Type casting happens later in the staging layer.
-- ==============================================================================

-- 1. Tourism Monthly (Source: MEF API)
CREATE TABLE IF NOT EXISTS raw.tourism_monthly (
    year TEXT,
    months TEXT,
    number_of_tourists TEXT,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Weather Daily (Source: Open-Meteo API)
-- Note: We add a 'city' column because we pulled data for 3 different cities.
CREATE TABLE IF NOT EXISTS raw.weather_daily (
    city TEXT,
    time TEXT,
    temperature_2m_mean TEXT,
    precipitation_sum TEXT,
    relative_humidity_2m_mean TEXT,
    wind_speed_10m_max TEXT,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Exchange Rate Daily (Source: MEF CSV)
-- Note: We keep the ugly column name exactly as it is in the CSV.
CREATE TABLE IF NOT EXISTS raw.exchange_rate_daily (
    date TEXT,
    purchase TEXT,
    sale TEXT,
    midpoint TEXT,
    exchange_rate TEXT,
    spread_market_day_x_1_over_oer_day_x_midpoint TEXT,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);